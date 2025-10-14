# SWAPNEST - Quick Start Guide

## Starting the Application

### Option 1: With Real-Time Chat (Recommended)

```bash
cd /home/mahi/Projects/OLX_clone
source .venv/bin/activate
daphne -b 0.0.0.0 -p 8000 olx_clone.asgi:application
```

**Features**: HTTP + WebSocket support, real-time chat works perfectly

### Option 2: Without WebSocket (Basic)

```bash
cd /home/mahi/Projects/OLX_clone
source .venv/bin/activate
python manage.py runserver
```

**Features**: HTTP only, chat requires page refresh

## Accessing the Application

Open your browser and go to:

- **Homepage**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Chat**: http://localhost:8000/chat/
- **Notifications**: http://localhost:8000/notifications/

## Testing Real-Time Chat

1. **Create two user accounts** (or use existing ones)
2. **Login as User 1** in one browser (or incognito window)
3. **Login as User 2** in another browser (or another incognito window)
4. **User 1**: Create/find a product to sell
5. **User 2**: Click "Chat with Seller" on that product
6. **Start chatting** - messages will appear instantly for both users!

## Key Features

### Chat Features

✅ Real-time messaging (no refresh needed)
✅ Connection status indicator
✅ Message history
✅ Automatic notifications
✅ Typing detection ready
✅ Mobile responsive

### Notification Features

✅ New message notifications
✅ Product inquiry alerts
✅ Price update notifications
✅ Wishlist updates
✅ Customizable preferences
✅ Mark as read/unread
✅ Filter by type

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Important Notes

1. **Always use Daphne** for real-time chat functionality
2. **Check connection status** - green badge means connected
3. **Messages are saved** even if connection drops
4. **Notifications appear** at the top navigation bar
5. **Counter updates** automatically every 30 seconds

## Common Issues

### Chat not updating in real-time?

- Make sure you're using Daphne, not `manage.py runserver`
- Check the connection status badge in the chat header

### WebSocket connection failed?

- Restart the Daphne server
- Clear browser cache and reload
- Check browser console (F12) for errors

### Port already in use?

```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
daphne -b 0.0.0.0 -p 8001 olx_clone.asgi:application
```

## Development Tips

- Keep the terminal open to see server logs
- Use browser console (F12) to debug JavaScript issues
- Test with multiple browsers/incognito windows
- Check database with: `python manage.py dbshell`

Enjoy your real-time college marketplace! 🎓💬
