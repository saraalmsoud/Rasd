import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(
    page_title="RASD",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

cred = credentials.Certificate("rasd-project.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        [data-testid="collapsedControl"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        .css-qri22k, .css-eczf16 {display: none !important;}
        [data-testid="fullscreen-button"] {display: none !important;}

        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        button[title="View fullscreen"] {
            display: none !important;
        }

        [data-testid="stSidebar"] {
            background-color: #1e1e1e;
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 40px;
        }

        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');
        * {
            font-family: 'Merriweather', serif !important;
        }
        .css-18e3th9 { background-color: #0e1117; }
        .block-container { padding-top: 30px !important; }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
        .css-1dp5vir.e1fqkh3o2 {
            border-bottom: none !important;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            width: 300px !important;
            min-width: 300px !important;
            max-width: 300px !important;
        }

        @media (max-width: 1200px) {
            [data-testid="stSidebar"] {
                width: 200px !important;
                min-width: 200px !important;
                max-width: 200px !important;
            }
        }

        @media (max-width: 900px) {
            [data-testid="stSidebar"] {
                width: 180px !important;
                min-width: 180px !important;
                max-width: 180px !important;
            }
        }

        @media (max-width: 600px) {
            [data-testid="stSidebar"] {
                width: 150px !important;
                min-width: 150px !important;
                max-width: 150px !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
    menu_title="RASD Navigation", 
    options=["Home", "Accident Reports", "Map", "Notifications"],
    icons=["house", "bar-chart", "map", "bell"],
    menu_icon="cast",
    default_index=0,
    styles={
        "container": {
            "background-color": "#1e1e1e",
            "padding": "10px",
            "border-radius": "0px",
            "border": "none",
            "box-shadow": "none",
            "border-bottom": "none",
            "border": "1px solid #1e1e1e"
        },
        "menu-title": {
            "color": "white",
            "font-size": "15px",
            "font-weight": "bold"
        },
        "icon": {
            "color": "white",
            "font-size": "18px"
        },
        "nav-link": {
            "font-size": "16px",
            "text-align": "left",
            "margin": "5px",
            "color": "white",
            "padding": "8px 10px",
            "border-radius": "8px"
        },
        "nav-link-selected": {
            "background-color": "#4B6FD6",
            "color": "white",
        }
    }
)
if selected == "Home":
    from pages import home
    home.show()

elif selected == "Accident Reports":
    from pages import analyze_accidents
    analyze_accidents.show()

elif selected == "Map":
    from pages import map
    map.show()

elif selected == "Notifications":
    from pages import notifications
    notifications.show()

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
