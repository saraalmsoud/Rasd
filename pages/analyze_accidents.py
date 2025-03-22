import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import firebase_admin
from firebase_admin import firestore

if not firebase_admin._apps:
    from firebase_admin import credentials
    cred = credentials.Certificate("/etc/secrets/rasd-project.json")
    firebase_admin.initialize_app(cred)


db = firestore.client()

def show():
    

    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] { 
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
        <style>
            * {
                color: white !important;
            }

            .stApp {
                background-color: #2A2C30 !important;
            }

            /* Animation for report cards */
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            /* Animation for title */
            @keyframes slideDown {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .title {
                animation: slideDown 0.8s ease-out;
            }

            .report-card {
                background-color: #1e1e1e !important;
                border-radius: 10px !important;
                padding: 12px !important;
                margin-bottom: 12px !important;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
                font-size: 14px !important;
                min-height: 350px; 
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                text-align: center;
                animation: fadeIn 0.8s ease-in-out;
                transition: transform 0.3s ease-in-out;
            }

            /* Hover effect for cards */
            .report-card:hover {
                transform: scale(1.05);
                box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.4);
            }

            .report-card h4, .report-card p, .report-card b {
                color: white !important;
            }

            .accident-image {
                width: 100%;
                height: 180px; 
                object-fit: cover;
                border-radius: 12px !important; 
            }

            div[data-baseweb="radio"] label div {
                color: white !important;
                font-size: 16px !important;
                font-weight: bold !important;
            }

            div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
                background-color: transparent !important; 
                border: 3px solid #3657C2 !important; 
                width: 20px !important; 
                height: 20px !important; 
                border-radius: 50% !important;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            div[data-baseweb="radio"] label div:first-child {
                background-color: transparent !important;
                border: 3px solid #3657C2 !important;
                width: 20px !important; 
                height: 20px !important; 
                border-radius: 50% !important;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            div[data-baseweb="radio"] input:checked + div:first-child {
                background-color: #3657C2 !important;
                border: 3px solid #4B6FD6 !important;
            }
            
            div[role="radiogroup"] input:checked + div:first-child {
                background-color: #3657C2 !important; 
                border: 3px solid #4B6FD6 !important; 
            }

            div[data-baseweb="radio"] input:checked + div {
                background-color: transparent !important;
            }/* Button styling */
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
                transition: background-color 0.3s ease-in-out, transform 0.1s ease-in-out;
            }

            button:hover {
                background-color: #4B6FD6 !important;
            }

            /* Button click effect */
            button:active {
                transform: scale(0.95);
            }

        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='title'>Accident Reports</h1>", unsafe_allow_html=True)

    filter_option = st.radio(
        "Filter by :",
        ["All", "Pending Only", "Resolved Only"],
        horizontal=True
    )

    try:
        accidents_ref = db.collection("accidents").order_by("timestamp", direction=firestore.Query.DESCENDING)
        accidents = accidents_ref.stream()

        accidents_data = []
        for doc in accidents:
            accident = doc.to_dict()
            accident["id"] = doc.id  
            print(f"📌 Loaded accident: {accident}")
            if filter_option == "Pending Only" and accident["status"] != "pending":
                continue
            if filter_option == "Resolved Only" and accident["status"] != "resolved":
                continue
            accidents_data.append(accident)

    except Exception as e:
        st.error(f"⚠️ Error loading accident data: {e}")
        accidents_data = []

    num_columns = 3  
    cols = st.columns(num_columns)

    for i, accident in enumerate(accidents_data):
        with cols[i % num_columns]:
            st.markdown(f"""
                <div class='report-card'>
                    <h4>{accident['accident_type']} - {accident['location']['city']}</h4>
                    <p><b>📍 Location:</b> {accident['location']['lat']}, {accident['location']['lon']}</p>
                    <p><b>⏳ Date:</b> {accident['timestamp'][:10]} | <b>🕒 Time:</b> {accident['timestamp'][11:19]}</p>
                    <img src="{accident['image_url']}" class="accident-image"/>
                </div>
            """, unsafe_allow_html=True)

            if accident["status"] == "pending":
                if st.button(f"Confirm Resolution", key=f"resolve_{accident['id']}"):
                    try:
                        db.collection("accidents").document(accident["id"]).update({"status": "resolved"})
                        st.success(f"Accident {accident['id']} resolved successfully.")
                    except Exception as e:
                        st.error(f"⚠️ Error updating accident status: {e}")

            elif accident["status"] == "resolved":
                st.button(f"Resolved Successfully ✔", key=f"resolved_{accident['id']}", disabled=True)

    remaining_cards = len(accidents_data) % num_columns
    if remaining_cards > 0:
        for _ in range(num_columns - remaining_cards):
            st.markdown("<div class='report-card' style='visibility: hidden;'></div>", unsafe_allow_html=True)
