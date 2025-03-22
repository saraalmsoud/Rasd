import streamlit as st
import streamlit.components.v1 as components
import base64

def show():
    
    def get_gif_base64(file_path):
        with open(file_path, "rb") as gif_file:
            return base64.b64encode(gif_file.read()).decode("utf-8")
    
    st.markdown("""
    <style>
        button[title="View fullscreen"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)
    st.markdown("""
        <style>
            [data-testid="stNotification"], .stNotification, .stAlert {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&display=swap');

            @keyframes slideInLeft {
                0% {
                    opacity: 0;
                    transform: translateX(-50px);
                }
                100% {
                    opacity: 1;
                    transform: translateX(0);
                }
            }

            @keyframes slideInRight {
                0% {
                    opacity: 0;
                    transform: translateX(50px);
                }
                100% {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            
            
            @keyframes slideFromRight {
                0% {
                    opacity: 0;
                    transform: translateX(50px);
                }
                100% {
                    opacity: 1;
                    transform: translateX(0);
                }
            }

            .gif-entrance img {
                animation: slideFromRight 1.2s ease-out;
            }
  

            body, .stApp {
                background-color: #2A2C30;
                color: white;
                font-family: 'Merriweather', serif !important;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .container {
                display: flex;
                align-items: center;
                justify-content: space-between;
                text-align: left;
                width: 90%;
                max-width: 1200px;
                margin: auto;
                padding: 40px 20px;
            }

            .text-section {
                flex: 1;
                padding-left: 50px;
                margin-top: 0px;
                animation: slideInLeft 1.2s ease-out;
            }

            .main-title {
                font-size: 42px;
                font-weight: 700;
                text-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);
                -webkit-text-stroke: 0.3px white;
                margin-bottom: 20px;
            }

            .purple-text {
                color: #3657C2;
            }

            .white-text {
                color: white;
            }

            .description {
                color: #cccccc;
                font-size: 20px;
                max-width: 600px;
                line-height: 1.8;
                margin-bottom: 20px;
            }

            .gif-container {
                flex: 1;
                text-align: center;
                display: flex;
                justify-content: flex-end;
                align-items: flex-start;
            }

            .stImage img {
                animation: slideInRight 1.2s ease-out;
                border-radius: 10px;
                opacity: 0.9;
                margin-top: -30px;
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
    
    st.markdown("""
    <style>
        div[data-testid="stImage"] button {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("""
            <div class='text-section'>
                <h1 class='main-title'><span class='purple-text'>RASD</span> <span class='white-text'>: Smarter Roads, Safer Lives.</span></h1>
                <p class='description'>
                    AI-powered accident detection system analyzing crash severity <br>  
                    and providing real-time alerts to emergency services.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        with st.container():
            gif_path = "static/animation_new.gif"
            gif_base64 = get_gif_base64(gif_path)

            gif_html = f'''
                <div style="display: flex; justify-content: center;">
                    <img src="data:image/gif;base64,{gif_base64}" class="slide-in-gif" alt="Animated GIF" style="width: 100%; border-radius: 12px;" />
                </div>
            '''

            components.html(gif_html + """
                <style>
                    @keyframes slideFromRight {
                        0% {
                            opacity: 0;
                            transform: translateX(60px);
                        }
                        100% {
                            opacity: 1;
                            transform: translateX(0);
                        }
                    }

                    .slide-in-gif {
                        animation: slideFromRight 1.2s ease-out;
                    }
                </style>
            """, height=400)
