import streamlit as st
from groq import Groq
import base64
import requests
from urllib.parse import quote
from PIL import Image
import io
import zipfile

st.set_page_config(
    page_title="increation - KI Studio",
    page_icon="🧠",
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
def set_logo(image_file, width=200):
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

# Hintergrund
try:
    set_background("background.jpg")
except:
    pass

# Logo
try:
    set_logo("logo.png", width=200)
except:
    st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <h1 style="font-size: 80px;">🧠</h1>
            <h1>{LOGO_NAME} KI Studio</h1>
            <p style="color: #888;">Powered by Groq ⚡</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ====== TABS ======
tab1, tab2, tab3, tab4 = st.tabs(["💬 KI-Chat", "🎨 Bild-Generator", "💻 Code-Helper", "🎬 Video-Ersteller"])

# ====== TAB 1: CHAT ======
with tab1:
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
        
        chat_model = st.selectbox("🎯 Chat-Modell:", [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ], key="chat_model")
        
        st.markdown("---")
        
        if st.button("🗑️ Chat löschen", use_container_width=True, key="clear_chat"):
            st.session_state.messages = []
            st.rerun()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    prompt = st.chat_input("Stelle deine Frage...", key="chat_input")
    
    # ====== SPENDEN-BUTTON (METALLIC-BLAU) ======
    st.markdown("""
    <div style="text-align: center; margin-top: 10px;">
        <a href="https://ko-fi.com/increate" target="_blank" style="text-decoration: none;">
            <button style="padding: 6px 18px; background: linear-gradient(135deg, #4A90E2 0%, #2C5F8D 50%, #1E3A5F 100%); color: #E0F0FF; border: 1px solid #6BB6FF; border-radius: 15px; font-weight: 600; cursor: pointer; font-size: 12px; box-shadow: 0 2px 6px rgba(74, 144, 226, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3); text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);">
                ☕ Unterstützen
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("KI denkt nach..."):
                try:
                    response = client.chat.completions.create(
                        model=chat_model,
                        messages=st.session_state.messages,
                        max_tokens=1000,
                        temperature=0.7
                    )
                    answer = response.choices[0].message.content
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Fehler: {e}")

# ====== TAB 2: BILD-GENERATOR ======
with tab2:
    st.header("🎨 Bild-Generator")
    st.write("Erstelle einzigartige Bilder mit KI!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        img_prompt = st.text_area(
            "Beschreibe das Bild:",
            placeholder="z.B. Ein futuristischer Roboter in einer neon-beleuchteten Stadt",
            height=100
        )
    
    with col2:
        img_style = st.selectbox("Stil:", [
            "realistisch", "künstlerisch", "anime", "digital art", "3D render"
        ])
        img_size = st.selectbox("Größe:", [
            "1024x1024 (quadratisch)",
            "1024x768 (landscape)",
            "768x1024 (portrait)"
        ])
    
    if st.button("🎨 Bild erstellen", use_container_width=True, key="gen_img"):
        if img_prompt:
            with st.spinner("Bild wird erstellt..."):
                try:
                    full_prompt = f"{img_prompt}, {img_style}, high quality, 4k, detailed"
                    encoded_prompt = quote(full_prompt)
                    sizes = {
                        "1024x1024 (quadratisch)": "1024x1024",
                        "1024x768 (landscape)": "1024x768",
                        "768x1024 (portrait)": "768x1024"
                    }
                    size = sizes[img_size]
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={size.split('x')[0]}&height={size.split('x')[1]}&nologo=true"
                    response = requests.get(image_url, timeout=60)
                    if response.status_code == 200:
                        st.success("✅ Bild erstellt!")
                        st.image(response.content, caption=img_prompt, use_container_width=True)
                        st.download_button("💾 Bild herunterladen", response.content, f"increation.png", "image/png")
                except Exception as e:
                    st.error(f"Fehler: {e}")
        else:
            st.warning("⚠️ Bitte Beschreibung eingeben!")

# ====== TAB 3: CODE-HELPER ======
with tab3:
    st.header("💻 Code-Helper")
    col1, col2 = st.columns([2, 1])
    with col1:
        code_request = st.text_area("Was für Code?", placeholder="z.B. Python-Funktion für Primzahlen", height=100)
    with col2:
        code_language = st.selectbox("Sprache:", ["Python", "JavaScript", "HTML/CSS", "Java", "C++", "SQL"])
    
    if st.button("💻 Code generieren", use_container_width=True, key="gen_code"):
        if code_request:
            with st.spinner("Code wird geschrieben..."):
                try:
                    full_prompt = f"Schreibe {code_language} Code für: {code_request}. Nur Code mit Kommentaren."
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": full_prompt}],
                        max_tokens=1500,
                        temperature=0.3
                    )
                    code = response.choices[0].message.content
                    if "```" in code:
                        parts = code.split("```")
                        code_clean = parts[1].strip() if len(parts) >= 2 else code
                    else:
                        code_clean = code
                    st.success("✅ Code generiert!")
                    st.code(code_clean, language=code_language.lower())
                except Exception as e:
                    st.error(f"Fehler: {e}")
        else:
            st.warning("⚠️ Bitte Beschreibung eingeben!")

# ====== TAB 4: VIDEO-ERSTELLER ======
with tab4:
    st.header("🎬 Video-Ersteller")
    st.info("💡 Lade 2-10 Bilder hoch für eine coole Slideshow!")
    
    uploaded_files = st.file_uploader("Bilder hochladen", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files and len(uploaded_files) >= 2:
        duration = st.slider("Dauer pro Bild (Sek):", 1, 10, 3)
        st.write(f"📸 {len(uploaded_files)} Bilder")
        
        if st.button("🎬 Video erstellen", use_container_width=True, key="gen_video"):
            with st.spinner("Video wird erstellt..."):
                try:
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for i, uploaded_file in enumerate(uploaded_files):
                            image = Image.open(uploaded_file)
                            img_byte_arr = io.BytesIO()
                            image.save(img_byte_arr, format='PNG')
                            zip_file.writestr(f"image_{i+1}.png", img_byte_arr.getvalue())
                        zip_file.writestr("README.txt", f"Video mit {len(uploaded_files)} Bildern, je {duration}s")
                    zip_buffer.seek(0)
                    st.success("✅ Video-Paket erstellt!")
                    st.download_button("💾 Video herunterladen", zip_buffer.getvalue(), "increation_video.zip", "application/zip")
                except Exception as e:
                    st.error(f"Fehler: {e}")
    elif uploaded_files:
        st.warning("⚠️ Mindestens 2 Bilder!")
    else:
        st.info("👆 Lade Bilder hoch um zu starten!")

# Sidebar Info
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Info")
st.sidebar.info("""
**increation KI Studio**

- 💬 KI-Chat
- 🎨 Bild-Generator
- 💻 Code-Helper
- 🎬 Video-Ersteller

Powered by Groq ⚡
100% kostenlos
""")
