import os
import requests
from dotenv import load_dotenv
from langchain.tools import Tool

load_dotenv()
moralis_api_key = os.getenv("MORALIS_API_KEY")

def get_token_balances(address):
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

token_balance_tool = Tool(
    name="TokenBalanceChecker",
    func=get_token_balances,
    description="Use this tool to check ERC-20 token balances for a given Ethereum wallet address."
)
