from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import random
import string

class UserProfile(models.Model):
    GRADUATION_STATUS_CHOICES = [
        ('current', 'Current Student'),
        ('recent', 'Recent Graduate (0-2 years)'),
        ('alumni', 'Alumni (2+ years)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    # College-specific fields
    college_name = models.CharField(max_length=200, blank=True, help_text="Name of your college/university")
    graduation_year = models.PositiveIntegerField(blank=True, null=True, help_text="Year of graduation")
    course = models.CharField(max_length=100, blank=True, help_text="Your course/degree (e.g., B.Tech CSE, MBA, etc.)")
    graduation_status = models.CharField(max_length=20, choices=GRADUATION_STATUS_CHOICES, default='current')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.user.username})

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

# Signal to create user profile automatically
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class OTP(models.Model):
    """Model to store OTP for email verification and password reset"""
    OTP_TYPE_CHOICES = [
        ('registration', 'Registration'),
        ('password_reset', 'Password Reset'),
    ]
    
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    
    # Store temporary registration data (for registration OTPs)
    temp_data = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'otp_type', 'is_verified']),
        ]
    
    def __str__(self):
        return f"{self.email} - {self.otp_type} - {self.otp_code}"
    
    @classmethod
    def generate_otp(cls, email, otp_type, temp_data=None):
        """Generate a new OTP"""
        from django.conf import settings
        
        # Delete old unverified OTPs for this email and type
        cls.objects.filter(
            email=email,
            otp_type=otp_type,
            is_verified=False
        ).delete()
        
        # Generate random 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))
        
        # Set expiry time
        expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
        # Create new OTP
        otp = cls.objects.create(
            email=email,
            otp_code=otp_code,
            otp_type=otp_type,
            expires_at=expires_at,
            temp_data=temp_data
        )
        
        return otp
    
    def is_valid(self):
        """Check if OTP is still valid"""
        return not self.is_verified and timezone.now() < self.expires_at
    
    @classmethod
    def verify_otp(cls, email, otp_code, otp_type):
        """Verify OTP and mark as used"""
        try:
            otp = cls.objects.get(
                email=email,
                otp_code=otp_code,
                otp_type=otp_type,
                is_verified=False
            )
            
            if otp.is_valid():
                otp.is_verified = True
                otp.save()
                return otp
            else:
                return None
        except cls.DoesNotExist:
            return None
