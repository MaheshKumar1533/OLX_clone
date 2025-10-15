from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_otp_email(email, otp_code, otp_type):
    """Send OTP email to user"""
    
    if otp_type == 'registration':
        subject = 'Verify Your STUDYSWAP Account'
        message = f"""
        Welcome to STUDYSWAP!
        
        Your verification code is: {otp_code}
        
        This code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.
        
        If you didn't request this code, please ignore this email.
        
        Best regards,
        STUDYSWAP Team
        """
    else:  # password_reset
        subject = 'Reset Your STUDYSWAP Password'
        message = f"""
        Hello,
        
        You requested to reset your password for STUDYSWAP.
        
        Your verification code is: {otp_code}
        
        This code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.
        
        If you didn't request this, please ignore this email and your password will remain unchanged.
        
        Best regards,
        STUDYSWAP Team
        """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
