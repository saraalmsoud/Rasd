import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("config/rasd-project.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

@st.cache_data(ttl=600)
def get_notifications():
    try:
        notifications_ref = db.collection("notifications").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(5)
        notifications = notifications_ref.stream()

        notifications_list = []
        for doc in notifications:
            notification = doc.to_dict()
            notification["id"] = doc.id
            notifications_list.append(notification)

        return notifications_list
    except Exception as e:
        st.error(f"⚠️ Error loading notifications: {e}")
        return []

def show():
    # نحط الصفحة الحالية في session لتجنب التداخل
    st.session_state["selected_page"] = "Notifications"

    # CSS Styling
    st.markdown("""
        <style>
            .stApp {
                background-color: #2A2C30 !important;
            }

            .notification-card {
                background-color: #1e1e1e;
                padding: 15px;
                margin-bottom: 12px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(255, 204, 66, 0.3);
                border-left: 5px solid #FCF596;
                opacity: 0;
                transform: translateY(10px);
                animation: fadeInMove 0.5s ease-out forwards;
            }

            .notification-card:hover {
                transform: translateY(-3px);
                box-shadow: 0px 6px 12px rgba(255, 204, 66, 0.5);
            }

            .notification-title {
                color: #FCF596;
                font-size: 20px;
                font-weight: bold;
            }

            .notification-time {
                color: #CCCCCC;
                font-size: 14px;
            }

            @keyframes fadeInMove {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            button {
                background-color: #3657C2 !important;
                color: white !important;
                font-size: 14px !important;
                font-weight: bold !important;
                padding: 8px 15px !important;
                border-radius: 25px !important;
                border: none !important;
                cursor: pointer !important;
                width: 100% !important;
                margin-top: 10px;
            }

            button:hover {
                background-color: #4B6FD6 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #FDFAF6;'>Latest Notifications ⚠️</h1>", unsafe_allow_html=True)

    notifications_list = get_notifications()

    for notification in notifications_list:
        st.markdown(f"""
            <div class="notification-card">
                <div class="notification-title">📢 {notification['message']}</div>
                <div class="notification-time">🕒 {notification['timestamp'][:19]}</div>
            </div>
        """, unsafe_allow_html=True)
