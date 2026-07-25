import streamlit as st
from groq import Groq

st.set_page_config(page_title="Meine KI-Plattform", page_icon="🤖")

st.title("🤖 Meine KI-Plattform")
st.write("Willkommen! Diese Plattform ist komplett kostenlos mit Groq!")

st.header("💬 KI-Chat")

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("Bitte GROQ_API_KEY in Streamlit Secrets setzen!")
    st.info("👉 Holen Sie sich einen kostenlosen Key auf https://console.groq.com/")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Top Modelle bei Groq
model_choice = st.selectbox("Modell wählen:", [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
])

# Chat-Verlauf
if "messages" not in st.session_state:
    st.session_state.messages = []

# Zeige Chat-Verlauf
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
prompt = st.chat_input("Stelle deine Frage...")

if prompt:
    # User-Nachricht anzeigen
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # KI-Antwort generieren
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

# Clear-Button
if st.sidebar.button("🗑️ Chat löschen"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("### Info")
st.sidebar.info("Powered by Groq ⚡ - ultraschnell & kostenlos")

st.sidebar.markdown("### Modelle")
st.sidebar.write("""
- 🦙 Llama 3.3 70B
- 🦙 Llama 3.1 70B  
- 🦙 Llama 3.1 8B
- 🎭 Mixtral 8x7B
- 💎 Gemma2 9B
""")
