from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Conversation(models.Model):
    """Model for conversation between two users about a product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='conversations')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_conversations')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('product', 'buyer', 'seller')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Conversation about {self.product.title} between {self.buyer.username} and {self.seller.username}"
    
    @property
    def other_user(self):
        """Get the other participant in the conversation from perspective of current user"""
        def get_other(current_user):
            return self.seller if current_user == self.buyer else self.buyer
        return get_other
    
    @property
    def latest_message(self):
        """Get the latest message in this conversation"""
        return self.messages.first()


class Message(models.Model):
    """Model for individual messages within a conversation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"
    
    def mark_as_read(self):
        """Mark this message as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])
