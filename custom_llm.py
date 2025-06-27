from langchain.llms.base import LLM
from langchain.schema import LLMResult, Generation
from typing import Optional, List, Mapping, Any
from pydantic import BaseModel, Field
import requests

class NgrokChatLLM(LLM, BaseModel):
    api_url: str = Field(default="https://206c-20-106-58-127.ngrok-free.app/chat")
    temperature: float = Field(default=0.7)
    model: str = Field(default="gpt-4o")

    @property
    def _llm_type(self) -> str:
        return "ngrok-chat"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        payload = {
            "messages": messages,
            "temperature": self.temperature,
            "model": self.model
        }

        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response received.")

    def _agenerate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        generations = [Generation(text=self._call(prompt)) for prompt in prompts]
        return LLMResult(generations=[generations])
