from datasets import load_dataset
from langchain_community.document_loaders import DataFrameLoader
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain.schema import Document
from langchain_ollama import OllamaLLM
import numpy as np
from langchain.prompts import PromptTemplate


def OllamaQ(query):

    # Carregando dataset
    dataset = load_dataset("KazeV/Eletronics_Assist", split="train")
    print("Colunas disponíveis no dataset:", dataset.column_names)

    # Convertendo o dataset para pandas
    data = dataset.to_pandas()

    # Extraindo as colunas necessárias
    docs = data[['Q', 'A']]

    # Criando objetos Document a partir dos dados com todas as colunas nos metadados
    documents = [
        Document(
            page_content=row['Q'],  # Usando o texto de questão como conteúdo principal
            metadata={
                "A": row['A']
            }
        ) for _, row in docs.iterrows()
    ]

    # Usando HuggingFaceEmbeddings para gerar embeddings
    embedder = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Criando cliente do Qdrant
    qdrant_client = QdrantClient(":memory:")  # Armazenamento em memória

    # Obter o tamanho dos vetores corretamente
    embedding_example = np.array(embedder.embed_query("test"))
    vector_size = embedding_example.shape[0]

    # Criar uma nova coleção no Qdrant para armazenar os vetores
    qdrant_client.create_collection(
        collection_name="chatbot",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

    # Inserindo os documentos com embeddings
    qdrant = QdrantVectorStore.from_documents(
        documents=documents,  # Lista de objetos Document
        embedding=embedder,
        location=":memory:",  # Local mode with in-memory storage only
        collection_name="chatbot",
    )

    # Busca no Qdrant com base na consulta passada como argumento
    results = qdrant.similarity_search(query, k=3)

    # Inicializando o modelo Llama
    ollama_model = OllamaLLM(model="llama3.2:latest", base_url="http://localhost:11434")

    # Gerando resposta usando Llama
    if results:  # Verifique se existem resultados
        # Concatena os conteúdos dos resultados para o contexto e os metadados de todos os resultados
        context = " ".join([result.page_content for result in results])  # Concatena os prompts
        A = " ".join([result.metadata["A"] for result in results])  # Concatena as respostas

        # Criando o template do prompt
        template = PromptTemplate(
            input_variables=["input_text", "context", "A"],
            template=(
            "Você é um assistente virtual especializado em suporte técnico para uma loja de eletrônicos. "
            "A seguir está o contexto relevante extraído de consultas anteriores: {context}. "
            "Com base apenas nesse contexto, e nas informações adicionais abaixo, "
            "responda de forma clara, direta e sem adicionar nada extra. "
            "Se a pergunta envolver uma quantidade ou valor, forneça apenas o valor numérico especificado na coluna A: {A}. "
            "Por favor, mantenha suas respostas precisas e de forma mais carinhosa com o cliente. Pergunta: {input_text}"
            )
        )

        # Formatando o prompt com o contexto, pergunta e respostas concatenadas
        formatted_prompt = template.format(
            input_text=query,
            context=context,
            A=A
        )

        # Gerando a resposta
        response = ollama_model.invoke(formatted_prompt)

        print("Resposta do Llama:")
        print(response)
        return response  

    else:
        print("Nenhum resultado encontrado.")
