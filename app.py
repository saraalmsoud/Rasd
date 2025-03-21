import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import time

# Page setup
st.set_page_config(page_title="RASD", page_icon="🚗", layout="wide")


st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;} /* يخفي القائمة العلوية */
        header {visibility: hidden;} /* يخفي الهيدر */
        footer {visibility: hidden;} /* يخفي الفوتر */
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;} /* إخفاء القائمة العلوية */
        header {visibility: hidden;} /* إخفاء الهيدر */
        footer {visibility: hidden;} /* إخفاء الفوتر */

        /* 🔹 تعديل موقع الشريط */
        div.stTabs {
            position: fixed; /* تثبيت الشريط */
            top: 0px; /* رفع الشريط للأعلى */
            left: 0;
            width: 100%;
            z-index: 1000; /* التأكد إنه فوق كل شيء */
            background-color: rgba(0, 0, 0, 0.7); /* خلفية شفافة */
            padding: 10px 0px;
        }

        /* 🔹 رفع المحتوى الرئيسي */
        .block-container {
            margin-top: -120px; /* تعديل المسافة بين الشريط والمحتوى */
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>
        /* إخفاء زر القائمة الجانبية */
        button[title="Toggle sidebar"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)



import firebase_admin
from firebase_admin import credentials

# تحميل ملف الشهادات السرية من Render Secrets
cred = credentials.Certificate("/etc/secrets/rasd-project.json")

# تهيئة Firebase
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
# Embed Firebase JavaScript in Streamlit
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
            console.log("❌ Token not found.");
          }
        }).catch((err) => {
          console.log("❌ Error fetching token:", err);
        });
      } else {
        console.log("❌ Notification permission denied.");
      }
    });
  }

  messaging.onMessage((payload) => {
    console.log("🔔 New notification received:", payload);
    alert("🚨 New Notification: " + payload.notification.title + "\\n" + payload.notification.body);
  });

  requestNotificationPermission();
</script>
""", unsafe_allow_html=True)

# Hide the sidebar in Streamlit
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# Add Merriweather font
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');
        * { font-family: 'Merriweather', serif !important; }
        .top-navbar {
            position: fixed;
            top: 0px;
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

# Get the current page from the URL
query_params = st.query_params
current_page = query_params.get("page", "home")

# Top navigation bar
st.markdown(f"""
    <div class="top-navbar">
        <a href="/?page=home" class="nav-item {'active' if current_page == 'home' else ''}">Home</a>
        <a href="/?page=reports" class="nav-item {'active' if current_page == 'reports' else ''}">Accident Reports</a>
        <a href="/?page=map" class="nav-item {'active' if current_page == 'map' else ''}">Map</a>
        <a href="/?page=notifications" class="nav-item {'active' if current_page == 'notifications' else ''}">Notifications</a>
    </div>
""", unsafe_allow_html=True)

# Display the requested page based on navigation
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
    from pages import notifications  # 🔥 New notifications page
    notifications.show()
