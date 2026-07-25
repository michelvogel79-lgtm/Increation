import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Meine KI-Plattform", page_icon="🤖")

st.title("🤖 Meine KI-Plattform")
st.write("Willkommen! Diese Plattform ist komplett kostenlos.")

st.header("💬 KI-Chat")

try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("Bitte HF_TOKEN in Streamlit Secrets setzen!")
    st.stop()

# VIELE Modelle zur Auswahl
model_choice = st.selectbox("Modell wählen:", [
    "meta-llama/Llama-3.3-70B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct",
    "meta-llama/Llama-3.2-1B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mistral-Nemo-Instruct-2407",
    "microsoft/Phi-3-mini-4k-instruct",
    "microsoft/Phi-3.5-mini-instruct",
    "google/gemma-2-2b-it",
    "google/gemma-2-9b-it",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-1.5B-Instruct",
    "HuggingFaceH4/zephyr-7b-beta"
])

# Provider-Auswahl
provider_choice = st.selectbox("Provider wählen:", [
    "auto",
    "together",
    "fireworks",
    "groq",
    "cerebras",
    "replicate"
])

prompt = st.text_input("Stelle deine Frage:")

if st.button("🚀 Generieren"):
    if prompt:
        with st.spinner(f"KI ({model_choice}) denkt nach..."):
            try:
                client = InferenceClient(
                    model=model_choice, 
                    token=HF_TOKEN,
                    provider=provider_choice if provider_choice != "auto" else None
                )
                response = client.chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                st.success("Fertig!")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Fehler: {e}")
                st.info("💡 Versuche ein anderes Modell oder Provider!")
    else:
        st.warning("Bitte eine Frage eingeben!")

st.sidebar.markdown("### Info")
st.sidebar.info("Powered by Hugging Face & Streamlit")

st.sidebar.markdown("### Verfügbare Modelle")
st.sidebar.write("12+ Modelle verfügbar!")
