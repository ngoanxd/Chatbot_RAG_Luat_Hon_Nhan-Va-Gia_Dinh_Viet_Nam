from langchain_ollama import OllamaLLM
from config import LLM_MODEL

def get_llm():
    return OllamaLLM(model=LLM_MODEL)
