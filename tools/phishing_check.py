#This api key that i have used here is also freelu available 
from langchain.tools import Tool
import requests
def check_phishing(address):
    url = f"https://api.chainabuse.com/api/reports?address={address}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return f"Reports for {address}: {data}"
    else:
        return f"Failed to fetch data. Status code: {res.status_code}"

phishing_tool = Tool(
    name="PhishingChecker",
    func=check_phishing,
    description="Check if a wallet address has phishing or scam reports."
)
