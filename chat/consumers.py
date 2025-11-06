import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Conversation, Message
from notifications.models import Notification
from notifications.push_utils import send_message_notification


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope['user']
        
        # Check if user is authenticated
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Check if user is part of this conversation
        is_participant = await self.check_conversation_participant()
        if not is_participant:
            await self.close()
            return
        
        # Join conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave conversation group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('message')
        
        # Handle typing indicator
        if 'typing' in text_data_json:
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {
                    'type': 'typing_indicator',
                    'is_typing': text_data_json['typing'],
                    'user': self.user.get_full_name() or self.user.username
                }
            )
            return
        
        if not message_text:
            return
        
        # Save message to database
        message = await self.save_message(message_text)
        
        if message:
            # Send message to conversation group
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {
                    'type': 'chat_message',
                    'message': message_text,
                    'sender_id': self.user.id,
                    'sender_username': self.user.username,
                    'sender_name': self.user.get_full_name() or self.user.username,
                    'message_id': message.id,
                    'timestamp': message.created_at.strftime('%b %d, %Y %I:%M %p'),
                    'is_read': False
                }
            )
            
            # Create notification for the other user
            await self.create_notification(message)
    
    # Receive message from conversation group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'sender_name': event['sender_name'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp'],
            'is_read': event['is_read']
        }))
    
    # Typing indicator
    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'is_typing': event['is_typing'],
            'user': event['user']
        }))
    
    @database_sync_to_async
    def check_conversation_participant(self):
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            return self.user == conversation.buyer or self.user == conversation.seller
        except Conversation.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, message_text):
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            message = Message.objects.create(
                conversation=conversation,
                sender=self.user,
                content=message_text
            )
            # Update conversation timestamp
            conversation.save()
            return message
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
    
    @database_sync_to_async
    def create_notification(self, message):
        try:
            conversation = message.conversation
            recipient = conversation.seller if self.user == conversation.buyer else conversation.buyer
            
            # Check notification preferences
            if hasattr(recipient, 'notification_preferences'):
                prefs = recipient.notification_preferences
                if not prefs.new_message_notifications:
                    return
            
            # Create in-app notification
            Notification.create_notification(
                recipient=recipient,
                sender=self.user,
                notification_type='new_message',
                title=f'New message about {conversation.product.title}',
                message=f'{self.user.get_full_name() or self.user.username} sent you a message',
                content_object=message,
                action_url=f'/chat/conversation/{conversation.id}/'
            )
            
            # Send push notification
            send_message_notification(
                sender=self.user,
                recipient=recipient,
                conversation=conversation,
                message_text=message.content
            )
            
        except Exception as e:
            print(f"Error creating notification: {e}")
