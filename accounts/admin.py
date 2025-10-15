from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, OTP

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'state', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'city', 'state', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'city']
    list_editable = ['is_verified']


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp_type', 'otp_code', 'is_verified', 'created_at', 'expires_at', 'is_expired']
    list_filter = ['otp_type', 'is_verified', 'created_at']
    search_fields = ['email', 'otp_code']
    readonly_fields = ['created_at', 'expires_at']
    
    def is_expired(self, obj):
        return not obj.is_valid()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
