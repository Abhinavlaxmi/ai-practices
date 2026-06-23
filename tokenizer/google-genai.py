from google import genai

client = genai.Client(
    api_key="AIzaSyBj_l_zMC8a7I_-XjLIoejAQ3gXRA5jyiA"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the capital of France? Please provide a detailed answer.",
)

print(response.text)