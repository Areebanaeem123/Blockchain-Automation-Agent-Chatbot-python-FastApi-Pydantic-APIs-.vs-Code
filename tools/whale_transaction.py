from langchain.tools import Tool
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()
API_KEY = os.getenv("WHALE_ALERT_API_KEY")
def get_whale_txn(coin="bitcoin", days=1):
    try:
        end_time = int(datetime.utcnow().timestamp())
        start_time = int((datetime.utcnow() - timedelta(days=days)).timestamp())
        url = (
            f"https://api.whale-alert.io/v1/transactions?"
            f"api_key={API_KEY}&start={start_time}&end={end_time}&min_value=500000&currency={coin}"
        )
        res = requests.get(url)
        if res.status_code != 200:
            return f"❌ Failed to fetch whale data: {res.status_code} - {res.text}"
        data = res.json()
        if not data.get("transactions"):
            return f"No whale transactions found for {coin.upper()} in the last {days} days."
        # Format top 3 transactions
        formatted = ""
        for tx in data["transactions"][:3]:
            formatted += (
                f"\n🔁 {tx['amount']} {tx['symbol'].upper()} | From: {tx['from']['owner_type']} "
                f"→ To: {tx['to']['owner_type']} | USD Value: ${tx['amount_usd']:,.0f}"
            )
        return f"🐋 Top Whale Transactions (Last {days} Days on {coin.upper()}):\n{formatted}"
    except Exception as e:
        return f"❌ Error fetching whale transactions: {str(e)}"
# Define LangChain Tool
whale_tool = Tool(
    name="WhaleTransactions",
    func=get_whale_txn,
    description="Get whale transactions for Bitcoin or Ethereum from the last N days"
)
