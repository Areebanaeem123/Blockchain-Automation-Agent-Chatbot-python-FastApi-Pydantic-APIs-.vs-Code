#This file will use the openAI key 
from langchain.agents import initialize_agent
from dotenv import load_dotenv
from custom_llm import NgrokChatLLM
#loading API keys from .env
load_dotenv()
#importing the custom models
#initializing the custom llm 
llm = NgrokChatLLM(
    temperature=0.7,
    model ="gpt-4o"
)
"""
##now creating tha lancgain agent with your tools 
agent = initialize_agent(
    tools=[phishing_tool, price_alert_tool, crypto_news_tool,token_balance_tool],
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True ,#for showing logs in console 
    handle_parsing_errors = True 
)
"""
