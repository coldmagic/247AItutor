import os
import json
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DATA_DIRECTORY = os.path.join(os.getcwd(), "data_feed")
PERSIST_DIRECTORY = "chroma_data"
COLLECTION_NAME = "high_school_pdf_data"

client = chromadb.Client(settings=Settings(chroma_db_impl="duckdb+parquet", persist_directory=PERSIST_DIRECTORY))
model = SentenceTransformer('paraphrase-distilroberta-base-v1')
embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY)
collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedding_function)

def load_pdfs():
    pdf_folder = DATA_DIRECTORY
    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    return pdf_files

pdf_file_paths = load_pdfs()
pdf_loaders = [PyPDFLoader(pdf_path) for pdf_path in pdf_file_paths]

def get_retrieval_qa_result(question, context):
    langchain_question = {"q": question, "context": context}

    # Get embeddings from LangChain
    langchain_embedding = embedding_function.embed_query(langchain_question)

    # Use ChromaDB to retrieve the most similar document
    most_similar_document_id, _ = collection.query(query_embeddings=langchain_embedding, n_results=1, where={})[0]

    # Load the retrieved document
    document_path = os.path.join(DATA_DIRECTORY, f"{most_similar_document_id}.pdf")
    document_loader = PyPDFLoader(document_path)
    document = document_loader.load()

    # Perform question-answering using LangChain
    openai = OpenAI(api_key=OPENAI_API_KEY)
    langchain_response = openai.answer_text({"question": question, "document": document})

    return {
        "question": question,
        "answer": langchain_response["answer"],
        "source_document": most_similar_document_id
    }
