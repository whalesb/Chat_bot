import streamlit as st
import requests

# --- Configuration ---
VAPI_PRIVATE_KEY = st.secrets["VAPI_PRIVATE_KEY"]
ASSISTANT_ID     = st.secrets["ASSISTANT_ID"]

# --- Streamlit Setup ---
st.set_page_config(page_title="Vapi Chatbot", page_icon="🤖")
st.title("💬 Vapi Text Chatbot")

# Initialize conversation state
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores full chat history
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None  # Tracks server-side session

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Prompt user for input
user_input = st.chat_input("Say something...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare API call to /chats endpoint with full history
    api_url = "https://api.vapi.ai/chats"
    headers = {
        "Authorization": f"Bearer {VAPI_PRIVATE_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "assistantId": ASSISTANT_ID,
        "messages": st.session_state.messages  # send full history
    }
    if st.session_state.chat_id:
        payload["chatId"] = st.session_state.chat_id

    # Call Vapi
    with st.spinner("Assistant is thinking..."):
        resp = requests.post(api_url, json=payload, headers=headers)

    # Handle response
    if resp.ok:
        data = resp.json()
        # Update chat_id for session continuity
        if data.get("id"):
            st.session_state.chat_id = data["id"]
        # Update full history from response
        server_msgs = data.get("messages")  # Vapi returns full sequence
        if isinstance(server_msgs, list):
            st.session_state.messages = server_msgs
        # Extract assistant's latest reply
        if st.session_state.messages:
            bot_reply = st.session_state.messages[-1]["content"]
        else:
            bot_reply = "(No response)"
    else:
        bot_reply = f"Error {resp.status_code}: {resp.text}"

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
