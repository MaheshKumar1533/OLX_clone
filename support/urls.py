from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.HelpCenterView.as_view(), name='help_center'),
    path('create-ticket/', views.CreateSupportTicketView.as_view(), name='create_ticket'),
    path('ticket-success/', views.TicketSuccessView.as_view(), name='ticket_success'),
    path('my-tickets/', views.MyTicketsView.as_view(), name='my_tickets'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
]
