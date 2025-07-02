from langchain.tools import Tool
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import json 
from pathlib import Path 
import requests
import os
from dotenv import load_dotenv
import json
import feedparser
from html import unescape
from datetime import datetime , timezone
load_dotenv()
app = FastAPI()
crypt_news_api_key = os.getenv("CRYPTO_NEWS_API_KEY")
moralis_api_key = os.getenv("MORALIS_API_KEY")
forta_api_key = os.getenv("FORTA_API_KEY")#not working  (paid version required)
chainabuse_api_key = os.getenv("CHAINABUSE_API_KEY") #not working  (paid version required) 
coindesk_api_key = os.getenv("COINDESK_API_KEY")
class WalletAddress(BaseModel):
    address :str
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
class ChatHistoryRequest(BaseModel):
    history: List[ChatMessage]
    answer: Optional[str] = ""
#for checking phishing query
import requests
def check_phishing(address: str) -> str:
    try:
        # Load scam address database from local GitHub clone  
        db_path = Path("C:/Users/HP/Blockchain-automation-agent/scam-database/blacklist/address.json") #set this path accordingly (see the folder scan-database) i cloned it from github 
        if not db_path.exists():
            return "❌ ScamSniffer database not found. Make sure you cloned https://github.com/scamsniffer/scam-database."
        with db_path.open("r", encoding="utf-8") as f:
            scam_data = json.load(f)

        address = address.lower().strip()

        if address in scam_data:
            label = scam_data[address].get("label", "Scam")
            reported_at = scam_data[address].get("reportedAt", "N/A")
            return (
                f"🚨 Address `{address}` is flagged as **{label}** by ScamSniffer.\n"
                f"- 🕒 Reported At (epoch): `{reported_at}`\n"
                f"- 📂 Source: [ScamSniffer GitHub](https://github.com/scamsniffer/scam-database)"
            )
        else:
            return f"✅ Address `{address}` appears clean (not found in ScamSniffer GitHub list)."

    except Exception as e:
        return f"❌ Error while checking ScamSniffer DB: {str(e)}"
def get_crypto_news(query="Ethereum"):
    url = "https://data-api.coindesk.com/news/v1/search"
    headers={
        "X-CoinDesk-API-Key": coindesk_api_key
    }
    params ={
        "search_string": query,
        "lang": "EN",
        "source_key": "coindesk"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("Data", [])
        print(articles)
        if not articles:
            return f"No news found for '{query}'."
        formatted_articles = []
        for article in articles:
            # Extract fields safely
            published_ts = article.get("PUBLISHED_ON")
            if published_ts:
                published_date = datetime.fromtimestamp(published_ts, tz=timezone.utc).strftime('%Y-%m-%d')
            else:
                published_date = "Unknown"
            title = article.get("TITLE", "No title")
            subtitle = article.get("SUBTITLE", "No subtitle")
            summary = article.get("SUMMARY", "No summary")
            authors = article.get("AUTHORS", "Unknown")
            body = article.get("BODY", "No body content")
            block = (
                f"🗞️ **{title}**\n"
                f"📅 **Published On**: {published_date}\n"
                f"✍️ **Authors**: {authors}\n"
                f"📋 **Subtitle**: {subtitle}\n"
                f"📜 **Summary**: {summary}\n"
                f"📝 **Content**:\n{body[:500]}..."  # Trim body for display
            )
            formatted_articles.append(block)

        return "\n\n---\n\n".join(formatted_articles)

    except requests.exceptions.RequestException as e:
        return f"❌ API request error: {e}"
    except Exception as e:
        return f"❌ General error: {e}"

#for the token balance thing
def get_token_balances(address: str):
    url = f"https://deep-index.moralis.io/api/v2.2/{address}/erc20"
    headers = {
        "accept": "application/json",
        "X-API-Key": moralis_api_key
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            return "No token balances found for this address."
        balances = []
        for token in data[:5]:  # limit to top 5 tokens
            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "")
            balance = int(token["balance"]) / 10**int(token["decimals"])
            balances.append(f"{name} ({symbol}): {balance:.4f}")
        return "\n".join(balances)
    except Exception as e:
        return f"❌ Error fetching token balances: {e}"
@app.post("/token-balances")
async def token_balances(wallet: WalletAddress):
    if not moralis_api_key:
        raise HTTPException(status_code=500, detail="the moralis api could not fetch")
    result = get_token_balances(wallet.address)
    return {"address": wallet.address, "balances": result}


