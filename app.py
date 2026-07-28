import streamlit as st
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

# ====== GLOBAL CSS ======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
    padding: 12px;
    background: rgba(20, 20, 35, 0.5);
    border-radius: 25px;
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
    border-radius: 20px;
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
    border-radius: 30px !important;
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

.main .block-container {
    padding-bottom: 150px !important;
}

.donation-btn {
    display: inline-block;
    padding: 10px 25px;
    background: linear-gradient(135deg, #4A90E2 0%, #2C5F8D 50%, #1E3A5F 100%);
    color: #E0F0FF;
    border: 1px solid #6BB6FF;
    border-radius: 25px;
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

.kreativ-box {
    background: linear-gradient(135deg, rgba(30, 45, 70, 0.7), rgba(20, 30, 50, 0.7));
    border: 1px solid rgba(107, 182, 255, 0.3);
    border-radius: 25px;
    padding: 25px;
    margin: 15px 0;
    backdrop-filter: blur(15px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.stButton > button {
    background: linear-gradient(135deg, #4A90E2 0%, #2C5F8D 100%) !important;
    color: white !important;
    border: 1px solid #6BB6FF !important;
    border-radius: 15px !important;
    font-weight: 700 !important;
    padding: 12px 28px !important;
    transition: all 0.3s ease !important;
    font-size: 15px !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(74, 144, 226, 0.5) !important;
}

.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    background: rgba(20, 30, 50, 0.7) !important;
    color: white !important;
    border: 1px solid rgba(107, 182, 255, 0.3) !important;
    border-radius: 15px !important;
    padding: 12px !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #6B8AB0 !important;
}

[data-testid="stChatMessage"] {
    background: linear-gradient(135deg, rgba(30, 45, 70, 0.5), rgba(20, 30, 50, 0.5)) !important;
    border: 1px solid rgba(107, 182, 255, 0.2) !important;
    border-radius: 20px !important;
    padding: 18px !important;
    margin: 10px 0 !important;
}

.stImage img {
    border-radius: 20px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.stCodeBlock {
    border-radius: 15px !important;
    border: 1px solid rgba(107, 182, 255, 0.3) !important;
}

[data-testid="stSidebar"] {
    border-radius: 0 25px 25px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ====== HINTERGRUND ======
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

# ====== LOGO ======
def set_logo(image_file, width=200):
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        logo_html = f"""
        <div style="text-align: center; padding: 20px;">
            <img src="data:image/png;base64,{b64_encoded}" width="{width}" style="border-radius: 25px; box-shadow: 0 0 30px rgba(100, 200, 255, 0.5);">
            <h1 style="margin-top: 20px; color: white; font-size: 36px;">{LOGO_NAME} KI Studio</h1>
            <p style="color: #6BB6FF; font-size: 16px; font-weight: 600;">⚡ Powered by Groq</p>
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
    except:
        st.markdown(f"""
            <div style="text-align: center; padding: 20px;">
                <h1 style="font-size: 80px;">🧠</h1>
                <h1 style="color: white;">{LOGO_NAME} KI Studio</h1>
                <p style="color: #6BB6FF; font-weight: 600;">⚡ Powered by Groq</p>
            </div>
        """, unsafe_allow_html=True)

# Hintergrund & Logo
set_background("background.jpg")
set_logo("logo.png", width=200)

st.divider()

# ====== TABS ======
tab1, tab2, tab3 = st.tabs(["💬  KI-CHAT", "🎨  BILD-GENERATOR", "💻  CODE-HELPER"])

# ====== TAB 1: CHAT ======
with tab1:
    st.markdown("## 💬 KI-Chat – Dein intelligenter Gesprächspartner")
    
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except:
        st.error("🔑 Bitte GROQ_API_KEY in Streamlit Secrets setzen!")
        st.stop()
    
    client = Groq(api_key=GROQ_API_KEY)
    
    with st.sidebar:
        try:
            with open("logo.png", "rb") as f:
                img_data = f.read()
            b64_encoded = base64.b64encode(img_data).decode()
            st.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <img src="data:image/png;base64,{b64_encoded}" width="100" style="border-radius: 20px;">
                    <h3 style="margin-top: 10px; color: #6BB6FF;">{LOGO_NAME}</h3>
                </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown(f"### 🧠 {LOGO_NAME}")
        
        st.markdown("---")
        st.markdown("### ⚙️ Chat-Einstellungen")
        
        chat_model = st.selectbox("🎯 Modell wählen:", [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "gemma2-9b-it",
            "mixtral-8x7b-32768"
        ], key="chat_model")
        
        ausfuehrlichkeit = st.selectbox("📝 Antwort-Stil:", [
            "✨ Kurz & knackig",
            "📄 Normal",
            "📚 Sehr ausführlich"
        ], key="ausfuehrlichkeit", index=2)
        
        max_tokens_setting = st.slider("🔢 Max. Tokens:", 1000, 8000, 4000, 500)
        
        st.markdown("---")
        
        if st.button("🗑️  Chat zurücksetzen", use_container_width=True, key="clear_chat"):
            st.session_state.messages = []
            st.rerun()
    
    system_prompts = {
        "✨ Kurz & knackig": "Du bist ein hilfreicher Assistent. Antworte kurz, präzise und auf den Punkt. Maximal 3-4 Sätze.",
        "📄 Normal": "Du bist ein hilfreicher Assistent. Antworte freundlich und informativ mit den wichtigsten Informationen.",
        "📚 Sehr ausführlich": "Du bist ein extrem hilfreicher und kompetenter Assistent. Antworte immer sehr ausführlich und detailliert. Verwende Überschriften, Listen, Beispiele und Hintergrundinformationen. Strukturiere deine Antwort professionell."
    }
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div class="kreativ-box" style="text-align: center;">
                <h3 style="color: #6BB6FF; margin-bottom: 15px;">👋 Willkommen im KI-Chat!</h3>
                <p style="color: #B8D4F0; font-size: 16px;">
                Stell mir Fragen zu jedem Thema!<br>
                <strong>Tipp:</strong> Wähle in der Sidebar ein Modell und die gewünschte Ausführlichkeit.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    prompt = st.chat_input("💭 Stelle deine Frage...", key="chat_input")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <a href="https://ko-fi.com/increate" target="_blank" class="donation-btn">
            ☕ Unterstützen
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 KI denkt nach..."):
                try:
                    response = client.chat.completions.create(
                        model=chat_model,
                        messages=[
                            {"role": "system", "content": system_prompts[ausfuehrlichkeit]},
                            *st.session_state.messages
                        ],
                        max_tokens=max_tokens_setting,
                        temperature=0.7
                    )
                    answer = response.choices[0].message.content
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"❌ Fehler: {e}")

# ====== TAB 2: BILD-GENERATOR (POLLINATIONS) ======
with tab2:
    st.markdown("## 🎨 Bild-Generator – Erschaffe deine Visionen")
    
    st.markdown("""
    <div class="kreativ-box">
        <p style="color: #B8D4F0; margin: 0; text-align: center; font-size: 16px;">
        🎨 Beschreibe dein Wunschbild so detailliert wie möglich. Kostenlos & ohne Anmeldung!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Bildbeschreibung")
        img_prompt = st.text_area(
            " ",
            placeholder="z.B. Ein majestätischer Drache über einer mittelalterlichen Stadt bei Sonnenuntergang",
            height=120,
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("### 🎭 Stil & Größe")
        img_style = st.selectbox("🎨 Stil:", [
            "realistisch", "künstlerisch", "anime", "digital art", "3D render", 
            "Ölgemälde", "Aquarell", "Cyberpunk", "Fotorealistisch", "Cartoon"
        ])
        img_size = st.selectbox("📐 Größe:", [
            "1024x1024 (quadratisch)",
            "1024x768 (landscape)",
            "768x1024 (portrait)",
            "1920x1080 (Full HD)"
        ])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Bild erstellen", use_container_width=True, key="gen_img", type="primary"):
        if not img_prompt:
            st.warning("⚠️ Bitte gib eine Bildbeschreibung ein!")
        else:
            with st.spinner("🎨 Bild wird erstellt..."):
                try:
                    full_prompt = f"{img_prompt}, {img_style}, high quality, 4k, detailed, masterpiece"
                    encoded_prompt = quote(full_prompt)
                    sizes = {
                        "1024x1024 (quadratisch)": "1024x1024",
                        "1024x768 (landscape)": "1024x768",
                        "768x1024 (portrait)": "768x1024",
                        "1920x1080 (Full HD)": "1920x1080"
                    }
                    size = sizes[img_size]
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={size.split('x')[0]}&height={size.split('x')[1]}&nologo=true"
                    response = requests.get(image_url, timeout=60)
                    if response.status_code == 200:
                        st.success("✅ Bild erfolgreich erstellt!")
                        st.image(response.content, caption=img_prompt, use_container_width=True)
                        st.download_button(
                            "💾 Bild herunterladen", 
                            response.content, 
                            f"increation_{img_style}.png", 
                            "image/png",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Fehler: {e}")

# ====== TAB 3: CODE-HELPER ======
with tab3:
    st.markdown("## 💻 Code-Helper – Dein Programmier-Assistent")
    
    st.markdown("""
    <div class="kreativ-box">
        <p style="color: #B8D4F0; margin: 0; text-align: center;">
        💻 Beschreibe, was der Code tun soll – die KI generiert dir sauberen Code!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Aufgabe beschreiben")
        code_request = st.text_area(
            " ",
            placeholder="z.B. Eine Python-Funktion, die alle Primzahlen bis n zurückgibt",
            height=120,
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("### 🛠️ Sprache & Details")
        code_language = st.selectbox("💻 Sprache:", [
            "Python", "JavaScript", "HTML/CSS", "Java", "C++", "SQL", 
            "TypeScript", "Go", "Rust", "PHP"
        ])
        code_erfahrung = st.selectbox("📊 Erfahrungslevel:", [
            "Anfänger (viele Kommentare)",
            "Fortgeschritten (normale Kommentare)",
            "Profi (minimal Kommentare)"
        ])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("⚡ Code generieren", use_container_width=True, key="gen_code", type="primary"):
        if not code_request:
            st.warning("⚠️ Bitte beschreibe deine Code-Aufgabe!")
        else:
            with st.spinner("💻 Code wird geschrieben..."):
                try:
                    kommentar_stil = {
                        "Anfänger (viele Kommentare)": "mit ausführlichen Kommentaren für jeden Schritt",
                        "Fortgeschritten (normale Kommentare)": "mit normalen Kommentaren, sauber und verständlich",
                        "Profi (minimal Kommentare)": "minimal kommentiert, produktionsreif"
                    }
                    
                    full_prompt = f"Schreibe {code_language} Code für: {code_request}. Stil: {kommentar_stil[code_erfahrung]}. Gib nur den fertigen Code zurück."
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": full_prompt}],
                        max_tokens=4000,
                        temperature=0.2
                    )
                    code = response.choices[0].message.content
                    
                    if "```" in code:
                        parts = code.split("```")
                        code_clean = parts[1].strip() if len(parts) >= 2 else code
                    else:
                        code_clean = code
                    
                    st.success("✅ Code erfolgreich generiert!")
                    
                    st.markdown("### 📋 Dein Code:")
                    st.code(code_clean, language=code_language.lower())
                    
                    st.download_button(
                        "💾 Code herunterladen",
                        code_clean,
                        "increation_code.txt",
                        "text/plain",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Fehler: {e}")

# Sidebar Info
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Über increation")
st.sidebar.markdown("""
<div class="kreativ-box" style="padding: 18px; margin: 0;">
    <p style="color: #6BB6FF; font-weight: 800; margin: 0 0 10px 0; font-size: 16px;">🧠 increation KI Studio</p>
    <p style="color: #B8D4F0; font-size: 13px; margin: 5px 0;">⚡ Powered by Groq</p>
    <p style="color: #B8D4F0; font-size: 13px; margin: 5px 0;">🎯 100% kostenlos</p>
    <p style="color: #B8D4F0; font-size: 13px; margin: 5px 0;">🚀 Ultra-schnell</p>
</div>
""", unsafe_allow_html=True)
