from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import SupportTicket, TicketReply
from .forms import SupportTicketForm, TicketReplyForm


class HelpCenterView(TemplateView):
    """Help center landing page with FAQs and support options"""
    template_name = 'support/help_center.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Common FAQs
        context['faqs'] = [
            {
                'question': 'How do I create a product listing?',
                'answer': 'Go to the "Sell" section and click "Create New Listing". Fill in the product details, upload images, and submit.'
            },
            {
                'question': 'How do I contact a seller?',
                'answer': 'Click on any product and use the "Chat with Seller" button to start a conversation directly.'
            },
            {
                'question': 'Is my college email required?',
                'answer': 'Yes, we verify college emails to ensure a safe community of students and graduates.'
            },
            {
                'question': 'How do I reset my password?',
                'answer': 'Click "Forgot Password" on the login page and follow the OTP verification process.'
            },
            {
                'question': 'Can I edit my listings?',
                'answer': 'Yes! Go to "My Products" and click the edit icon on any of your listings.'
            },
            {
                'question': 'How do notifications work?',
                'answer': 'You receive notifications for new messages, product updates, and other important activities.'
            },
        ]
        
        return context


class CreateSupportTicketView(CreateView):
    """Create a new support ticket"""
    model = SupportTicket
    form_class = SupportTicketForm
    template_name = 'support/create_ticket.html'
    success_url = reverse_lazy('support:ticket_success')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Associate ticket with user if authenticated
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        
        response = super().form_valid(form)
        
        # Send email notification to admin
        self.send_admin_notification(self.object)
        
        # Send confirmation email to user
        self.send_user_confirmation(self.object)
        
        messages.success(
            self.request, 
            f'Your support ticket #{self.object.id} has been created successfully. We will get back to you soon!'
        )
        
        return response
    
    def send_admin_notification(self, ticket):
        """Send email notification to admin"""
        try:
            subject = f'New Support Ticket #{ticket.id}: {ticket.subject}'
            
            # Plain text message
            message = f"""
New Support Ticket Received

Ticket ID: #{ticket.id}
From: {ticket.name} ({ticket.email})
Category: {ticket.get_category_display()}
Priority: {ticket.get_priority_display()}
Subject: {ticket.subject}

Description:
{ticket.description}

View and respond to this ticket in the admin panel.
            """
            
            # HTML message
            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #3b82f6; border-bottom: 2px solid #3b82f6; padding-bottom: 10px;">
                        New Support Ticket
                    </h2>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Ticket ID:</strong> #{ticket.id}</p>
                        <p><strong>From:</strong> {ticket.name} ({ticket.email})</p>
                        <p><strong>Category:</strong> <span style="background-color: #e3f2fd; padding: 2px 8px; border-radius: 3px;">{ticket.get_category_display()}</span></p>
                        <p><strong>Priority:</strong> <span style="background-color: #fff3cd; padding: 2px 8px; border-radius: 3px;">{ticket.get_priority_display()}</span></p>
                        <p><strong>Subject:</strong> {ticket.subject}</p>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h3 style="color: #555;">Description:</h3>
                        <p style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3b82f6; border-radius: 3px;">
                            {ticket.description}
                        </p>
                    </div>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center;">
                        <p style="color: #666; font-size: 14px;">
                            Please log in to the admin panel to view and respond to this ticket.
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['studiswap@gmail.com'],
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=True)
            
        except Exception as e:
            print(f"Error sending admin notification: {e}")
    
    def send_user_confirmation(self, ticket):
        """Send confirmation email to user"""
        try:
            subject = f'Support Ticket #{ticket.id} Received - STUDISWAP'
            
            message = f"""
Dear {ticket.name},

Thank you for contacting STUDISWAP support!

Your ticket has been received and assigned ID #{ticket.id}. Our support team will review your request and respond as soon as possible.

Ticket Details:
- Subject: {ticket.subject}
- Category: {ticket.get_category_display()}
- Priority: {ticket.get_priority_display()}

You can check the status of your ticket by logging into your account and visiting the Help Center.

Best regards,
STUDISWAP Support Team
            """
            
            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #3b82f6;">Support Ticket Received</h2>
                    
                    <p>Dear {ticket.name},</p>
                    
                    <p>Thank you for contacting <strong>STUDISWAP</strong> support!</p>
                    
                    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Your ticket has been received and assigned ID:</strong></p>
                        <h3 style="color: #3b82f6; margin: 10px 0;">#{ticket.id}</h3>
                    </div>
                    
                    <p>Our support team will review your request and respond as soon as possible.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h4 style="margin-top: 0;">Ticket Details:</h4>
                        <p><strong>Subject:</strong> {ticket.subject}</p>
                        <p><strong>Category:</strong> {ticket.get_category_display()}</p>
                        <p><strong>Priority:</strong> {ticket.get_priority_display()}</p>
                    </div>
                    
                    <p>Best regards,<br>
                    <strong>STUDISWAP Support Team</strong></p>
                </div>
            </body>
            </html>
            """
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[ticket.email],
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=True)
            
        except Exception as e:
            print(f"Error sending user confirmation: {e}")


class TicketSuccessView(TemplateView):
    """Success page after ticket creation"""
    template_name = 'support/ticket_success.html'


class MyTicketsView(LoginRequiredMixin, ListView):
    """List of user's support tickets"""
    model = SupportTicket
    template_name = 'support/my_tickets.html'
    context_object_name = 'tickets'
    paginate_by = 10
    
    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user).order_by('-created_at')


class TicketDetailView(LoginRequiredMixin, DetailView):
    """View ticket details and replies"""
    model = SupportTicket
    template_name = 'support/ticket_detail.html'
    context_object_name = 'ticket'
    
    def get_queryset(self):
        # Users can only view their own tickets
        return SupportTicket.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reply_form'] = TicketReplyForm()
        context['replies'] = self.object.replies.all()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TicketReplyForm(request.POST)
        
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = self.object
            reply.user = request.user
            reply.save()
            
            messages.success(request, 'Your reply has been added.')
            return redirect('support:ticket_detail', pk=self.object.pk)
        
        context = self.get_context_data()
        context['reply_form'] = form
        return self.render_to_response(context)
