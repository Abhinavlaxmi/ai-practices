import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from qdrant_client import QdrantClient

load_dotenv(Path(__file__).resolve().parent / ".env")

openai_client = OpenAI()

embedding_model = None
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        embedding_model = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2",
            google_api_key=gemini_key,
        )
except Exception as exc:
    print(f"Gemini embeddings unavailable: {exc}")

if embedding_model is None:
    from langchain_openai import OpenAIEmbeddings

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

collection_name = "learning_rag"
qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")

try:
    qdrant_client = QdrantClient(url=qdrant_url)
    collections = qdrant_client.get_collections().collections

    if not any(collection.name == collection_name for collection in collections):
        print(f"Qdrant collection '{collection_name}' was not found at {qdrant_url}.")
        print("Run the indexing script first:")
        print("  python rag/index.py")
        raise SystemExit(1)

    vector_db = QdrantVectorStore.from_existing_collection(
        url=qdrant_url,
        collection_name=collection_name,
        embedding=embedding_model,
    )
except Exception as exc:
    print(f"Could not connect to Qdrant at {qdrant_url}: {exc}")
    print("Make sure Qdrant is running and the collection exists.")
    raise SystemExit(1) from exc

user_query = input("Enter your query: ")

search_results = vector_db.similarity_search(user_query, k=5)  # Retrieve top 5 similar documents

context = "\n\n\n".join([f"Page content: {result.page_content}" for result in search_results])

system_prompt = f"""
You are a helpful assistant that provides information based on the context provided. 
Use the context to answer the user's query. If the context does not contain relevant information, 
respond with "I don't know.

you should only answer the user based on following context: {context}"""

response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
)

print(f"Response: {response.choices[0].message.content}")