// Push Notification Manager for StudiSwap

class PushNotificationManager {
    constructor() {
        this.isSupported = 'serviceWorker' in navigator && 'PushManager' in window;
        this.registration = null;
        this.subscription = null;
    }

    // Initialize push notifications
    async init() {
        if (!this.isSupported) {
            console.log('Push notifications are not supported');
            return false;
        }

        try {
            // Register service worker
            this.registration = await navigator.serviceWorker.register('/static/js/service-worker.js');
            console.log('Service Worker registered:', this.registration);

            // Check current subscription
            this.subscription = await this.registration.pushManager.getSubscription();

            if (this.subscription) {
                console.log('Already subscribed to push notifications');
                return true;
            }

            return true;
        } catch (error) {
            console.error('Service Worker registration failed:', error);
            return false;
        }
    }

    // Request permission and subscribe
    async subscribe() {
        if (!this.isSupported) {
            throw new Error('Push notifications are not supported');
        }

        try {
            // Request notification permission
            const permission = await Notification.requestPermission();

            if (permission !== 'granted') {
                throw new Error('Notification permission denied');
            }

            // Get VAPID public key from server
            const response = await fetch('/notifications/push/vapid-key/');
            const data = await response.json();
            const vapidPublicKey = data.public_key;

            if (!vapidPublicKey) {
                throw new Error('VAPID public key not configured on server');
            }

            // Convert VAPID key
            const convertedKey = this.urlBase64ToUint8Array(vapidPublicKey);

            // Subscribe to push notifications
            this.subscription = await this.registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: convertedKey
            });

            console.log('Subscribed to push notifications:', this.subscription);

            // Send subscription to server
            await this.sendSubscriptionToServer(this.subscription);

            return true;
        } catch (error) {
            console.error('Error subscribing to push notifications:', error);
            throw error;
        }
    }

    // Unsubscribe from push notifications
    async unsubscribe() {
        if (!this.subscription) {
            return true;
        }

        try {
            await this.subscription.unsubscribe();

            // Notify server
            await fetch('/notifications/push/unsubscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({
                    subscription: this.subscription.toJSON()
                })
            });

            this.subscription = null;
            console.log('Unsubscribed from push notifications');
            return true;
        } catch (error) {
            console.error('Error unsubscribing:', error);
            throw error;
        }
    }

    // Send subscription to server
    async sendSubscriptionToServer(subscription) {
        const browser = this.getBrowserInfo();
        const deviceName = `${browser} on ${navigator.platform}`;

        const response = await fetch('/notifications/push/subscribe/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken')
            },
            body: JSON.stringify({
                subscription: subscription.toJSON(),
                browser: browser,
                device_name: deviceName
            })
        });

        if (!response.ok) {
            throw new Error('Failed to send subscription to server');
        }

        const data = await response.json();
        console.log('Subscription sent to server:', data);
        return data;
    }

    // Helper: Convert VAPID key
    urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');

        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);

        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }

    // Helper: Get CSRF token
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Helper: Get browser info
    getBrowserInfo() {
        const ua = navigator.userAgent;
        let browser = 'Unknown';

        if (ua.indexOf('Firefox') > -1) {
            browser = 'Firefox';
        } else if (ua.indexOf('Opera') > -1 || ua.indexOf('OPR') > -1) {
            browser = 'Opera';
        } else if (ua.indexOf('Trident') > -1) {
            browser = 'Internet Explorer';
        } else if (ua.indexOf('Edge') > -1) {
            browser = 'Edge';
        } else if (ua.indexOf('Chrome') > -1) {
            browser = 'Chrome';
        } else if (ua.indexOf('Safari') > -1) {
            browser = 'Safari';
        }

        return browser;
    }

    // Check if already subscribed
    async isSubscribed() {
        if (!this.isSupported || !this.registration) {
            return false;
        }

        this.subscription = await this.registration.pushManager.getSubscription();
        return this.subscription !== null;
    }

    // Get notification permission status
    getPermissionStatus() {
        if (!this.isSupported) {
            return 'unsupported';
        }
        return Notification.permission;
    }
}

// Create global instance
window.pushNotificationManager = new PushNotificationManager();

// Auto-initialize and prompt for notifications on login
document.addEventListener('DOMContentLoaded', async function () {
    // Check if user is authenticated
    const isAuthenticated = document.querySelector('meta[name="user-authenticated"]')?.content === 'true';

    if (isAuthenticated) {
        await window.pushNotificationManager.init();

        // Check if we should prompt for notifications
        const permission = window.pushNotificationManager.getPermissionStatus();
        const isSubscribed = await window.pushNotificationManager.isSubscribed();

        // Only prompt if permission hasn't been asked yet and not already subscribed
        if (permission === 'default' && !isSubscribed) {
            // Small delay to not overwhelm user immediately on page load
            setTimeout(async () => {
                try {
                    await window.pushNotificationManager.subscribe();
                    console.log('Successfully subscribed to push notifications');
                } catch (error) {
                    // User denied or error occurred - fail silently
                    console.log('Push notification subscription skipped:', error.message);
                }
            }, 2000); // Wait 2 seconds after page load
        }
    }
});
