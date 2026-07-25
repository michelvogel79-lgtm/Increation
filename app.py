import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Meine KI-Plattform", page_icon="🤖")

st.title("🤖 Meine KI-Plattform")
st.write("Willkommen! Diese Plattform ist komplett kostenlos.")

st.header("💬 KI-Chat")

# Token wird später in Streamlit Secrets gesetzt
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("Bitte HF_TOKEN in Streamlit Secrets setzen!")
    st.stop()

client = InferenceClient(token=HF_TOKEN)

prompt = st.text_input("Stelle deine Frage:")

col1, col2, col3 = st.columns(3)
with col1:
    model_choice = st.selectbox("Modell:", [
        "mistralai/Mistral-7B-Instruct-v0.3",
        "meta-llama/Llama-3.2-3B-Instruct"
    ])

if st.button("🚀 Generieren"):
    if prompt:
        with st.spinner("KI denkt nach..."):
            try:
                response = client.chat_completion(
                    model=model_choice,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                st.success("Fertig!")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Fehler: {e}")
    else:
        st.warning("Bitte eine Frage eingeben!")

st.sidebar.markdown("### Info")
st.sidebar.info("Powered by Hugging Face & Streamlit")
