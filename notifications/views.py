from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Notification, NotificationPreference
from .forms import NotificationPreferenceForm


class NotificationListView(LoginRequiredMixin, ListView):
    """View to list all notifications for the current user"""
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    
    def get_queryset(self):
        filter_type = self.request.GET.get('type')
        queryset = Notification.objects.filter(recipient=self.request.user)
        
        if filter_type == 'unread':
            queryset = queryset.filter(is_read=False)
        elif filter_type == 'read':
            queryset = queryset.filter(is_read=True)
        elif filter_type and filter_type in dict(Notification.NOTIFICATION_TYPES):
            queryset = queryset.filter(notification_type=filter_type)
            
        return queryset.select_related('sender').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = Notification.objects.filter(
            recipient=self.request.user, 
            is_read=False
        ).count()
        context['notification_types'] = Notification.NOTIFICATION_TYPES
        context['current_filter'] = self.request.GET.get('type', 'all')
        return context


@login_required
def mark_notification_read(request, notification_id):
    """Mark a single notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.mark_as_read()
    
    # If there's an action URL, redirect to it
    if notification.action_url:
        return redirect(notification.action_url)
    
    return redirect('notifications:list')


@login_required
def mark_all_read(request):
    """Mark all notifications as read for the current user"""
    if request.method == 'POST':
        updated_count = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).update(is_read=True)
        
        messages.success(request, f'Marked {updated_count} notifications as read.')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'marked_count': updated_count})
        
        return redirect('notifications:list')
    
    return redirect('notifications:list')


@login_required
def delete_notification(request, notification_id):
    """Delete a single notification"""
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.delete()
        
        messages.success(request, 'Notification deleted.')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        return redirect('notifications:list')
    
    return redirect('notifications:list')


@login_required
def clear_all_notifications(request):
    """Clear all notifications for the current user"""
    if request.method == 'POST':
        deleted_count = Notification.objects.filter(recipient=request.user).delete()[0]
        messages.success(request, f'Cleared {deleted_count} notifications.')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'deleted_count': deleted_count})
        
        return redirect('notifications:list')
    
    return redirect('notifications:list')


class NotificationPreferenceView(LoginRequiredMixin, UpdateView):
    """View to update notification preferences"""
    model = NotificationPreference
    form_class = NotificationPreferenceForm
    template_name = 'notifications/preferences.html'
    success_url = reverse_lazy('notifications:preferences')
    
    def get_object(self):
        preference, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preference
    
    def form_valid(self, form):
        messages.success(self.request, 'Notification preferences updated successfully!')
        return super().form_valid(form)


@login_required
def get_unread_count(request):
    """AJAX view to get unread notification count"""
    count = Notification.objects.filter(
        recipient=request.user, 
        is_read=False
    ).count()
    
    return JsonResponse({'unread_count': count})
