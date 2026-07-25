import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="increation - KI Studio",
    page_icon="🚀",
    layout="wide"
)

LOGO = "🚀"
LOGO_NAME = "increation"

st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <h1 style="font-size: 60px;">{LOGO}</h1>
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
    st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <h1 style="font-size: 50px;">{LOGO}</h1>
            <h3>increation</h3>
        </div>
    """, unsafe_allow_html=True)
    
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
        with st.spinner(f"{LOGO} denkt nach..."):
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
