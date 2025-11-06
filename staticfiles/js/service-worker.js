// Service Worker for handling push notifications

self.addEventListener('install', function (event) {
    console.log('Service Worker installing.');
    self.skipWaiting();
});

self.addEventListener('activate', function (event) {
    console.log('Service Worker activated.');
    event.waitUntil(clients.claim());
});

// Handle push notification
self.addEventListener('push', function (event) {
    console.log('Push notification received:', event);

    let notificationData = {
        title: 'New Notification',
        body: 'You have a new notification',
        icon: '/static/icons/favicon.png',
        badge: '/static/icons/favicon.png',
        data: {
            url: '/'
        }
    };

    if (event.data) {
        try {
            const data = event.data.json();
            notificationData = {
                title: data.title || notificationData.title,
                body: data.body || data.message || notificationData.body,
                icon: data.icon || notificationData.icon,
                badge: data.badge || notificationData.badge,
                data: {
                    url: data.url || data.action_url || '/',
                    notification_id: data.notification_id
                },
                tag: data.tag || 'studiswap-notification',
                requireInteraction: data.requireInteraction || false,
                vibrate: [200, 100, 200]
            };
        } catch (e) {
            console.error('Error parsing push data:', e);
        }
    }

    event.waitUntil(
        self.registration.showNotification(notificationData.title, {
            body: notificationData.body,
            icon: notificationData.icon,
            badge: notificationData.badge,
            data: notificationData.data,
            tag: notificationData.tag,
            requireInteraction: notificationData.requireInteraction,
            vibrate: notificationData.vibrate,
            actions: [
                {
                    action: 'open',
                    title: 'Open'
                },
                {
                    action: 'close',
                    title: 'Close'
                }
            ]
        })
    );
});

// Handle notification click
self.addEventListener('notificationclick', function (event) {
    console.log('Notification clicked:', event);

    event.notification.close();

    if (event.action === 'close') {
        return;
    }

    // Open the URL associated with the notification
    const urlToOpen = event.notification.data.url || '/';

    event.waitUntil(
        clients.matchAll({
            type: 'window',
            includeUncontrolled: true
        }).then(function (clientList) {
            // Check if there's already a window open
            for (let i = 0; i < clientList.length; i++) {
                const client = clientList[i];
                if (client.url === urlToOpen && 'focus' in client) {
                    return client.focus();
                }
            }
            // If no window is open, open a new one
            if (clients.openWindow) {
                return clients.openWindow(urlToOpen);
            }
        })
    );
});

// Handle notification close
self.addEventListener('notificationclose', function (event) {
    console.log('Notification closed:', event);
});
