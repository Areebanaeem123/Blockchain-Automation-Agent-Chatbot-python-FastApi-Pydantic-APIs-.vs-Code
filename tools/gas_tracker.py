# tools/gas_tracker.py

import os
import requests
from dotenv import load_dotenv
from langchain.tools import Tool

load_dotenv()
etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")

def get_gas_price(_input=""):
    try:
        url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={etherscan_api_key}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        if data["status"] != "1":
            return "⚠️ Unable to fetch gas price at the moment."

        result = data["result"]
        low = result["SafeGasPrice"]
        avg = result["ProposeGasPrice"]
        high = result["FastGasPrice"]

        return (
            f"⛽ **Ethereum Gas Prices** (in Gwei):\n"
            f"- 🟢 Low: {low} Gwei\n"
            f"- 🟡 Average: {avg} Gwei\n"
            f"- 🔴 High: {high} Gwei"
        )

    except Exception as e:
        return f"❌ Error fetching gas price: {e}"

gas_tracker_tool = Tool(
    name="GasPriceTracker",
    func=get_gas_price,
    description="Use this tool to check current Ethereum gas prices (low, average, high) in Gwei."
)
