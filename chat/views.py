from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from products.models import Product
from .models import Conversation, Message
from .forms import MessageForm, ChatStartForm
from notifications.models import Notification


class ConversationListView(LoginRequiredMixin, ListView):
    """View to list all conversations for the current user"""
    model = Conversation
    template_name = 'chat/conversation_list.html'
    context_object_name = 'conversations'
    paginate_by = 20
    
    def get_queryset(self):
        return Conversation.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user),
            is_active=True
        ).select_related('product', 'buyer', 'seller').prefetch_related('messages')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Count unread messages for each conversation
        for conversation in context['conversations']:
            other_user_func = conversation.other_user
            other_user = other_user_func(self.request.user)
            conversation.other_user_instance = other_user
            conversation.unread_count = conversation.messages.filter(
                sender=other_user, 
                is_read=False
            ).count()
        return context


class ConversationDetailView(LoginRequiredMixin, DetailView):
    """View to display conversation details and messages"""
    model = Conversation
    template_name = 'chat/conversation_detail.html'
    context_object_name = 'conversation'
    
    def get_queryset(self):
        return Conversation.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        ).select_related('product', 'buyer', 'seller')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_object()
        
        # Get messages and paginate them
        messages_list = conversation.messages.select_related('sender').all()
        paginator = Paginator(messages_list, 20)  # 20 messages per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['messages'] = page_obj
        context['message_form'] = MessageForm()
        other_user_func = conversation.other_user
        context['other_user'] = other_user_func(self.request.user)
        
        # Mark messages from other user as read
        other_user = other_user_func(self.request.user)
        conversation.messages.filter(sender=other_user, is_read=False).update(is_read=True)
        
        return context
    
    def post(self, request, *args, **kwargs):
        conversation = self.get_object()
        form = MessageForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            # Update conversation timestamp
            conversation.save(update_fields=['updated_at'])
            
            # Create notification for the other user
            other_user_func = conversation.other_user
            other_user = other_user_func(request.user)
            Notification.create_notification(
                recipient=other_user,
                sender=request.user,
                notification_type='new_message',
                title=f'New message about {conversation.product.title}',
                message=f'{request.user.get_full_name() or request.user.username} sent you a message',
                content_object=message,
                action_url=f'/chat/conversation/{conversation.id}/'
            )
            
            messages.success(request, 'Message sent successfully!')
            return redirect('chat:conversation_detail', pk=conversation.pk)
        
        return self.get(request, *args, **kwargs)


@login_required
def start_conversation(request, product_id):
    """Start a new conversation about a product"""
    product = get_object_or_404(Product, id=product_id, status='active')
    
    # Check if user is trying to chat with themselves
    if product.seller == request.user:
        messages.error(request, "You can't start a conversation about your own product.")
        return redirect('products:product_detail', pk=product.id)
    
    # Check if conversation already exists
    conversation, created = Conversation.objects.get_or_create(
        product=product,
        buyer=request.user,
        seller=product.seller,
        defaults={'is_active': True}
    )
    
    if request.method == 'POST':
        form = ChatStartForm(request.POST)
        if form.is_valid():
            # Create the first message if this is a new conversation
            if created or not conversation.messages.exists():
                Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    content=form.cleaned_data['message']
                )
                
                # Create notification for seller
                Notification.create_notification(
                    recipient=product.seller,
                    sender=request.user,
                    notification_type='product_inquiry',
                    title=f'Someone is interested in your {product.title}',
                    message=f'{request.user.get_full_name() or request.user.username} started a conversation about your product',
                    content_object=conversation,
                    action_url=f'/chat/conversation/{conversation.id}/'
                )
                
                messages.success(request, 'Conversation started! You can now chat with the seller.')
            else:
                messages.info(request, 'You already have an active conversation about this product.')
            
            return redirect('chat:conversation_detail', pk=conversation.pk)
    else:
        form = ChatStartForm()
    
    return render(request, 'chat/start_conversation.html', {
        'product': product,
        'form': form
    })


@login_required
def mark_messages_read(request, conversation_id):
    """AJAX view to mark messages as read"""
    if request.method == 'POST':
        conversation = get_object_or_404(
            Conversation, 
            Q(buyer=request.user) | Q(seller=request.user),
            id=conversation_id
        )
        
        other_user_func = conversation.other_user
        other_user = other_user_func(request.user)
        updated_count = conversation.messages.filter(
            sender=other_user, 
            is_read=False
        ).update(is_read=True)
        
        return JsonResponse({
            'success': True, 
            'marked_count': updated_count
        })
    
    return JsonResponse({'success': False})


@login_required
def conversation_search(request):
    """Search conversations"""
    query = request.GET.get('q', '')
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user),
        is_active=True
    ).select_related('product', 'buyer', 'seller')
    
    if query:
        conversations = conversations.filter(
            Q(product__title__icontains=query) |
            Q(buyer__username__icontains=query) |
            Q(seller__username__icontains=query) |
            Q(buyer__first_name__icontains=query) |
            Q(seller__first_name__icontains=query)
        )
    
    return render(request, 'chat/conversation_search.html', {
        'conversations': conversations,
        'query': query
    })
