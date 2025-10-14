# Real-Time Chat Implementation - SWAPNEST

## Overview

The chat feature has been upgraded from standard HTTP requests to real-time WebSocket communication using Django Channels. This allows for instant message delivery without requiring page refreshes.

## What Was Changed

### 1. **Installed Dependencies**

- `channels==4.3.1` - Django Channels for WebSocket support
- `channels-redis==4.3.0` - Redis backend for channel layers (optional, using InMemory for now)
- `daphne==4.2.1` - ASGI server to handle WebSocket connections

### 2. **Updated Settings (`olx_clone/settings.py`)**

- Added `daphne` as the first app in `INSTALLED_APPS` (required for Channels)
- Added `channels` to `INSTALLED_APPS`
- Configured `ASGI_APPLICATION` to use custom ASGI routing
- Added `CHANNEL_LAYERS` configuration (using InMemoryChannelLayer for development)

### 3. **Updated ASGI Configuration (`olx_clone/asgi.py`)**

- Configured Protocol Type Router to handle both HTTP and WebSocket connections
- Added WebSocket routing with authentication middleware
- Integrated chat WebSocket URL patterns

### 4. **Created WebSocket Consumer (`chat/consumers.py`)**

The `ChatConsumer` class handles:

- WebSocket connection/disconnection
- Authentication checks
- Participant verification
- Real-time message sending/receiving
- Message persistence to database
- Notification creation
- Typing indicators (optional feature)

### 5. **Created WebSocket Routing (`chat/routing.py`)**

- Defined WebSocket URL pattern: `ws/chat/<conversation_id>/`
- Routes WebSocket connections to the ChatConsumer

### 6. **Updated Chat Template (`templates/chat/conversation_detail.html`)**

Enhanced with:

- **WebSocket Connection**: Establishes real-time connection to the chat room
- **Real-time Message Display**: New messages appear instantly without refresh
- **Connection Status Indicator**: Shows "Connected", "Disconnected", or "Error"
- **Auto-scroll**: Automatically scrolls to new messages
- **Typing Indicators**: (Ready for implementation)
- **Better UX**: Messages appear with smooth animations
- **Error Handling**: Shows reconnection message if connection is lost

## How It Works

1. **User opens chat page** → WebSocket connection is established
2. **User types message** → Message is sent via WebSocket (not HTTP POST)
3. **Server receives message** → Saves to database and broadcasts to conversation group
4. **Both users receive message** → Message appears instantly in their chat window
5. **Notification created** → Other user gets notified about new message

## Key Features

### Real-Time Messaging

- Messages appear instantly for both users
- No page refresh needed
- Smooth user experience

### Connection Status

- Visual indicator showing connection status
- Green badge: Connected
- Grey badge: Disconnected
- Red badge: Error

### Message Persistence

- All messages are saved to database
- Messages remain available after refresh
- Message history is preserved

### Notifications

- Automatic notification creation when messages are sent
- Notifications respect user preferences
- Links directly to the conversation

## Running the Application

### Development Mode

```bash
# Activate virtual environment
source .venv/bin/activate

# Run with Daphne (ASGI server - supports WebSockets)
daphne -b 0.0.0.0 -p 8000 olx_clone.asgi:application

# Or run with Django development server (HTTP only, no WebSockets)
python manage.py runserver
```

**Note**: You MUST use Daphne (or another ASGI server) to enable WebSocket support. The standard Django `runserver` command does not support WebSockets.

### Production Mode (Optional - Redis Backend)

For production with multiple server instances, uncomment the Redis configuration in `settings.py`:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

Then install and run Redis:

```bash
# Install Redis
sudo apt-get install redis-server

# Start Redis
redis-server
```

## Testing the Chat

1. **Start the server**: `daphne -b 0.0.0.0 -p 8000 olx_clone.asgi:application`
2. **Open two browser windows/tabs**
3. **Login as different users in each**
4. **Start a conversation about a product**
5. **Send messages from both windows**
6. **Observe messages appearing instantly without refresh**

## Browser Console

Open browser console (F12) to see WebSocket connection logs:

- "WebSocket connection established" - Connection successful
- "WebSocket connection closed" - Connection lost
- Error messages if any issues occur

## Troubleshooting

### WebSocket Connection Failed

- Ensure Daphne is running (not Django runserver)
- Check browser console for error messages
- Verify firewall/proxy settings allow WebSocket connections

### Messages Not Appearing

- Check WebSocket connection status in the header
- Verify both users are in the same conversation
- Check browser console for JavaScript errors

### Connection Keeps Dropping

- May need to implement Redis backend for production
- Check server resources and network stability
- Consider adding reconnection logic

## Future Enhancements

1. **Typing Indicators**: Show when the other user is typing
2. **Read Receipts**: Show when messages are read
3. **File Sharing**: Allow sending images/documents
4. **Message Search**: Search within conversation history
5. **Message Reactions**: React to messages with emojis
6. **Voice Messages**: Record and send voice messages
7. **Online Status**: Show when users are online/offline
8. **Push Notifications**: Browser push notifications for new messages

## Technical Notes

- WebSocket URL format: `ws://domain/ws/chat/<conversation_id>/`
- Messages are JSON-encoded
- Authentication required for WebSocket connections
- Users must be conversation participants
- Channel layers handle message broadcasting
- InMemory backend suitable for single-server development
- Redis backend recommended for production with multiple servers
