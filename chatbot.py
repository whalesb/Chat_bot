import streamlit as st
import requests

# --- Configuration (Use Streamlit Secrets) ---
VAPI_PRIVATE_KEY = st.secrets["VAPI_PRIVATE_KEY"]
ASSISTANT_ID     = st.secrets["ASSISTANT_ID"]

# --- Streamlit UI ---
st.set_page_config(page_title="Vapi Text Chatbot", page_icon="🤖")
st.title("💬 Vapi Text Chatbot (Python + Streamlit)")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Say something...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- Call Vapi Chat API via /chat endpoint ---
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

    try:
        with st.spinner("Assistant is thinking..."):
            response = requests.post(api_url, json=payload, headers=headers)
            data = response.json()

            if response.status_code == 200:
                # Capture chat ID on first response
                if not st.session_state.chat_id and data.get("id"):
                    st.session_state.chat_id = data["id"]
                # Assistant responses are in 'output'
                outputs = data.get("output", [])
                bot_reply = outputs[-1].get("content", "(No response)") if outputs else "(No response)"
            else:
                bot_reply = f"Error {response.status_code}: {response.text}"
    except Exception as e:
        bot_reply = f"Connection error: {str(e)}"

    # Display assistant message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
