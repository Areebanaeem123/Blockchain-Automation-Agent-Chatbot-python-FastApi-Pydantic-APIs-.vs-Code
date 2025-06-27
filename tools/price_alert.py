#The api key i have used here is freely available 
from langchain.tools import Tool
import requests
def check_price_alert(threshold=65000, coin="bitcoin"):
    try: 
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        if coin not in data:
            return f"⚠️ Coin '{coin}' not found. Please try 'bitcoin' or 'ethereum'."
        price = data[coin]["usd"]
        if price > threshold:
            return f"⚠️ ALERT: {coin.upper()} price is **${price}**, which is above your threshold of ${threshold}!"
        else:
            return f"{coin.upper()} is currently at ${price}, below your threshold of ${threshold}."
    except Exception as e:
        return f"❌ Error checking price alert: {str(e)}"
# Define the LangChain tool
price_alert_tool = Tool(
    name="PriceAlert",
    func=check_price_alert,
    description="Set price alerts for BTC or ETH by comparing the current price to a given threshold."
)
