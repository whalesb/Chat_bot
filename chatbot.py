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

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get new user input
user_input = st.chat_input("Say something...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- Call Vapi /chat endpoint ---
    api_url = "https://api.vapi.ai/chat"
    headers = {
        "Authorization": f"Bearer {VAPI_PRIVATE_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "assistantId": ASSISTANT_ID,
        "input": user_input
    }
    if st.session_state.chat_id:
        payload["previousChatId"] = st.session_state.chat_id

    with st.spinner("Assistant is thinking..."):
        resp = requests.post(api_url, json=payload, headers=headers)

    if resp.ok:
        data = resp.json()
        # Store chat session ID on first turn
        if not st.session_state.chat_id and data.get("id"):
            st.session_state.chat_id = data["id"]
        # Parse assistant's reply
        outputs = data.get("output", [])
        bot_reply = outputs[-1].get("content", "(No response)") if outputs else "(No response)"
    else:
        bot_reply = f"Error {resp.status_code}: {resp.text}"

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
