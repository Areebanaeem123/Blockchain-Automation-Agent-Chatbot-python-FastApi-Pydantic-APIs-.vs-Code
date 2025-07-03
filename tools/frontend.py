import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="Blockchain Chatbot", layout="centered")
st.title("🤖 Blockchain Automation Chatbot")
st.markdown("""
This chatbot lets you:
- Check if a wallet address is flagged for phishing 🛡️
- Fetch token balances from a wallet 💰
- Get the latest crypto news 📰
""")
# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "waiting_for_bot" not in st.session_state:
    st.session_state.waiting_for_bot = False
# Sidebar
st.sidebar.header("Chat Settings")
api_url = st.sidebar.text_input("Backend Chat Endpoint URL", value="http://localhost:8000/chat")
# User Input
user_input = st.chat_input("Ask something like 'Is this wallet a scam?' or 'Get Ethereum news'")
if user_input and not st.session_state.waiting_for_bot:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.waiting_for_bot = True

    # Display 'Bot is typing...'
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("_🤖 Bot is typing..._")

    # Send to backend
    payload = {
        "history": st.session_state.chat_history,
        "answer": ""
    }
    try:
        with st.spinner("Thinking..."):
            res = requests.post(api_url, json=payload)
            res.raise_for_status()
            data = res.json()
            response = data.get("response")
            st.session_state.chat_history = data.get("history", [])
    except Exception as e:
        response = f"❌ Error: {e}"
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    st.session_state.waiting_for_bot = False
    typing_placeholder.empty()

# Display chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        try:
            content = json.loads(message["content"])
            st.markdown(content["Answer"], unsafe_allow_html=True)
        except:
            st.markdown(message["content"], unsafe_allow_html=True)
