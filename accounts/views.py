from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from django.utils import timezone
from .forms import (
    UserRegistrationForm, UserUpdateForm, UserProfileForm,
    RegistrationStepOneForm, OTPVerificationForm,
    PasswordResetRequestForm, PasswordResetConfirmForm
)
from .models import UserProfile, OTP
from .utils import send_otp_email
from products.models import Product, Wishlist


class LoginView(BaseLoginView):
    """Custom login view that logs out user from all other devices"""
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        # Get the user before login
        user = form.get_user()
        
        # Delete all existing sessions for this user
        # Get all sessions
        all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        
        for session in all_sessions:
            session_data = session.get_decoded()
            if session_data.get('_auth_user_id') == str(user.id):
                session.delete()
        
        # Now perform the login (creates a new session)
        response = super().form_valid(form)
        
        messages.success(self.request, f'Welcome back, {user.username}! You have been logged in.')
        
        return response

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('products:shop')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Clear any existing sessions for this user (shouldn't be any for new user, but just in case)
        user = self.object
        all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in all_sessions:
            session_data = session.get_decoded()
            if session_data.get('_auth_user_id') == str(user.id):
                session.delete()
        
        # Login the new user
        login(self.request, self.object)
        messages.success(self.request, 'Registration successful! Welcome to STUDISWAP.')
        return response

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        context['products_count'] = Product.objects.filter(seller=self.request.user).count()
        context['active_products_count'] = Product.objects.filter(
            seller=self.request.user, 
            status='active'
        ).count()
        return context

class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['profile_form'] = UserProfileForm(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        
        context = self.get_context_data()
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return self.render_to_response(context)

class PublicProfileView(TemplateView):
    template_name = 'accounts/public_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=kwargs['username'])
        context['profile_user'] = user
        context['profile'] = user.profile
        context['products'] = Product.objects.filter(
            seller=user, 
            status='active'
        ).order_by('-created_at')[:10]
        context['products_count'] = Product.objects.filter(
            seller=user, 
            status='active'
        ).count()
        return context

class MyProductsView(LoginRequiredMixin, ListView):
    template_name = 'accounts/my_products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).order_by('-created_at')

class MyWishlistView(LoginRequiredMixin, ListView):
    template_name = 'accounts/my_wishlist.html'
    context_object_name = 'wishlist_items'
    paginate_by = 12

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product').order_by('-created_at')


# OTP-based Registration Views

class RegisterStepOneView(View):
    """Step 1: Collect user details and send OTP"""
    template_name = 'accounts/register_step1.html'
    
    def get(self, request):
        form = RegistrationStepOneForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = RegistrationStepOneForm(request.POST)
        
        if form.is_valid():
            # Store form data in session
            request.session['registration_data'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'password': form.cleaned_data['password1'],
            }
            
            # Generate and send OTP
            email = form.cleaned_data['email']
            otp = OTP.generate_otp(
                email=email,
                otp_type='registration',
                temp_data=request.session['registration_data']
            )
            
            if send_otp_email(email, otp.otp_code, 'registration'):
                messages.success(request, f'Verification code sent to {email}')
                return redirect('accounts:register_verify_otp')
            else:
                messages.error(request, 'Failed to send verification email. Please try again.')
        
        return render(request, self.template_name, {'form': form})


class RegisterVerifyOTPView(View):
    """Step 2: Verify OTP and create account"""
    template_name = 'accounts/register_verify_otp.html'
    
    def get(self, request):
        if 'registration_data' not in request.session:
            messages.error(request, 'Please start the registration process again.')
            return redirect('accounts:register_step1')
        
        form = OTPVerificationForm()
        email = request.session['registration_data'].get('email')
        return render(request, self.template_name, {'form': form, 'email': email})
    
    def post(self, request):
        if 'registration_data' not in request.session:
            messages.error(request, 'Session expired. Please start again.')
            return redirect('accounts:register_step1')
        
        form = OTPVerificationForm(request.POST)
        email = request.session['registration_data'].get('email')
        
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            otp = OTP.verify_otp(email, otp_code, 'registration')
            
            if otp:
                # Create user account
                reg_data = request.session['registration_data']
                
                try:
                    with transaction.atomic():
                        user = User.objects.create_user(
                            username=reg_data['username'],
                            email=reg_data['email'],
                            first_name=reg_data['first_name'],
                            last_name=reg_data['last_name'],
                            password=reg_data['password']
                        )
                        
                        # Mark profile as verified
                        user.profile.is_verified = True
                        user.profile.save()
                        
                        # Clear session data
                        del request.session['registration_data']
                        
                        # Log the user in
                        login(request, user)
                        
                        messages.success(request, 'Account created successfully! Welcome to STUDYSWAP.')
                        return redirect('products:shop')
                        
                except Exception as e:
                    messages.error(request, f'Error creating account: {str(e)}')
            else:
                messages.error(request, 'Invalid or expired OTP. Please try again.')
        
        return render(request, self.template_name, {'form': form, 'email': email})


class ResendOTPView(View):
    """Resend OTP for registration"""
    
    def post(self, request):
        if 'registration_data' not in request.session:
            messages.error(request, 'Session expired. Please start registration again.')
            return redirect('accounts:register_step1')
        
        email = request.session['registration_data'].get('email')
        
        # Generate new OTP
        otp = OTP.generate_otp(
            email=email,
            otp_type='registration',
            temp_data=request.session['registration_data']
        )
        
        if send_otp_email(email, otp.otp_code, 'registration'):
            messages.success(request, f'New verification code sent to {email}')
        else:
            messages.error(request, 'Failed to send verification email.')
        
        return redirect('accounts:register_verify_otp')


# OTP-based Password Reset Views

class PasswordResetRequestView(View):
    """Request password reset OTP"""
    template_name = 'accounts/password_reset_request.html'
    
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Generate and send OTP
            otp = OTP.generate_otp(email=email, otp_type='password_reset')
            
            if send_otp_email(email, otp.otp_code, 'password_reset'):
                request.session['reset_email'] = email
                messages.success(request, f'Password reset code sent to {email}')
                return redirect('accounts:password_reset_confirm')
            else:
                messages.error(request, 'Failed to send reset email. Please try again.')
        
        return render(request, self.template_name, {'form': form})


class PasswordResetConfirmView(View):
    """Verify OTP and reset password"""
    template_name = 'accounts/password_reset_confirm_otp.html'
    
    def get(self, request):
        if 'reset_email' not in request.session:
            messages.error(request, 'Please request a password reset first.')
            return redirect('accounts:password_reset_request')
        
        form = PasswordResetConfirmForm()
        email = request.session['reset_email']
        return render(request, self.template_name, {'form': form, 'email': email})
    
    def post(self, request):
        if 'reset_email' not in request.session:
            messages.error(request, 'Session expired. Please start again.')
            return redirect('accounts:password_reset_request')
        
        form = PasswordResetConfirmForm(request.POST)
        email = request.session['reset_email']
        
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            otp = OTP.verify_otp(email, otp_code, 'password_reset')
            
            if otp:
                # Reset password
                try:
                    user = User.objects.get(email=email)
                    user.set_password(form.cleaned_data['new_password1'])
                    user.save()
                    
                    # Clear session
                    del request.session['reset_email']
                    
                    messages.success(request, 'Password reset successfully! You can now log in.')
                    return redirect('accounts:login')
                    
                except User.DoesNotExist:
                    messages.error(request, 'User not found.')
            else:
                messages.error(request, 'Invalid or expired OTP. Please try again.')
        
        return render(request, self.template_name, {'form': form, 'email': email})


class ResendPasswordResetOTPView(View):
    """Resend OTP for password reset"""
    
    def post(self, request):
        if 'reset_email' not in request.session:
            messages.error(request, 'Session expired. Please start again.')
            return redirect('accounts:password_reset_request')
        
        email = request.session['reset_email']
        
        # Generate new OTP
        otp = OTP.generate_otp(email=email, otp_type='password_reset')
        
        if send_otp_email(email, otp.otp_code, 'password_reset'):
            messages.success(request, f'New reset code sent to {email}')
        else:
            messages.error(request, 'Failed to send reset email.')
        
        return redirect('accounts:password_reset_confirm')
