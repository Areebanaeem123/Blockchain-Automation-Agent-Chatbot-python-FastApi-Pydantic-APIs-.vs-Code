import os
import requests
from langchain.tools import Tool
from dotenv import load_dotenv

load_dotenv()
news_api_key = os.getenv("CRYPTO_NEWS_API_KEY")

def fetch_crypto_news(topic=None):
    base_url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": news_api_key,
        "kind": "news",  # filter for news only, not signals
        "currencies": topic.upper() if topic else None
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        posts = data.get("results", [])[:5]

        if not posts:
            return "No recent news found."

        news_items = [
            f"🗞️ {post['title']}\n🔗 {post['url']}" for post in posts
        ]
        return "\n\n".join(news_items)

    except Exception as e:
        return f"❌ Error fetching news: {e}"

crypto_news_tool = Tool(
    name="CryptoNews",
    func=fetch_crypto_news,
    description="Use this to get the latest crypto news headlines. Optionally provide a topic like BTC or ETH."
)
