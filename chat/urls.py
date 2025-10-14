from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ConversationListView.as_view(), name='conversation_list'),
    path('conversation/<int:pk>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    path('start/<int:product_id>/', views.start_conversation, name='start_conversation'),
    path('search/', views.conversation_search, name='search'),
    path('mark-read/<int:conversation_id>/', views.mark_messages_read, name='mark_messages_read'),
]
