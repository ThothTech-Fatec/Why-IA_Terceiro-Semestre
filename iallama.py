from gtts import gTTS
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from Functions import *

# Funções mapeadas para facilitar a chamada do modelo
mapa_funcoes = {
    'cumprimentar_usuario': cumprimentar_usuario,
    'buscar_medicamentos': buscar_medicamentos,
    'adicionar_ao_carrinho': adicionar_ao_carrinho,
    'consultar_estoque': consultar_estoque,
    'ver_carrinho': ver_carrinho,
    'finalizar_compra': finalizar_compra,
    'listar_todos_medicamentos': listar_todos_medicamentos,
    'verificar_receita': verificar_receita,
    'remover_do_carrinho': remover_do_carrinho,
    'mostrar_todas_funcoes': mostrar_todas_funcoes
}

def gerar_audio(texto):
    tts = gTTS(text=texto, lang='pt')
    tts.save("PharmacIA.mp3")
    return "PharmacIA.mp3"

def gerar_prompt_para_decisao(question):
    prompt = f"""
    Você é um assistente inteligente que executa funções para ajudar o usuário com medicamentos. Aqui estão as funções disponíveis e o que elas fazem:

    1. cumprimentar_usuario: Saudação ao usuário.
    2. buscar_medicamentos: Busca por medicamentos com base em uma consulta.
    3. adicionar_ao_carrinho: Adiciona um medicamento ao carrinho de compras.
    4. consultar_estoque: Consulta a quantidade de medicamentos no estoque.
    5. ver_carrinho: Exibe os medicamentos no carrinho.
    6. finalizar_compra: Finaliza a compra de medicamentos.
    7. listar_todos_medicamentos: Lista todos os medicamentos disponíveis.
    8. verificar_receita: Verifica se é necessário receita para comprar um medicamento.
    9. remover_do_carrinho: Remove um medicamento do carrinho de compras.
    10. mostrar_todas_funcoes: Mostra todas as funções que o usuário pode usar

    A pergunta do usuário é: "{question}"

    Com base na pergunta, decida qual função deve ser chamada e os parâmetros necessários para essa função. Responda com o formato:

    Função: nome_da_funcao, Parâmetros: [param1, param2, ...]

    Se não houver parâmetros, escreva "Parâmetros: []".

    Se não houver nenhuma função que se encaixe no oque o usuário disse, execute a função: mostrar_todas_funcoes
    """
    return prompt

def OllamaQuestion(question):
    ollama_model = OllamaLLM(model="llama3.1:latest", base_url="http://localhost:11434")
    template = PromptTemplate(input_variables=["input_text"], template="{input_text}")
    llm_chain = template | ollama_model
    prompt = gerar_prompt_para_decisao(question)
    resposta = llm_chain.invoke({"input_text": prompt})

    if "Função" in resposta and "Parâmetros" in resposta:
        try:
            funcao_str = resposta.split("Função:")[1].split(",")[0].strip()
            parametros_str = resposta.split("Parâmetros:")[1].strip()
            funcao = mapa_funcoes.get(funcao_str.lower(), None)

            if funcao:
                parametros_str = parametros_str.strip("[]").strip()
                if parametros_str:
                    parametros_lista = [p.strip().strip('"').strip("'").replace("\\", "") for p in parametros_str.split(",")]
                    return funcao(*parametros_lista)
                else:
                    return funcao()
        except Exception as e:
            return "Erro ao processar a resposta do modelo."
    
    resposta_gerada = llm_chain.invoke({"input_text": question})
    return resposta_gerada
