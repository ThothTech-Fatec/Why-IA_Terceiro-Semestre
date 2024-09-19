from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def OllamaQuestion(question):
    # Inicializa o modelo do Ollama
    ollama_model = OllamaLLM(model="llama3.1:8b", base_url="http://localhost:11434")

    # Cria um template de prompt
    template = PromptTemplate(
        input_variables=["input_text"],
        template="Você é um assistente especialista em inteligência artificial. Pergunta: {input_text} Resposta: "
    )

    # Encadeia o template com o modelo
    llm_chain = template | ollama_model

    # Obtém a resposta do modelo
    resposta = llm_chain.invoke({"input_text": question})
    
    return resposta
