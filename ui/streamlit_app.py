# Filename: ui/streamlit_app.py

import streamlit as st
import requests
from typing import List, Tuple

# === Configuration ===
BACKEND_URL = "http://localhost:8000/chat"
st.set_page_config(page_title="LangChain Chat", page_icon="🧠", layout="wide")

# === Initialize chat memory ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history: List[Tuple[str, str]] = []

# === Function to call the backend ===
def get_response_from_backend(user_input: str, chat_history: List[Tuple[str, str]]) -> str:
    try:
        payload = {
            "question": user_input,
            "chat_history": chat_history,
        }
        response = requests.post(BACKEND_URL, json=payload, timeout=30)
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

# Display existing chat
for user_msg, bot_msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)

# Input from user
if user_input := st.chat_input("Ask something..."):
    # Display user message
    st.chat_message("user").markdown(user_input)

    # Get response from backend
    with st.spinner("Thinking..."):
        bot_response = get_response_from_backend(user_input, st.session_state.chat_history)

    # Display assistant reply
    st.chat_message("assistant").markdown(bot_response)

    # Update session memory
    st.session_state.chat_history.append((user_input, bot_response))
