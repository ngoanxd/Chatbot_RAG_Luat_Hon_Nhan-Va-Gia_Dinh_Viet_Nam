from langchain_community.llms import Ollama
from config import *

llm = Ollama(model=LLM_MODEL)