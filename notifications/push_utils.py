"""
Utility functions for sending push notifications
"""
from django.conf import settings
from .models import WebPushDevice
from pywebpush import webpush, WebPushException
import json


def send_push_notification(user, title, message, url=None, tag='studiswap-notification'):
    """
    Send push notification to all active devices of a user
    
    Args:
        user: User object
        title: Notification title
        message: Notification message
        url: Optional URL to open when notification is clicked
        tag: Notification tag for grouping
    
    Returns:
        Number of devices notified successfully
    """
    if not settings.VAPID_PRIVATE_KEY or not settings.VAPID_PUBLIC_KEY:
        print("VAPID keys not configured. Push notifications disabled.")
        return 0
    
    # Check if user has push notifications enabled
    if hasattr(user, 'notification_preferences'):
        prefs = user.notification_preferences
        if not prefs.push_notifications:
            return 0
    
    # Get all active devices for this user
    devices = WebPushDevice.objects.filter(user=user, is_active=True)
    
    if not devices.exists():
        return 0
    
    # Prepare notification data
    notification_data = {
        'title': title,
        'body': message,
        'message': message,  # Backwards compatibility
        'icon': '/static/icons/favicon.png',
        'badge': '/static/icons/favicon.png',
        'url': url or '/',
        'action_url': url or '/',
        'tag': tag,
        'requireInteraction': False
    }
    
    success_count = 0
    
    for device in devices:
        try:
            subscription_info = device.get_subscription_info()
            
            if not subscription_info:
                continue
            
            # Send push notification
            webpush(
                subscription_info=subscription_info,
                data=json.dumps(notification_data),
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": settings.VAPID_ADMIN_EMAIL
                }
            )
            
            success_count += 1
            
        except WebPushException as e:
            print(f"WebPush error for device {device.id}: {e}")
            
            # If subscription is invalid, deactivate the device
            if e.response and e.response.status_code in [404, 410]:
                device.is_active = False
                device.save()
                
        except Exception as e:
            print(f"Error sending push notification to device {device.id}: {e}")
    
    return success_count


def send_message_notification(sender, recipient, conversation, message_text):
    """
    Send push notification for a new chat message
    
    Args:
        sender: User who sent the message
        recipient: User who should receive the notification
        conversation: Conversation object
        message_text: The message content
    """
    title = f"New message from {sender.get_full_name() or sender.username}"
    
    # Truncate long messages
    if len(message_text) > 100:
        message = message_text[:97] + '...'
    else:
        message = message_text
    
    url = f'/chat/conversation/{conversation.id}/'
    
    return send_push_notification(
        user=recipient,
        title=title,
        message=message,
        url=url,
        tag=f'chat-{conversation.id}'
    )
