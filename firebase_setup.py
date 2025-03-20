import firebase_admin
from firebase_admin import credentials, firestore, messaging

# تحميل مفاتيح Firebase
cred = credentials.Certificate("config/rasd-project.json")
firebase_admin.initialize_app(cred)

# الاتصال بقاعدة البيانات Firestore
db = firestore.client()

# ✅ دالة إرسال الإشعار عبر Firebase Cloud Messaging
def send_notification(title, body):
    print("📢 محاولة إرسال إشعار...")
    print(f"🔹 العنوان: {title}")
    print(f"🔹 الرسالة: {body}")
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        topic="accidents"  # اسم التوبيك اللي بتستخدمه للمشتركين
    )
    response = messaging.send(message)
    print("✅ تم إرسال الإشعار:", response)

# ✅ متابعة إضافات جديدة في Firestore
def watch_accidents():
    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == "ADDED":
                data = change.document.to_dict()
                title = "🚨 حادث جديد!"
                body = f"📍 الموقع: {data.get('location', 'غير محدد')}"
                send_notification(title, body)  # إرسال الإشعار

    accidents_ref = db.collection("accidents")
    accidents_ref.on_snapshot(on_snapshot)  # تشغيل المراقبة

# ✅ تشغيل المراقبة عند تشغيل السكريبت
watch_accidents()
print("👀 مراقبة Firestore تعمل الآن...")