import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_lottie import st_lottie
import time
from streamlit_javascript import st_javascript
import requests
import base64


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


if "user" not in st.session_state:
    import pages.auth as home_public
    home_public.show()
    st.stop()

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
                width: 230px !important;
                min-width: 230px !important;
                max-width: 230px !important;
            }
        }

        @media (max-width: 900px) {
            [data-testid="stSidebar"] {
                width: 250px !important;
                min-width: 250px !important;
                max-width: 250px !important;
            }
        }

        @media (max-width: 600px) {
            [data-testid="stSidebar"] {
                width: 250px !important;
                min-width: 250px !important;
                max-width: 250px !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

svg_logo = """
<svg width="100" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#4B6FD6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#A259FF;stop-opacity:1" />
    </linearGradient>
  </defs>
  <path d="M60 30 L160 70 Q165 75 160 80 L130 100 Q110 115 90 110 L60 100 Q55 90 60 80 Z"
        fill="url(#grad1)" />
  <circle cx="125" cy="85" r="12" fill="#1e1e1e"/>
  <circle cx="125" cy="85" r="6" fill="#A259FF"/>
  <path d="M70 110 Q65 120 70 130 L100 150 Q105 155 110 150 L140 120 Q150 110 145 95 L135 90"
        fill="url(#grad1)" />
</svg>
"""

import base64  # تأكدي إنك مستوردة base64 فوق

if "user" in st.session_state:
    with st.sidebar:

        def get_base64_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()

        img_base64 = get_base64_image("static/logo.png")  # تأكدي من المسار الصحيح

        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{img_base64}" width="120" style="margin: auto;" />
            </div>
            """,
            unsafe_allow_html=True
        )

        selected = option_menu(
            menu_title="RASD Navigation", 
            options=["Home", "Accident Reports", "Map", "Notifications", "Logout"],
            icons=["house", "bar-chart", "map", "bell", "box-arrow-right"],
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
                    "font-size": "14px",
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
    
elif selected == "Logout":
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("You have been logged out.")
    st.rerun()
        
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
