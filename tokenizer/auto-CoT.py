from dotenv import load_dotenv
from openai import OpenAI

import json

load_dotenv()

client = OpenAI(
    api_key="AIzaSyBj_l_zMC8a7I_-XjLIoejAQ3gXRA5jyiA",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
    You are a helpful assistant that answers questions in a detailed manner. 
    You should provide comprehensive and informative responses to the user's queries.
    You work on START, PLAN and OUTPUT steps.
    You need to first analyze the question and break it down into smaller steps (START).
    Then, you need to create a plan to answer the question (PLAN).
    Finally, you need to execute the plan and provide the final answer (OUTPUT).

    Rules:
    1. Strictly follow the given JSON format.
    2. Only run one step at a time.
    3. The sequence of steps is START(where user gives the question), PLAN(that can be multiple times) and finally OUTPUT(which is going to display the final answer).
    4. Always follow the START, PLAN, OUTPUT steps in order.
    
    Output JSON Format:
    {"step":"START"|"PLAN"|"OUTPUT", "content": "string"}

    Example:
    START: Hey can you solve 3+4*4+6-45+32/4
    PLAN: {"step": "PLAN", "content": "It seems you are trying to solve a mathematical expression."}
    PLAN: {"step": "PLAN", "content": "Looking at theproblem, we should solve this using BODMAS rule."}
    PLAN: {"step": "PLAN", "content": "Yes, BODMAS is correct things to be done here."}
    PLAN: {"step": "PLAN", "content": "Divide 32 by 4 to get 8."}
    PLAN: {"step": "PLAN", "content": "Multiply 4 by 4 to get 16."}
    PLAN: {"step": "PLAN", "content": "Add 3 and 16 to get 19."}
    PLAN: {"step": "PLAN", "content": "Add 6 to 19 to get 25."}
    PLAN: {"step": "PLAN", "content": "Subtract 45 from 25 to get -20."}
    OUTPUT: {"step": "OUTPUT", "content": "The final answer is -20."}
    """

print("\n\n\n")

message_history = [
    {'role': 'system', 'content': SYSTEM_PROMPT},
]

user_input = input("Enter your question: ");

message_history.append({'role': 'user', 'content': user_input})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_content = response.choices[0].message.content
    message_history.append({'role': 'assistant', 'content': raw_content})

    parsed_content = json.loads(raw_content)

    if parsed_content['step'] == 'START':
        print("🔥", parsed_content['content'])
        continue

    if parsed_content['step'] == 'PLAN':
        print("🧠", parsed_content['content'])
        continue

    if parsed_content['step'] == 'OUTPUT':
        print("✅", parsed_content['content'])
        break


# response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     messages=[
#         {
#             "role": "user",
#             "content": "Hi there! This is Michael Jackson. Who are you?"
#         }
#     ]
# )

# print(response.choices[0].message.content)