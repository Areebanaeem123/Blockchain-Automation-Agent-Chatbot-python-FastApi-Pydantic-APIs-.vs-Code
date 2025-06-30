#🛡️ Blockchain Auto Agent 🤖🔗
A smart AI-powered blockchain assistant built with LangChain and Streamlit. This chatbot-style agent analyzes wallet addresses, tracks crypto prices, and flags suspicious activity — all in real-time.

#🔍 Features
##✅ Phishing Checker (Chainabuse API)
Detects if a wallet address is involved in scams, frauds, or phishing schemes.
Returns detailed reports directly in the chatbot.
##📈 Price Alert Tool (CoinGecko API)
Monitors BTC/ETH prices.
Alerts the user if a crypto coin exceeds a defined USD threshold.
##🐋 Whale Transaction Monitor (Coming Soon)
Will track large transactions ("whales") on Ethereum or Bitcoin blockchain.
Highlights transfers over a user-defined value.
##🧠 Tech Stack
LangChain — To build and manage the LLM agent logic
OpenAI / GPT-4o — Language model for reasoning and conversation
Streamlit — Beautiful, interactive frontend UI
Chainabuse API — To detect wallet fraud/phishing reports
CoinGecko API — For real-time crypto pricing
QuickNode / Alchemy (Planned) — To fetch whale transactions via on-chain data
##📦 Installation

git clone https://github.com/your-username/blockchain-auto-agent.git
cd blockchain-auto-agent
pip install -r requirements.txt
streamlit run main.py
Add your API keys in a .env file:
env

OPENAI_API_KEY=your_openai_key
COINGECKO_API_KEY=optional
CHAINABUSE_API_KEY=your_chainabuse_key
QUICKNODE_FUNCTION_URL=https://...
QUICKNODE_API_KEY=your_key
#💡 Example Prompts

🔐 "Check if this address 0x742d35... is involved in fraud"
📈 "Alert me if Bitcoin crosses 50,000 USD"
🐋 "Show me Ethereum whale transactions from the last 5 days" *(Coming soon)*
#📊 Future Features
Whale transaction tracking via QuickNode Functions
Telegram notifications for price alerts
Dark/light mode switch for the frontend
Deployment on Streamlit Cloud or Hugging Face Spaces
#🤝 Contributing
Contributions welcome! Open an issue or submit a PR.
Thank you !
