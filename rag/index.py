from dotenv import load_dotenv
import os

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

load_dotenv(Path(__file__).resolve().parent / ".env")
pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(str(pdf_path))

docs = loader.load()
# print(docs[8])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(docs)

embedding_model = None
providers = []

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        providers.append(("gemini", GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2",
            google_api_key=gemini_key,
        )))
except Exception as exc:
    print(f"Gemini embeddings unavailable: {exc}")

# from langchain_openai import OpenAIEmbeddings
# providers.append(("openai", OpenAIEmbeddings(model="text-embedding-3-large")))

vector_store = None
for provider_name, provider_embedding in providers:
    try:
        vector_store = QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=provider_embedding,
            collection_name="learning_rag",
            url="http://localhost:6333",
        )
        print(f"Indexed successfully with {provider_name} embeddings.")
        break
    except Exception as exc:
        print(f"{provider_name} embedding failed: {exc}")
        if provider_name == "openai":
            raise
