from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

class LLM:

    def __init__(self, model="llama3:8b"):
        self.model = ChatOllama(
            model=model,
            temperature=0,
            format="json" # forces JSON output (new feature)
        )
    
    def generate(self, prompt: str) -> str:
        response = self.model.invoke([
            HumanMessage(content=prompt)
        ])
        return response.content