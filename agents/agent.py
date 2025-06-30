#This file will use the openAI key 
from langchain.agents import initialize_agent
from dotenv import load_dotenv
from custom_llm import NgrokChatLLM
#loading API keys from .env
load_dotenv()
#importing the custom models
from tools.phishing_check import phishing_tool
from tools.price_alert import price_alert_tool
from tools.whale_transaction import whale_tool
from tools.crypto_news import crypto_news_tool
from tools.token_balance import token_balance_tool
from tools.gas_tracker import gas_tracker_tool
#initializing the custom llm 
llm = NgrokChatLLM(
    temperature=0.7,
    model ="gpt-4o"
)
##now creating tha lancgain agent with your tools 
agent = initialize_agent(
    tools=[phishing_tool, whale_tool, price_alert_tool, crypto_news_tool,token_balance_tool, gas_tracker_tool],
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True #for showing logs in console 
)