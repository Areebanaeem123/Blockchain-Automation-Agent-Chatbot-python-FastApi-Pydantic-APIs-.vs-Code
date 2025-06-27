import streamlit as st
from agents.agent import agent  # Make sure agent includes phishing_tool and price_alert_tool
# Streamlit page config
st.set_page_config(page_title="Blockchain Auto Agent", page_icon="🚀", layout="centered")
# Custom CSS styling for a sleek look
st.markdown("""
    <style>
        .main {
            background-color: #f7f9fc;
        }
        .block-container {
            padding: 2rem 1rem;
        }
        .stTextInput>div>div>input {
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 0.75rem;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #10538c;
        }
    </style>
""", unsafe_allow_html=True)
# App Header
st.title("🤖Blockchain Auto Agent🤖")
st.subheader("Check wallet safety and set crypto price alerts easily")
# Tab selection for tools
tool_selection = st.selectbox("Select Tool", ["🔧Phishing Checker", "💰Price Alert","🐋Whale Transaction"])
# ---- PHISHING TOOL ---- #
if tool_selection == "🔧Phishing Checker":
    st.write("Check if a crypto wallet is flagged for scams , phishing or fraud.")
    wallet_address = st.text_input("Enter Wallet Address")
    if st.button("Check Address"):
        if wallet_address:
            with st.spinner("Analyzing wallet address..."):
                response = agent.run(f"Check if this address {wallet_address} is involved in fraud")
            st.success(response)
        else:
            st.warning("Please enter a wallet address.")

# ---- PRICE ALERT TOOL ---- #
elif tool_selection == "💰Price Alert":
    st.write("💰Set a price alert for Bitcoin or Ethereum.💰")
    coin = st.selectbox("Select Coin", ["bitcoin", "ethereum"])
    threshold = st.number_input("Alert Threshold in USD", min_value=1.0, step=100.0)

    if st.button("Set Alert"):
        with st.spinner("Setting up alert..."):
            response = agent.run(f"Alert me if {coin} crosses {threshold} USD")
        st.success(response)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>💎 Made with LangChain + Streamlit</p>", unsafe_allow_html=True)
