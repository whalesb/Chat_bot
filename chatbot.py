import streamlit as st
import requests

# --- Configuration ---
VAPI_PRIVATE_KEY = st.secrets["VAPI_PRIVATE_KEY"]
ASSISTANT_ID     = st.secrets["ASSISTANT_ID"]

# --- Streamlit Setup ---
st.set_page_config(page_title="Vapi Chatbot", page_icon="🤖")
st.title("💬 Vapi Text Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New user input
user_input = st.chat_input("Say something...")

if user_input:
    # show the user’s message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call Vapi’s /chat endpoint
    api_url = "https://api.vapi.ai/chat"
    headers = {
        "Authorization": f"Bearer {VAPI_PRIVATE_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "assistantId": ASSISTANT_ID,
        "input": user_input
    }
    # for multi‑turn, include the previous chat ID:
    if st.session_state.chat_id:
        payload["previousChatId"] = st.session_state.chat_id

    with st.spinner("Assistant is thinking..."):
        resp = requests.post(api_url, json=payload, headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        # Capture the chat session ID on the first turn
        if not st.session_state.chat_id and data.get("id"):
            st.session_state.chat_id = data["id"]
        # The assistant’s reply is in data["output"]
        outputs = data.get("output", [])
        bot_reply = outputs[-1]["content"] if outputs else "(No response)"
    else:
        bot_reply = f"Error {resp.status_code}: {resp.text}"

    # display the assistant reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
