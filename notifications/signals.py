from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NotificationPreference
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_notification_preferences(sender, instance, created, **kwargs):
    """Create default notification preferences for new users"""
    if created:
        NotificationPreference.objects.create(user=instance)
