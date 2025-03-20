const messaging = firebase.messaging();

Notification.requestPermission().then(permission => {
    if (permission === "granted") {
        console.log("🔔 إشعارات مفعلة!");
        getToken(messaging, { vapidKey: "BBP1Ua121e6icCNjO9o-6QaU_8_E997gWQVpfkpHZkJgHW9m3wRHsJ6Oqc-rh_YNn5QImYwZ6FWo8zUpaXPXlbc" })
        .then(token => {
            if (token) {
            console.log("📲 توكن FCM:", token);
        }
        })
        .catch(err => console.error("❌ خطأ في جلب التوكن:", err));
    } else {
        console.log("❌ تم رفض الإشعارات");
    }
});

onMessage(messaging, payload => {
    console.log("📩 تم استقبال إشعار:", payload);
    new Notification(payload.notification.title, {
        body: payload.notification.body,
        icon: "/static/notification-icon.png"
    });
});

navigator.serviceWorker.register("/script/firebase-messaging-sw.js")
  .then((registration) => {
    console.log("✅ Service Worker مسجل بنجاح:", registration);
    messaging.useServiceWorker(registration);
  }).catch((err) => {
    console.error("❌ خطأ في تسجيل Service Worker:", err);
  });