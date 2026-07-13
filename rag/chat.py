from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model,
)

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