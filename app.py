import streamlit as st
from groq import Groq
import base64
import requests
from urllib.parse import quote

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

# ====== TABS FÜR VERSCHIEDENE FUNKTIONEN ======
tab1, tab2, tab3 = st.tabs(["💬 KI-Chat", "🎨 Bild-Generator", "💻 Code-Helper"])

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
    st.write("Erstelle einzigartige Bilder mit KI - komplett kostenlos!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        img_prompt = st.text_area(
            "Beschreibe das Bild:",
            placeholder="z.B. Ein futuristischer Roboter in einer neon-beleuchteten Stadt, 4k, detailliert",
            height=100
        )
    
    with col2:
        img_style = st.selectbox("Stil:", [
            "realistisch",
            "künstlerisch",
            "anime",
            "digital art",
            "3D render",
            "pixel art"
        ])
        
        img_size = st.selectbox("Größe:", [
            "1024x1024 (quadratisch)",
            "1024x768 (landscape)",
            "768x1024 (portrait)"
        ])
    
    if st.button("🎨 Bild erstellen", use_container_width=True):
        if img_prompt:
            with st.spinner("Bild wird erstellt... (kann 10-30 Sekunden dauern)"):
                try:
                    # Pollinations.ai - kostenlos, kein Key nötig!
                    full_prompt = f"{img_prompt}, {img_style}, high quality, 4k, detailed"
                    encoded_prompt = quote(full_prompt)
                    
                    # Größen mapping
                    sizes = {
                        "1024x1024 (quadratisch)": "1024x1024",
                        "1024x768 (landscape)": "1024x768",
                        "768x1024 (portrait)": "768x1024"
                    }
                    size = sizes[img_size]
                    
                    # URL zusammenbauen
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={size.split('x')[0]}&height={size.split('x')[1]}&nologo=true"
                    
                    # Bild herunterladen
                    response = requests.get(image_url, timeout=60)
                    
                    if response.status_code == 200:
                        st.success("✅ Bild erfolgreich erstellt!")
                        st.image(response.content, caption=img_prompt, use_container_width=True)
                        
                        # Download-Button
                        st.download_button(
                            label="💾 Bild herunterladen",
                            data=response.content,
                            file_name=f"increation_{img_prompt[:20]}.png",
                            mime="image/png"
                        )
                    else:
                        st.error("❌ Bild konnte nicht erstellt werden. Versuche es erneut!")
                except Exception as e:
                    st.error(f"Fehler: {e}")
        else:
            st.warning("⚠️ Bitte gib eine Beschreibung ein!")

# ====== TAB 3: CODE-HELPER ======
with tab3:
    st.header("💻 Code-Helper")
    st.write("Lass die KI Code für dich schreiben!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        code_request = st.text_area(
            "Was für Code brauchst du?",
            placeholder="z.B. Eine Python-Funktion, die Primzahlen berechnet",
            height=100
        )
    
    with col2:
        code_language = st.selectbox("Programmiersprache:", [
            "Python",
            "JavaScript",
            "HTML/CSS",
            "Java",
            "C++",
            "SQL"
        ])
    
    if st.button("💻 Code generieren", use_container_width=True):
        if code_request:
            with st.spinner("Code wird geschrieben..."):
                try:
                    full_prompt = f"Schreibe {code_language} Code für: {code_request}. Gib nur den Code aus, mit Kommentaren erklärt."
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": full_prompt}],
                        max_tokens=1500,
                        temperature=0.3
                    )
                    
                    code = response.choices[0].message.content
                    
                    # Code aus Markdown extrahieren falls ``` vorhanden
                    if "```" in code:
                        parts = code.split("```")
                        if len(parts) >= 2:
                            code_clean = parts[1].strip()
                            # Sprache entfernen falls am Anfang
                            if code_clean.startswith(code_language.lower()):
                                code_clean = code_clean[len(code_language):].strip()
                    else:
                        code_clean = code
                    
                    st.success("✅ Code generiert!")
                    st.code(code_clean, language=code_language.lower())
                    
                    # Download-Button
                    extensions = {
                        "Python": "py",
                        "JavaScript": "js",
                        "HTML/CSS": "html",
                        "Java": "java",
                        "C++": "cpp",
                        "SQL": "sql"
                    }
                    st.download_button(
                        label="💾 Code herunterladen",
                        data=code_clean,
                        file_name=f"code.{extensions[code_language]}",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Fehler: {e}")
        else:
            st.warning("⚠️ Bitte beschreibe was du brauchst!")

# Sidebar Info
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Info")
st.sidebar.info("""
**increation KI Studio**

Features:
- 💬 KI-Chat
- 🎨 Bild-Generator
- 💻 Code-Helper

Powered by Groq ⚡
100% kostenlos
""")
