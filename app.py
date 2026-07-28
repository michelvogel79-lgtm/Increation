import streamlit as st
from openai import OpenAI
from groq import Groq
import base64
import requests
from urllib.parse import quote

st.set_page_config(
    page_title="increation - KI Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

LOGO_NAME = "increation"

# ====== GLOBAL CSS - ALLES ABGERUNDET ======
st.markdown("""
<style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ====== TABS - GROß, ABGERUNDET & KREATIV ====== */
.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
    padding: 12px;
    background: rgba(20, 20, 35, 0.5);
    border-radius: 25px;  /* ABGERUNDET */
    backdrop-filter: blur(15px);
    border: 1px solid rgba(100, 200, 255, 0.15);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}
.stTabs [data-baseweb="tab"] {
    height: 75px;
    padding: 0 30px;
    font-size: 22px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, rgba(40, 50, 70, 0.6), rgba(25, 35, 50, 0.6));
    border-radius: 20px;  /* ABGERUNDET */
    color: #B8D4F0 !important;
    border: 1px solid rgba(100, 200, 255, 0.2);
    transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    background: linear-gradient(135deg, rgba(60, 100, 160, 0.6), rgba(40, 70, 120, 0.6));
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(74, 144, 226, 0.4);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4A90E2 0%, #2C5F8D 50%, #1E3A5F 100%) !important;
    color: #FFFFFF !important;
    border: 2px solid #6BB6FF !important;
    box-shadow: 0 10px 30px rgba(74, 144, 226, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
}

/* ====== HEADER GRADIENT ====== */
.stTabs [data-baseweb="tab-panel"] h2 {
    font-size: 40px !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #6BB6FF, #4A90E2, #2C5F8D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 25px !important;
    text-align: center;
}

/* ====== CHAT INPUT FIXIERT UNTEN - ABGERUNDET ====== */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 30px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 65% !important;
    max-width: 900px !important;
    z-index: 999 !important;
    background: linear-gradient(135deg, rgba(30, 40, 60, 0.95), rgba(20, 30, 50, 0.95)) !important;
    border: 2px solid rgba(107, 182, 255, 0.5) !important;
    border-radius: 30px !important;  /* STARK ABGERUNDET */
    padding: 10px !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 15px 50px rgba(74, 144, 226, 0.4) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: white !important;
    font-size: 16px !important;
    border: none !important;
    border-radius: 20px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #8AB4D8 !important;
}

/* ====== PADDING UNTEN ====== */
.main .block-container {
    padding-bottom: 150px !important;
}

/* ====== SPENDEN-BUTTON - ABGERUNDET ====== */
.donation-btn {
    display: inline-block;
    padding: 10px 25px;
    background: linear-gradient(135deg, #4A90E2 0%, #2C5F8D 50%, #1E3A5F 100%);
    color: #E0F0FF;
    border: 1px solid #6BB6FF;
    border-radius: 25px;  /* ABGERUNDET */
    font-weight: 700;
    font-size: 14px;
    text-decoration: none;
    box-shadow: 0 5px 20px rgba(74, 144, 226, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}
.donation-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(74, 144, 226, 0.6);
}

/* ====== KREATIVE BOXEN - ABGERUNDET ====== */
.kreativ-box {
    background: linear-gradient(135deg, rgba(30, 45, 70, 0.7), rgba(20, 30, 50, 0.7));
    border: 1px solid rgba(107, 182, 255, 0.3);
    border-radius: 25px;  /* ABGERUNDET */
    padding: 25px;
    margin: 15px 0;
    backdrop-filter: blur(15px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

/* ====== BUTTONS - ABGERUNDET ====== */
.stButton > button {
    background: linear-gradient(135deg, #4A90E2 0%, #2C5F8D 100%) !important;
    color: white !important;
    border: 1px solid #6BB6FF !important;
    border-radius: 15px !important;  /* ABGERUNDET */
    font-weight: 700 !important;
    padding: 12px 28px !important;
    transition: all 0.3s ease !important;
    font-size: 15px !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(74, 144, 226, 0.5) !important;
}

/* ====== INPUTS - ABGERUNDET ====== */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    background: rgba(20, 30, 50, 0.7) !important;
    color: white !important;
    border: 1px solid rgba(107, 182, 255, 0.3) !important;
    border-radius: 15px !important;  /* ABGERUNDET */
    padding: 12px !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #6B8AB0 !important;
}

/* ====== CHAT NACHRICHTEN - ABGERUNDET ====== */
[data-testid="stChatMessage"] {
    background: linear-gradient(135deg, rgba(30, 45, 70, 0.5), rgba(20, 30, 50, 0.5)) !important;
    border: 1px solid rgba(107, 182, 255, 0.2) !important;
    border-radius: 20px !important;  /* ABGERUNDET */
    padding: 18px !important;
    margin: 10px 0 !important;
}

/* ====== BILDER - ABGERUNDET ====== */
.stImage img {
    border-radius: 20px !important;  /* ABGERUNDET */
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

/* ====== CODE-BLÖCKE - ABGERUNDET ====== */
.stCodeBlock {
    border-radius: 15px !important;
    border: 1px solid rgba(107, 182, 255, 0.3) !important;
}

/* ====== SIDEBAR - ABGERUNDET ====== */
[data-testid="stSidebar"] {
    border-radius: 0 25px 25px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ====== HINTERGRUND-BILD ======
def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        page_bg_img = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{b64_encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.6);
            z-index: -1;
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(20, 20, 30, 0.85);
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except:
        pass

# ====== LOGO-BILD ======
def set_logo(image_file, width=200):
    try:
        with*
