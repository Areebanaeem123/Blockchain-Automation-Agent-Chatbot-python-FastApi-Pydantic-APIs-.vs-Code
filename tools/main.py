# run_agent.py
import os
import json
from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.concurrency import run_in_threadpool
from app import check_phishing ,  get_crypto_news , get_token_balances
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatHistoryRequest(BaseModel):
    history: list
    answer : str
    task_id : int

SYSTEM_PROMPT = """
You are a blockchain assistant. You will be given user queries and must identify the appropriate function to call based on each query. You will also be provided with a list of available functions and their descriptions.

If the user query does not specify which function to call, respond using your own knowledge and suggest functions the user may want to use.
Note: Some functions contain specific guidance in their descriptions about how and when they should be suggested or triggered. Be sure to follow those instructions exactly when handling user queries. 
Your responses must follow this JSON structure:
{
    "Function Name": "The matched function name based on the user query, or None if no match is found",
    "Answer": "Your response to the user query, including suggestions or questions for values",
    "Proceed": "set to true once all the parameters for the identified functions are provided ",
    "Function Parameters": "A dictionary of all required parameters once provided, otherwise NULL" 
}
Once a function is identified, begin asking the user for the required parameters for that function. 
If the user changes their intent and requests a different function while parameters are still being collected, switch to the new function and begin asking for the new parameters. 
If the user provides all required parameters, set "Proceed" to true and include the parameters in the "Function Parameters" dictionary. 
If the user provides an invalid or incorrect parameter, ask again for the correct input. 
Once a task is done:
- DO NOT explain how the task was completed.
- DO NOT mention the backend function or logic.
- Just confirm that the task is done.
- Then immediately suggest the next task the user can perform.
- If the task was an interruption, return to the previous task instead of suggesting a new one.

Available Functions:

1 - Name: check_phishing 
    Description: Check if a wallet address has phishing or scam reports and according to it provide user with the result.  
    Parameters:
        - Wallet Address (string; a valid Ethereum or other chain wallet address)
        In the json you return the paramets should be -+in programatic format i.e. where comma seprated a list is provided,and for other values also 
2 - Name: get_crypto_news  
    Description: Fetch the latest crypto news based on the coin name or keyword.  
    Parameters:
        - Query (string; e.g., "bitcoin", "ethereum", or general terms like "defi")
3 - Name: get_token_balances
    Description: Retrieve the top token balances for a given blockchain wallet address.
    Parameters:
        - Wallet Address (string; a valid blockchain wallet address)
You must follow these instructions strictly. If the user initiates a new task while a previous one is incomplete, handle the new task and then return to the previous one. All user-facing responses should be stored in the "Answer" field, where you ask for parameters, provide suggestions, or answer general queries, when asking for users to eneter parameters dont mention them as parameters ask the user to provide these values and against each value provide a short description or example of that value of how they have to provide it, 
Task flow steps : 

    Step 1: Wait until all parameters for a task have been completed. 

    Step 2: Ensure all details and user confirmations are received. 

    Step 3: Once confirmed: 

        - Do NOT mention what you are proceeding with. 

        - Do NOT explain how it was done. 

        - Simply state that the task is done. 

        - Immediately suggest a new task the user can perform. 

    Step 4: If this task was an interruption (loaded in between another task): 

        - Instead of suggesting a new task, continue where you left off in the previous task. 
You must not make the proceed value to true unless you have done all confirmations, even if all the parameters are filled and you have to make a confirmation call, after the user confirms then make the proceed value true 

In the email generation task you must not genrate an email, you just ask for prompt and make proceed true, and mention Email Generated 
You must not mark `Proceed` as true unless:
- All required values have been confirmed
- The user has clearly approved moving forward
Always be helpful, conversational, and structured. If you're unsure which function to trigger, ask clarifying questions.
"""
first_response = """## Chat Endpoint Agent

I am an intelligent agent designed to handle dynamic blockchain tasks such as phishing checks, crypto news, and token balances.

When I receive a chat history, I:

1. **Understand the context** – I process all previous messages in the conversation.
2. **Interpret the request** – I analyze the chat using the `LeadGenerationAgent` logic.
3. **Decide whether to proceed** – Based on intent and confirmation.
4. **Call the right function** – Depending on what is needed:
   - Check wallet for phishing (`check_phishing`)
   - Get token balances (`get_token_balances`)
   - Get crypto news (`get_crypto_news`)
5. **Return a clear, human-readable response**

"""
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
class ChatHistoryRequest(BaseModel):
    history: List[ChatMessage]
    answer: Optional[str] = ""
from fastapi.concurrency import run_in_threadpool
def get_chat_response(arr):
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=arr,
        temperature=0
    )
    return resp.choices[0].message.content

def LeadGenerationAgent(chat_history):
    full_history = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history
    response = get_chat_response(full_history)
    return response
def merge_chat_response(assistant_response, function_response):
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a smart assistant. You will be provided with an assistant response and a function response. "
                    "The assistant response comes after the user provided details and the assistant initiated a function. "
                    "The function response is the output of that function. Merge both into a user-facing message:\n\n"
                    "- Confirm the task is complete.\n"
                    "- Show the function output clearly.\n"
                    "- Include any follow-up suggestions or instructions from the assistant response.\n"
                    "- Mention if the user wants to continue a previous task.\n\n"
                    "Your final response must be in markdown. Just return the merged message, nothing else."
                )
            },
            {
                "role": "user",
                "content": (
                    f"assistant response: {assistant_response}\n\n"
                    f"function response: {function_response}"
                )
            }
        ],
        temperature=0
    )
    return resp.choices[0].message.content

@app.post("/chat")
async def chat_endpoint(req: ChatHistoryRequest):
    chat_history = req.history
    if len(chat_history) == 0 and req.answer == "":
        return {"history": [], "response": first_response}
    if req.answer:
        chat_history.append({"role": "user", "content": req.answer})
    assistant_response = LeadGenerationAgent(chat_history)
    assistant_response = assistant_response.replace("```", "").replace("json", "")
    ass_resp = json.loads(assistant_response)
    if ass_resp["Proceed"]:
        fn = ass_resp["Function Name"]
        params = ass_resp["Function Parameters"]
        if fn == "check_phishing":
            results = check_phishing(params["Wallet Address"])
            final_response = merge_chat_response(ass_resp["Answer"], results)
            ass_resp["Answer"] = final_response
        elif fn == "get_token_balances":
            results = get_token_balances(params["Wallet Address"])
            final_response = merge_chat_response(ass_resp["Answer"], results)
            ass_resp["Answer"] = final_response
        elif fn == "get_crypto_news": #because the api i have used it gives info for the keywords like ETH , BTC thats why i have done mapping here 
            COIN_MAP = {
                "ethereum": "ETH",
                "bitcoin": "BTC",
                "solana": "SOL",
                "cardano": "ADA",
                "dogecoin": "DOGE"
            }
            # Right before calling get_crypto_news():
            query = params["Query"].lower()
            params["Query"] = COIN_MAP.get(query, query.upper())
            results = get_crypto_news(params["Query"])
            final_response = merge_chat_response(ass_resp["Answer"], results)
            ass_resp["Answer"] = final_response
    chat_history.append({"role": "assistant", "content": json.dumps(ass_resp)})
    return {"history": chat_history, "response": ass_resp["Answer"]}
