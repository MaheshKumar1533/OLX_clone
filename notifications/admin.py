from django.contrib import admin
from .models import Notification, NotificationPreference, WebPushDevice


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'title', 'message']
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = "Mark selected notifications as unread"


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'email_notifications', 'push_notifications', 
        'new_message_notifications', 'product_inquiry_notifications', 
        'price_update_notifications'
    ]
    list_filter = [
        'email_notifications', 'push_notifications',
        'new_message_notifications', 'product_inquiry_notifications', 
        'price_update_notifications'
    ]
    search_fields = ['user__username']


@admin.register(WebPushDevice)
class WebPushDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'browser', 'device_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'browser', 'created_at']
    search_fields = ['user__username', 'device_name', 'browser']
    readonly_fields = ('created_at', 'updated_at', 'subscription_info')
    actions = ['activate_devices', 'deactivate_devices']
    
    def activate_devices(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} devices activated.')
    activate_devices.short_description = "Activate selected devices"
    
    def deactivate_devices(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} devices deactivated.')
    deactivate_devices.short_description = "Deactivate selected devices"
