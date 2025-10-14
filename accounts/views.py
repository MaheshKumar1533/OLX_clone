from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from .forms import UserRegistrationForm, UserUpdateForm, UserProfileForm
from .models import UserProfile
from products.models import Product, Wishlist

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('products:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Registration successful! Welcome to STUDYSWAP.')
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
