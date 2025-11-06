from django import forms
from .models import NotificationPreference


class NotificationPreferenceForm(forms.ModelForm):
    """Form for user notification preferences"""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'email_notifications',
            'push_notifications',
            'new_message_notifications', 
            'product_inquiry_notifications',
            'price_update_notifications',
            'wishlist_notifications',
            'marketing_notifications'
        ]
        
        widgets = {
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'push_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'new_message_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'product_inquiry_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price_update_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wishlist_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'marketing_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'email_notifications': 'Send email notifications',
            'push_notifications': 'Browser push notifications',
            'new_message_notifications': 'New message alerts',
            'product_inquiry_notifications': 'Product inquiry notifications',
            'price_update_notifications': 'Price change notifications',
            'wishlist_notifications': 'Wishlist item updates',
            'marketing_notifications': 'Marketing and promotional emails',
        }
        
        help_texts = {
            'email_notifications': 'Receive notifications via email',
            'push_notifications': 'Receive real-time push notifications in your browser',
            'new_message_notifications': 'Get notified when someone sends you a message',
            'product_inquiry_notifications': 'Get notified when someone inquires about your products',
            'price_update_notifications': 'Get notified when product prices change',
            'wishlist_notifications': 'Get notified about updates to your wishlist items',
            'marketing_notifications': 'Receive promotional offers and news about STUDISWAP',
        }
