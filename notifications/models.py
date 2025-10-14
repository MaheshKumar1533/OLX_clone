from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Notification(models.Model):
    """Model for user notifications"""
    NOTIFICATION_TYPES = (
        ('new_message', 'New Message'),
        ('product_inquiry', 'Product Inquiry'),
        ('price_update', 'Price Update'),
        ('product_sold', 'Product Sold'),
        ('wishlist_price_drop', 'Wishlist Price Drop'),
        ('new_product_in_category', 'New Product in Category'),
        ('product_expired', 'Product Expired'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Generic foreign key to link to any model (Product, Message, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Optional action URL
    action_url = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"
    
    def mark_as_read(self):
        """Mark this notification as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])
    
    @classmethod
    def create_notification(cls, recipient, notification_type, title, message, sender=None, content_object=None, action_url=None):
        """Helper method to create a notification"""
        notification = cls.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            title=title,
            message=message,
            content_object=content_object,
            action_url=action_url
        )
        return notification


class NotificationPreference(models.Model):
    """Model for user notification preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_notifications = models.BooleanField(default=True)
    new_message_notifications = models.BooleanField(default=True)
    product_inquiry_notifications = models.BooleanField(default=True)
    price_update_notifications = models.BooleanField(default=True)
    wishlist_notifications = models.BooleanField(default=True)
    marketing_notifications = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"
