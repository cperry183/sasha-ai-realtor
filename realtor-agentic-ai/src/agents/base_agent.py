from abc import ABC, abstractmethodfrom typing import Dict, Any, Optional
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

class BaseAgent(ABC):
def __init__(self, model_name: str = "gpt-4"):
self.llm = ChatOpenAI(
temperature=0.7,
model_name=model_name,
api_key=os.getenv("OPENAI_API_KEY")
)

@abstractmethod
async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
pass

def create_chain(self, template: str) -> LLMChain:
prompt = PromptTemplate(
input_variables=["input"],
template=template
)
return LLMChain(llm=self.llm, prompt=prompt)
