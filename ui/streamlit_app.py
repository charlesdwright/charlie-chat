# Filename: ui/streamlit_app.py

import streamlit as st
import requests
import uuid
from typing import List, Tuple
from config import CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Configuration ===
BACKEND_URL = CONFIG["backend_url"]

# === Session Initialization ===
if "chat_id" not in st.session_state:
    st.session_state["chat_id"] = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history: List[Tuple[str, str]] = []

# === Streamlit Page Config ===
st.set_page_config(page_title="LangChain Chat", page_icon="🧠", layout="wide")

# === Function to call the backend ===
def get_response_from_backend(user_input: str, chat_history: List[Tuple[str, str]]) -> str:
    try:
        payload = {
            "question": user_input,
            "chat_history": chat_history,
            "chat_id": st.session_state["chat_id"],
        }
        logger.debug(f" ---- the payload: {payload}")

        #response = requests.post(BACKEND_URL, json=payload, timeout=30)
        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "⚠️ No answer returned.")
    except requests.exceptions.RequestException as e:
        return f"🚨 Request failed: {e}"

# === Sidebar controls ===
with st.sidebar:
    st.title("🔧 Controls")
    if st.button("Reset Conversation"):
        st.session_state.chat_history = []
        st.experimental_rerun()
    st.markdown("**Backend URL:**")
    st.code(BACKEND_URL, language="bash")

# === Main Interface ===
st.title("🧠 LangChain Chatbot (Cloudflare LLM)")
st.caption("Powered by a custom FastAPI backend + LangChain chain")

# Display existing chat history
for user_msg, bot_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)

# === Input and response flow ===
if user_input := st.chat_input("Ask something..."):
    # ---- Check for duplicate input to avoid unnecessary backend calls ----
    if (
        st.session_state.chat_history and
        st.session_state.chat_history[-1][0].strip().lower() == user_input.strip().lower()
    ):
        st.warning("You just asked that. Try something different!")
    else:
        # Display user message
        st.chat_message("user").markdown(user_input)

        # Get response from backend
        with st.spinner("Thinking..."):
            bot_response = get_response_from_backend(user_input, st.session_state.chat_history)

        # Display assistant reply
        st.chat_message("assistant").markdown(bot_response)

        # Update session memory
        st.session_state.chat_history.append((user_input, bot_response))
