import streamlit as st
import requests
import json
from datetime import datetime
API_URL = "http://127.0.0.1:8000/chat"
st.set_page_config(page_title="Blockchain Automation Agent", page_icon="🔗")
st.title("🤖Blockchain Automation Chatbot")
st.subheader("🚀Ask about scam wallets, token balances, or crypto news.🚀")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
user_input = st.chat_input("Ask me something like: 'Check if this wallet is a scam'")
# Show chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        timestamp = msg.get("timestamp")
        content = msg["content"]
        if timestamp:
            content += f"\n\n<span style='color:gray;font-size:0.8em;'>🕒 {timestamp}</span>"
        st.markdown(content, unsafe_allow_html=True)
# Handle user input
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    st.session_state.last_input = user_input
# Call backend if there's new user input or retrying
if user_input or (st.session_state.last_input and st.button("🔁 Retry Last")):
    payload = {
        "history": [msg for msg in st.session_state.chat_history if msg["role"] != "assistant"],
        "answer": st.session_state.last_input
    }
    with st.chat_message("assistant"):
        with st.spinner("🤖 Typing..."):
            try:
                response = requests.post(API_URL, json=payload)
                result = response.json()
                assistant_reply = result.get("response", "Something went wrong.")

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.markdown(assistant_reply + f"\n\n<span style='color:gray;font-size:0.8em;'>🕒 {timestamp}</span>", unsafe_allow_html=True)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": assistant_reply,
                    "timestamp": timestamp
                })
            except Exception as e:
                st.error(f"❌ Backend error: {e}")
                st.warning("Click '🔁 Retry Last' to try again.")
