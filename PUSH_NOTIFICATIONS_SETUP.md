# Push Notifications Setup Guide

This guide will help you set up browser push notifications for chat messages in StudiSwap.

## Prerequisites

1. **Python package installed**: `pywebpush` (already added to requirements.txt)
2. **HTTPS connection**: Push notifications require HTTPS (use localhost for development)
3. **Modern browser**: Chrome, Firefox, Edge, or Safari

## Setup Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate VAPID Keys

VAPID keys are required for web push notifications. Generate them using:

```bash
python manage.py generate_vapid_keys
```

This will output something like:

```
=== VAPID Keys Generated Successfully ===

Add these to your settings.py or .env file:

VAPID_PRIVATE_KEY = "your-private-key-here"
VAPID_PUBLIC_KEY = "your-public-key-here"
VAPID_ADMIN_EMAIL = "mailto:your-email@example.com"

=== Keep the private key secure! ===
```

### 3. Add VAPID Keys to Environment

Create a `.env` file in your project root (if not already exists) and add:

```env
VAPID_PRIVATE_KEY=your-private-key-here
VAPID_PUBLIC_KEY=your-public-key-here
VAPID_ADMIN_EMAIL=mailto:studiswap@gmail.com
```

**Important**: Never commit the `.env` file to version control!

### 4. Run Migrations

Create and apply migrations for the new WebPushDevice model:

```bash
python manage.py makemigrations notifications
python manage.py migrate
```

### 5. Test Push Notifications

#### Development (localhost):

1. Start the development server:

   ```bash
   python manage.py runserver
   ```

2. Visit http://localhost:8000 in your browser

3. Log in to your account

4. Go to Notifications → Preferences (or visit `/notifications/preferences/`)

5. Click "Enable Browser Push Notifications"

6. Allow notifications when prompted by your browser

7. Open a chat conversation and send a message from another user

8. You should receive a push notification!

#### Production (HTTPS):

For production deployment, ensure:

1. Your site is served over HTTPS
2. VAPID keys are set in environment variables
3. Service worker is accessible at `/static/js/service-worker.js`
4. Redis is configured for Channels (for multi-server deployments)

## How It Works

### Architecture

1. **Service Worker** (`static/js/service-worker.js`):

   - Runs in the background
   - Handles push events
   - Displays notifications
   - Manages notification clicks

2. **Push Manager** (`static/js/push-notifications.js`):

   - Requests notification permission
   - Subscribes to push notifications
   - Sends subscription to server
   - Auto-initializes for logged-in users

3. **Backend** (`notifications/push_utils.py`):

   - Sends push notifications using pywebpush
   - Manages device subscriptions
   - Handles failed notifications

4. **Chat Consumer** (`chat/consumers.py`):
   - Triggers push notifications when messages are sent
   - Checks user preferences before sending

### User Flow

1. User visits the site (logged in)
2. Service worker automatically registers
3. User enables push notifications in preferences
4. Browser requests permission
5. Subscription info sent to server
6. When a message is received:
   - In-app notification created
   - Push notification sent to all active devices
   - User sees notification even if browser is closed

## Notification Preferences

Users can control push notifications in two places:

1. **App Settings** (`/notifications/preferences/`):

   - Enable/disable push notifications entirely
   - Control which types of notifications to receive

2. **Browser Settings**:
   - Allow/block notifications for the site
   - Manage notification permissions

## Troubleshooting

### Push notifications not working?

1. **Check VAPID keys are set**:

   ```python
   python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.VAPID_PUBLIC_KEY)
   ```

2. **Check browser console for errors**:

   - Open Developer Tools (F12)
   - Look for service worker registration errors
   - Check for permission denied messages

3. **Verify service worker is registered**:

   - Chrome: chrome://serviceworker-internals/
   - Firefox: about:debugging#/runtime/this-firefox

4. **Check notification permissions**:

   - Chrome: chrome://settings/content/notifications
   - Firefox: about:preferences#privacy

5. **Test with browser notification API**:
   ```javascript
   Notification.requestPermission().then((permission) => {
     if (permission === "granted") {
       new Notification("Test", { body: "Push notifications work!" });
     }
   });
   ```

### Common Issues

**"Service Worker registration failed"**

- Ensure service-worker.js is accessible at `/static/js/service-worker.js`
- Check that static files are being served correctly

**"VAPID public key not configured"**

- Run `python manage.py generate_vapid_keys`
- Add keys to environment variables
- Restart the server

**"Notification permission denied"**

- User must grant permission in browser
- Check browser settings for the site
- Try in incognito mode (fresh permissions)

**"Push notifications not received"**

- Check user notification preferences
- Verify WebPushDevice entry exists for user
- Check server logs for errors
- Ensure pywebpush is installed correctly

## Testing

### Manual Testing

1. Create two user accounts
2. Enable push notifications for User A
3. Log in as User B
4. Send a message to User A about a product
5. User A should receive a push notification

### Test with cURL

You can test push notification delivery:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from notifications.push_utils import send_push_notification

user = User.objects.get(username='your_username')
send_push_notification(
    user=user,
    title='Test Notification',
    message='This is a test push notification',
    url='/notifications/'
)
```

## Production Considerations

### Security

- Never expose VAPID private key
- Use environment variables for sensitive data
- Implement rate limiting for subscriptions
- Validate all user input

### Performance

- Push notifications are sent asynchronously
- Failed subscriptions are automatically deactivated
- Consider using Celery for large-scale notifications

### Monitoring

- Log push notification failures
- Track subscription statistics
- Monitor notification delivery rates
- Set up alerts for high failure rates

## Browser Support

| Browser    | Support    | Notes                        |
| ---------- | ---------- | ---------------------------- |
| Chrome     | ✅ Full    | Desktop & Android            |
| Firefox    | ✅ Full    | Desktop & Android            |
| Edge       | ✅ Full    | Desktop only                 |
| Safari     | ⚠️ Limited | Desktop only, requires HTTPS |
| Opera      | ✅ Full    | Desktop & Android            |
| iOS Safari | ❌ None    | Not supported                |

## Additional Resources

- [Web Push Protocol](https://developers.google.com/web/fundamentals/push-notifications)
- [pywebpush Documentation](https://github.com/web-push-libs/pywebpush)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)

## Support

For issues or questions, contact: studiswap@gmail.com
