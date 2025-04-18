import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json
import os

firebaseConfig = {
    "apiKey": os.environ.get("apiKey"),
    "authDomain": os.environ.get("authDomain"),
    "databaseURL": os.environ.get("databaseURL"),
    "projectId": os.environ.get("projectId"),
    "storageBucket": os.environ.get("storageBucket"),
    "messagingSenderId": os.environ.get("messagingSenderId"),
    "appId": os.environ.get("appId"),
    "measurementId": os.environ.get("measurementId")
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

if not firebase_admin._apps:
    cred = credentials.Certificate("config/rasd-project.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def show():
 
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');

    [data-testid="stSidebar"], #MainMenu, header, footer {
        display: none !important;
        visibility: hidden !important;
    }
    
    label, .css-1cpxqw2 {
        color: white !important;
    }
    
    .stApp, body {
    font-family: 'Poppins', sans-serif !important;
}

    .stApp, body, .css-18ni7ap, .css-1d391kg {
        background-color: #2A2C30 !important;
        color: white !important;
        font-family: 'Merriweather', serif;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .custom-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        color: #3657C2;
        text-shadow: 0 0 2px white, 0 0 2px white;
        margin-top: 3rem;
        animation: fadeIn 1.2s ease-out;
    }
    
    
    
    .stButton > button {
        background-color: #3657C2 !important;
        color: black !important;  
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 10px 24px !important;
        border: none !important;
        border-radius: 30px !important;
        width: 100% !important;
        margin-top: 10px !important;
        transition: background-color 0.3s ease-in-out, transform 0.1s ease-in-out;
    }

    .stButton > button:hover {
        background-color: #4B6FD6 !important;
        transform: scale(1.02);
    }
    
    
    input[type="password"]::-webkit-clear-button,
    input[type="password"]::-webkit-inner-spin-button,
    input[type="password"]::-webkit-credentials-auto-fill-button {
        -webkit-appearance: none !important;
        appearance: none !important;
        filter: brightness(0.7) invert(1) !important;
        background-color: #2f2f2f !important;
        border-radius: 8px !important;
        padding: 5px !important;
        margin-right: 5px !important;
    }
    
    
    
    input[type="password"]::-webkit-clear-button,
    input[type="password"]::-webkit-inner-spin-button,
    input[type="password"]::-webkit-credentials-auto-fill-button {
        display: none !important;
    }
    
    
        input::-ms-reveal,
        input::-ms-clear {
            display: none !important;
        }

        input[type="password"]::-webkit-credentials-auto-fill-button,
        input[type="password"]::-webkit-inner-spin-button,
        input[type="password"]::-webkit-clear-button {
            filter: invert(100%);
            background-color: #2f2f2f;
            border-radius: 8px;
        }
    

    .custom-subtitle {
        font-size: 18px;
        text-align: center;
        color: #CCCCCC;
        margin-bottom: 2.5rem;
        font-weight: 300;
        animation: fadeIn 1.6s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

    st.markdown("<div class='custom-title'>Access the RASD Platform</div>", unsafe_allow_html=True)
    st.markdown("<div class='custom-subtitle'>Login or create an account to explore real-time accident detection and analysis.</div>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    input[type="text"], input[type="password"] {
        background-color: #2f2f2f !important; 
        color: white !important;
        border: 1px solid #4B6FD6 !important;
        border-radius: 8px !important;
        padding: 10px;
    }
    

    button:hover {
    background-color: #4B6FD6 !important;
    }
    
    .css-1cpxqw2 {
        color: white !important;
    }

    .stTextInput > div > div > input {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

    st.subheader("Login to your account")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            try:
                user = auth.sign_in_with_email_and_password(email, password)

                user_ref = db.collection("users").document(email)
                if not user_ref.get().exists:
                    user_ref.set({
                        "email": email,
                        "role": "admin" if email == "admin@rasd.com" else "user",
                        "created_at": datetime.now().isoformat()
                    })

                user_data = user_ref.get().to_dict()

                st.session_state["user"] = email
                st.session_state["is_admin"] = (user_data.get("role") == "admin")
                st.session_state["role"] = user_data.get("role", "user")
                st.session_state["selected_page"] = "Home"

                st.stop()

            except Exception:
                st.warning("Login failed. Please check your credentials.")

    st.markdown("---")
    st.subheader("Don't have an account? Create one")

    with st.form("signup_form"):
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        create = st.form_submit_button("Create Account")

        if create:
            if new_password != confirm_password:
                st.warning("Passwords do not match.")
            elif len(new_password) < 6:
                st.warning("Password must be at least 6 characters.")
            else:
                try:
                    auth.create_user_with_email_and_password(new_email, new_password)

                    db.collection("users").document(new_email).set({
                        "email": new_email,
                        "role": "user",
                        "created_at": datetime.now().isoformat()
                    })

                    st.success("Account created successfully. You can now log in.")

                except:
                    st.warning("Please check your email and password, or try again later.")
