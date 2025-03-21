import streamlit as st

def show():
    # ✅ إخفاء جميع التنبيهات (بما في ذلك تحذير use_column_width)
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

            body, .stApp {
                background-color: #373A40;
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
                margin-top: 100px;
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
            st.image("static/cropped_animation_NEW2.gif", use_column_width=True)  
