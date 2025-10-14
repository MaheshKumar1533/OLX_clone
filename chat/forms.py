from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    """Form for sending messages in chat"""
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Type your message here...',
            'class': 'form-control'
        }),
        max_length=1000,
        help_text='Maximum 1000 characters'
    )
    
    class Meta:
        model = Message
        fields = ['content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ''


class ChatStartForm(forms.Form):
    """Form to start a new chat about a product"""
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Hi! I\'m interested in your product. Can you tell me more about it?',
            'class': 'form-control'
        }),
        max_length=1000,
        help_text='Start the conversation with the seller',
        initial='Hi! I\'m interested in your product. Can you tell me more about it?'
    )
