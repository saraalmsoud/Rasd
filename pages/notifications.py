import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import time

# Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("config/rasd-project.json")

db = firestore.client()

# Cache notifications to reduce API calls
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
    # CSS Styling
    st.markdown("""
        <style>
            .stApp {
                background-color: #373A40 !important;
            }

            /* Notification card with smooth fade-in */
            .notification-card {
                background-color: #222831;
                padding: 15px;
                margin-bottom: 12px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(255, 204, 66, 0.3); /* Glow effect */
                border-left: 5px solid #FCF596;
                opacity: 0;
                transform: translateY(10px);
                animation: fadeInMove 0.5s ease-out forwards;
                transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            }

            /* Hover effect (simple elevation) */
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

            /* Smooth fade-in animation */
            @keyframes fadeInMove {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #FDFAF6;'>Latest Notifications ⚠️</h1>", unsafe_allow_html=True)

    notification_container = st.container()

    # Get latest notifications
    notifications_list = get_notifications()

    with notification_container:
        for notification in notifications_list:
            st.markdown(f"""
                <div class="notification-card">
                    <div class="notification-title">📢 {notification['message']}</div>
                    <div class="notification-time">🕒 {notification['timestamp'][:19]}</div>
                </div>
            """, unsafe_allow_html=True)

    # Schedule update every 10 minutes
    time.sleep(600)
    st.rerun()