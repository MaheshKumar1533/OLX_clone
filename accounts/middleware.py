from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.utils import timezone


class SingleDeviceLoginMiddleware:
    """
    Middleware to ensure users are only logged in on one device at a time.
    If a user's session is not the most recent one, they will be logged out.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Get current session key
            current_session_key = request.session.session_key
            
            if current_session_key:
                # Get all active sessions for this user
                user_sessions = []
                all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
                
                for session in all_sessions:
                    session_data = session.get_decoded()
                    if session_data.get('_auth_user_id') == str(request.user.id):
                        user_sessions.append({
                            'session_key': session.session_key,
                            'expire_date': session.expire_date
                        })
                
                # If there are multiple sessions, keep only the most recent one
                if len(user_sessions) > 1:
                    # Sort by expire_date (most recent last)
                    user_sessions.sort(key=lambda x: x['expire_date'])
                    
                    # If current session is not the most recent, log out
                    if current_session_key != user_sessions[-1]['session_key']:
                        logout(request)
                        # Don't redirect here, just log out silently
                        # The user will be redirected by LoginRequiredMixin on next protected view

        response = self.get_response(request)
        return response
