from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="AIzaSyBj_l_zMC8a7I_-XjLIoejAQ3gXRA5jyiA",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": "Hi there! This is Michael Jackson. Who are you?"
        }
    ]
)

print(response.choices[0].message.content)