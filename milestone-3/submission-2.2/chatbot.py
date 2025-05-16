import streamlit as st
import requests
import uuid

# Page config
st.set_page_config(page_title="Chatbot", page_icon="🤖")

st.title("🤖 LangChain Chatbot UI")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())  # Unique ID per session

# Display previous messages
for role, content in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(content)


def generate_response(user_input, chat_history, chat_id):
    # Format history into list of [user, assistant] pairs
    formatted_history = []
    for i in range(0, len(chat_history), 2):
        try:
            user = chat_history[i][1]
            assistant = chat_history[i + 1][1] if i + 1 < len(chat_history) else ""
            formatted_history.append([user, assistant])
        except IndexError:
            pass  # Skip malformed pairs

    payload = {
        "question": user_input,
        "chat_history": formatted_history,
        "chat_id": chat_id,
    }

    try:
        response = requests.post("http://localhost:8000/chat", json=payload)
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer", "No answer received.")
        return answer
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return "Sorry, there was an error with the request."


# Chat input
if prompt := st.chat_input("Type a message..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append(("user", prompt))

    with st.spinner("Thinking..."):
        response = generate_response(prompt, st.session_state.chat_history, st.session_state.chat_id)

    # Display assistant response
    st.chat_message("assistant").markdown(response)
    st.session_state.chat_history.append(("assistant", response))
