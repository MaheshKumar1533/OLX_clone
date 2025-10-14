from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('sender', 'content', 'is_read', 'created_at')
    ordering = ['-created_at']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['product', 'buyer', 'seller', 'created_at', 'is_active', 'message_count']
    list_filter = ['is_active', 'created_at', 'product__category']
    search_fields = ['product__title', 'buyer__username', 'seller__username']
    readonly_fields = ('created_at', 'updated_at')
    inlines = [MessageInline]
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'conversation', 'content_preview', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['content', 'sender__username']
    readonly_fields = ('created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
