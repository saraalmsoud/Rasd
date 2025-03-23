import streamlit as st
import firebase_admin
from firebase_admin import firestore
import folium
from streamlit_folium import folium_static

if not firebase_admin._apps:
    from firebase_admin import credentials
    cred = credentials.Certificate("config/rasd-project.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def show():
    with st.container():
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');

                * { 
                    font-family: 'Merriweather', serif !important; 
                    color: white !important;
                }

                .stApp {
                    background-color: #2A2C30 !important;
                }

                /* Fade-in Animation */
                @keyframes fadeInSoft {
                    from {
                        opacity: 0;
                    }
                    to {
                        opacity: 1;
                    }
                }

                .title {
                    font-size: 36px !important;
                    font-weight: 700;
                    text-align: center;
                    margin-bottom: 10px;
                    animation: fadeInSoft 2s ease-in-out;
                }

                .divider {
                    width: 80%;
                    height: 3px;
                    background-color: #4B6FD6;
                    margin: auto;
                    margin-bottom: 20px;
                    border-radius: 2px;
                    animation: fadeInSoft 2s ease-in-out;
                }

                .stats {
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    animation: fadeInSoft 2s ease-in-out;
                }

                .severe { color: #ff4c4c; } 
                .minor { color: #f4b400; } 

                /* Map Animation */
                .map-box {
                    border-radius: 12px;
                    overflow: hidden;
                    border: 2px solid #4B6FD6;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
                    animation: fadeIn 1.6s ease-in-out;
                }

                /* Marker Pulse Animation */
                @keyframes pulse {
                    0% {
                        transform: scale(1);
                        box-shadow: 0 0 0 0 rgba(255, 76, 76, 0.7);
                    }
                    50% {
                        transform: scale(1.1);
                        box-shadow: 0 0 10px 5px rgba(255, 76, 76, 0.4);
                    }
                    100% {
                        transform: scale(1);
                        box-shadow: 0 0 0 0 rgba(255, 76, 76, 0.7);
                    }
                }

                .leaflet-marker-icon {
                    animation: pulse 1.5s infinite;
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
                    transition: background-color 0.3s ease-in-out, transform 0.1s ease-in-out;
                }

                button:hover {
                    background-color: #4B6FD6 !important;
                }

                button:active {
                    transform: scale(0.95);
                }

            </style>
        """, unsafe_allow_html=True)

        st.markdown("<h1 class='title'>Accident Map</h1>", unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True) 

        try:
            accidents_ref = db.collection("accidents").stream()
            accidents_data = [doc.to_dict() for doc in accidents_ref]
        except Exception as e:
            st.error(f"⚠️ Error loading accident data: {e}")
            return

        total_accidents = len(accidents_data)
        severe_accidents = sum(1 for acc in accidents_data if acc["accident_type"] == "Severe Accident")
        minor_accidents = total_accidents - severe_accidents

        st.markdown(f"""
            <div class="stats">
                <span>Total Accidents: <b>{total_accidents}</b></span> |
                <span class="severe">Severe: <b>{severe_accidents}</b></span> |
                <span class="minor">Minor: <b>{minor_accidents}</b></span>
            </div>
        """, unsafe_allow_html=True)

        map_center = [24.7136, 46.6753]
        accident_map = folium.Map(location=map_center, zoom_start=6, tiles="cartodb dark_matter")

        for accident in accidents_data:
            lat = accident["location"]["lat"]
            lon = accident["location"]["lon"]
            accident_type = accident["accident_type"]
            timestamp = accident["timestamp"][:16]
            image_url = accident["image_url"]

            color = "red" if accident_type == "Severe Accident" else "blue"

            popup_content = f"""
            <div style="width:220px; text-align:center">
                <h4 style="color: black; font-size: 16px;">{accident_type}</h4>
                <p style="color: black; font-size: 14px;">🕒 {timestamp}</p>
                <img src="{image_url}" width="100%" style="border-radius:8px; border:1px solid #ddd"/>
            </div>
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=250),
                icon=folium.Icon(color=color, icon="info-sign")
            ).add_to(accident_map)

        col1, col2, col3 = st.columns([1, 6, 1]) 
        with col2:
            st.markdown('<div class="map-box">', unsafe_allow_html=True)
            folium_static(accident_map, width=900, height=500)  
            st.markdown('</div>', unsafe_allow_html=True)
