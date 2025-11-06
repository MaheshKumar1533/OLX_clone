from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='list'),
    path('read/<int:notification_id>/', views.mark_notification_read, name='mark_read'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('delete/<int:notification_id>/', views.delete_notification, name='delete'),
    path('clear-all/', views.clear_all_notifications, name='clear_all'),
    path('preferences/', views.NotificationPreferenceView.as_view(), name='preferences'),
    path('unread-count/', views.get_unread_count, name='unread_count'),
    
    # Push notification endpoints
    path('push/vapid-key/', views.get_vapid_public_key, name='vapid_key'),
    path('push/subscribe/', views.subscribe_push, name='subscribe_push'),
    path('push/unsubscribe/', views.unsubscribe_push, name='unsubscribe_push'),
]
