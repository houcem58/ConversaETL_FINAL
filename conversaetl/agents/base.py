from abc import ABC, abstractmethod
from typing import Any, Dict
import openai
import os

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, api_key: str = None):
        self.name = name
        self.role = role
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError('OPENAI_API_KEY not found')
        openai.api_key = self.api_key
    
    @abstractmethod
    def execute(self, input_data: Any) -> Dict[str, Any]:
        pass
    
    def call_llm(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': self.role},
                    {'role': 'user', 'content': prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f' LLM error: {e}')
            return ''
