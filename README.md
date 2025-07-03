# 🧠 Blockchain Automation Chatbot 🤖

A powerful AI-driven blockchain assistant that helps users interact with on-chain data effortlessly. This chatbot leverages LLM capabilities to dynamically interpret user queries and perform real-time blockchain tasks including phishing detection, token balance fetching, and live crypto news aggregation.

---

## 🚀 Features

1. **Phishing Address Checker 🛡️**  
   Detects whether a wallet address is flagged in the ScamSniffer GitHub database for scams or phishing.

2. **Token Balance Fetcher 💰**  
   Retrieves the top ERC-20 token balances for a given Ethereum wallet using the Moralis API.

3. **Latest Crypto News Aggregator 📰**  
   Fetches real-time news based on coin names or keywords using the CoinDesk News API.

---

## 🛠 Tech Stack

| Layer        | Technology                            |
|--------------|----------------------------------------|
| **Frontend** | Streamlit (Chat-style interface)       |
| **Backend**  | FastAPI (LLM-integrated logic)         |
| **LLM**      | OpenAI GPT-4o (Chat analysis + intent) |
| **APIs Used**| Moralis, CoinDesk, ScamSniffer GitHub  |

---

## 🧩 Architecture

- **LLM Agent (GPT-4o)**: Interprets chat intent and maps it to function calls (`check_phishing`, `get_token_balances`, `get_crypto_news`).
- **Function Executor**: FastAPI handles backend logic and dynamically executes appropriate functions.
- **Merge Layer**: Response from the LLM and function output is merged into a clean, user-friendly reply.
- **Streamlit UI**: A simple chat interface for user interaction, with real-time bot feedback and spinner animations.

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/blockchain-chatbot.git
cd blockchain-chatbot

