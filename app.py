import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import time

# ✅ إعداد الصفحة
st.set_page_config(page_title="RASD", page_icon="🚗", layout="wide")

# ✅ تحميل بيانات Firebase إذا لم تكن مُحمّلة بالفعل
if not firebase_admin._apps:
    cred = credentials.Certificate("config/rasd-project.json")  # تأكد أن المسار صحيح
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✅ تضمين Firebase JavaScript في Streamlit
st.markdown("""
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-messaging.js"></script>

<script>
  function requestNotificationPermission() {
    Notification.requestPermission().then((permission) => {
      if (permission === "granted") {
        messaging.getToken().then((currentToken) => {
          if (currentToken) {
            console.log("🔔 FCM Token:", currentToken);
          } else {
            console.log("❌ لم يتم العثور على توكن.");
          }
        }).catch((err) => {
          console.log("❌ خطأ في جلب التوكن:", err);
        });
      } else {
        console.log("❌ تم رفض الإذن بالإشعارات.");
      }
    });
  }

  messaging.onMessage((payload) => {
    console.log("🔔 إشعار جديد وصل:", payload);
    alert("🚨 إشعار جديد: " + payload.notification.title + "\\n" + payload.notification.body);
  });

  requestNotificationPermission();
</script>
""", unsafe_allow_html=True)

# ✅ إخفاء الشريط الجانبي في Streamlit
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ✅ إضافة خط Merriweather
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');
        * { font-family: 'Merriweather', serif !important; }
        .top-navbar {
            position: fixed;
            top: 60px;
            left: 0%;
            width: 100%;
            min-height: 55px;
            background: rgba(34, 34, 34, 0.85);
            backdrop-filter: blur(10px);
            display: flex;
            justify-content: left;
            align-items: center;
            padding: 12px 40px;
            z-index: 1000;
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        }
        .nav-item {
            margin: 0 15px;
            font-size: 18px;
            font-weight: bold;
            color: white !important;
            text-decoration: none !important;
            padding: 4px 10px;
            border-radius: 30px;
            transition: all 0.3s ease-in-out;
            background-color: transparent;
            border: 2px solid transparent;
        }
        .nav-item:hover {
            background-color: #4B6FD6;
            color: white !important;
        }
        .nav-item.active {
            background-color: #3657C2;
            color: white !important;
            padding: 2px 20px;
        }
        .stApp { padding-top: 100px !important; }
    </style>
""", unsafe_allow_html=True)

# ✅ جلب الصفحة الحالية من الرابط
query_params = st.query_params
current_page = query_params.get("page", "home")

# ✅ شريط التنقل العلوي
st.markdown(f"""
    <div class="top-navbar">
        <a href="/?page=home" class="nav-item {'active' if current_page == 'home' else ''}">Home</a>
        <a href="/?page=reports" class="nav-item {'active' if current_page == 'reports' else ''}">Accident Reports</a>
        <a href="/?page=map" class="nav-item {'active' if current_page == 'map' else ''}">Map</a>
        <a href="/?page=notifications" class="nav-item {'active' if current_page == 'notifications' else ''}">Notifications</a>
    </div>
""", unsafe_allow_html=True)

# ✅ عرض الصفحة المطلوبة بناءً على التنقل
if current_page == "home":
    from pages import home
    home.show()
elif current_page == "reports":
    from pages import analyze_accidents
    analyze_accidents.show()
elif current_page == "map":
    from pages import map
    map.show()
elif current_page == "notifications":
    from pages import notifications  # 🔥 صفحة الإشعارات الجديدة
    notifications.show()