from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()
client = Client(
    host="http://localhost:11434"
)

@app.get("/")
def homePage():
    return{"message": "Welcome to FastAPI with Ollama!"}

@app.get("/contact")
def contactPage():
    return{"email": "abhinavlaxmi@gmail.com", "phone": "+91-9012345678"}

@app.post("/model/chat")
def chatWithOurModel(message: str = Body(..., description="The message to send to the model")):
    response = client.chat(
        model="gemma:2b",
        messages=[
            {"role":"user", "content": message}
        ]
    )
    return {"response": response.message.content}