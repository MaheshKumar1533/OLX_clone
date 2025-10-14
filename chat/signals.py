from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from notifications.models import Notification


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """Create notification when a new message is sent"""
    if created:
        # Get the recipient (the other person in the conversation)
        conversation = instance.conversation
        recipient = conversation.seller if instance.sender == conversation.buyer else conversation.buyer
        
        # Check if user has notification preferences enabled
        try:
            if hasattr(recipient, 'notification_preferences'):
                prefs = recipient.notification_preferences
                if not prefs.new_message_notifications:
                    return
        except:
            pass  # If no preferences exist, send the notification
        
        # Create the notification
        Notification.create_notification(
            recipient=recipient,
            sender=instance.sender,
            notification_type='new_message',
            title=f'New message about {conversation.product.title}',
            message=f'{instance.sender.get_full_name() or instance.sender.username} sent you a message',
            content_object=instance,
            action_url=f'/chat/conversation/{conversation.id}/'
        )
