import streamlit as st
from groq import Groq
import base64

st.set_page_config(
    page_title="increation - KI Studio",
    page_icon="🧠",  # Browser-Tab Icon
    layout="wide"
)

LOGO_NAME = "increation"

# ====== HINTERGRUND-BILD ======
def set_background(image_file):
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

# ====== LOGO-BILD ======
def set_logo(image_file, width=150):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    logo_html = f"""
    <div style="text-align: center; padding: 20px;">
        <img src="data:image/png;base64,{b64_encoded}" width="{width}" style="border-radius: 20px; box-shadow: 0 0 30px rgba(100, 200, 255, 0.5);">
        <h1 style="margin-top: 20px; color: white;">{LOGO_NAME} KI Studio</h1>
        <p style="color: #ccc; font-size: 18px;">Powered by Groq ⚡</p>
    </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)

# Hintergrund setzen
try:
    set_background("background.jpg")
except Exception as e:
    st.warning(f"⚠️ Hintergrundbild konnte nicht geladen werden")

# Logo setzen
try:
    set_logo("logo.png", width=200)
except Exception as e:
    st.warning(f"⚠️ Logo konnte nicht geladen werden - Emoji wird verwendet")
    st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <h1 style="font-size: 80px;">🧠</h1>
            <h1 style="margin-top: -20px;">{LOGO_NAME} KI Studio</h1>
            <p style="color: #888; font-size: 18px;">Powered by Groq ⚡</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

st.header("💬 KI-Chat")

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("Bitte GROQ_API_KEY in Streamlit Secrets setzen!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

with st.sidebar:
    try:
        with open("logo.png", "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        st.markdown(f"""
            <div style="text-align: center; padding: 10px;">
                <img src="data:image/png;base64,{b64_encoded}" width="100" style="border-radius: 15px;">
                <h3 style="margin-top: 10px;">{LOGO_NAME}</h3>
            </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown(f"### 🧠 {LOGO_NAME}")
    
    st.markdown("---")
    
    model_choice = st.selectbox("🎯 Modell:", [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ])
    
    st.markdown("---")
    
    if st.button("🗑️ Chat löschen", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("### ℹ️ Info")
    st.info("**increation KI Studio** - Powered by Groq")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Stelle deine Frage...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("KI denkt nach..."):
            try:
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=st.session_state.messages,
                    max_tokens=1000,
                    temperature=0.7
                )
                answer = response.choices[0].message.content
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Fehler: {e}")
