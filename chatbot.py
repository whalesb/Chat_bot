import streamlit as st
import requests

# --- Configuration ---
VAPI_PRIVATE_KEY = "56039554-5828-4a5f-a307-e181477104ea"  # Replace with your private API key
ASSISTANT_ID = "d5e70420-ed24-423c-96b7-94bdc9b4fd31"  # Replace with your assistant ID

# --- Streamlit UI ---
st.set_page_config(page_title="Vapi Text Chat_bot", page_icon="🤖")
st.title("💬 Vapi Text Chatbot (Python + Streamlit)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Say something...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- Call Vapi API ---
    api_url = f"https://api.vapi.ai/assistant/{ASSISTANT_ID}/text"
    headers = {
        "Authorization": f"Bearer {VAPI_PRIVATE_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"text": user_input}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            bot_reply = response.json().get("text", "(No response from assistant)")
        else:
            bot_reply = f"(Error {response.status_code}: {response.text})"
    except Exception as e:
        bot_reply = f"(Connection error: {str(e)})"

    # Display assistant message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
