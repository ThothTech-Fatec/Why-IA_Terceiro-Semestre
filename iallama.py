from langchain_ollama import Ollama
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Define o modelo Ollama LLaMA
llm = Ollama(model="llama3", base_url="http://localhost:11434")

# Defina um prompt
prompt_template = """
Você é um assistente especialista em inteligência artificial.
Pergunta: {question}
Resposta:
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["question"])

#

