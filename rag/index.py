from dotenv import load_dotenv
import os

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()
pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(str(pdf_path))

docs = loader.load()
# print(docs[8])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(docs)
print(os.getenv("OPENAI_API_KEY"))
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="learning_rag",
    url="http://localhost:6333",
)
