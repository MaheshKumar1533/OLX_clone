from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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
