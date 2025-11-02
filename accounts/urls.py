from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # OTP-based Registration (New)
    path('register/', views.RegisterStepOneView.as_view(), name='register'),
    path('register/verify-otp/', views.RegisterVerifyOTPView.as_view(), name='register_verify_otp'),
    path('register/resend-otp/', views.ResendOTPView.as_view(), name='resend-otp'),
    
    # OTP-based Password Reset (New)
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/resend-otp/', views.ResendPasswordResetOTPView.as_view(), name='resend-password-reset-otp'),
    
    # Old Registration (Backup - can be removed later)
    path('register-old/', views.RegisterView.as_view(), name='register_old'),
    
    # Old Password reset URLs (can be removed later)
    path('password-reset-old/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'
    ), name='password_reset_old'),
    path('password-reset-old/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done_old'),
    path('password-reset-old-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm_old'),
    path('password-reset-old-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete_old'),
    
    # Profile URLs
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<str:username>/', views.PublicProfileView.as_view(), name='public_profile'),
    path('my-products/', views.MyProductsView.as_view(), name='my_products'),
    path('my-wishlist/', views.MyWishlistView.as_view(), name='my_wishlist'),
    
    # AJAX validation endpoints
    path('check-username/', views.check_username_availability, name='check_username'),
    path('check-email/', views.check_email_availability, name='check_email'),
]
