from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import START, StateGraph, END
from openai import OpenAI

load_dotenv()

client = OpenAI()

class State(TypedDict):
    user_query: str
    llm_response: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print("\n Chatbot function called with state:", state)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": state["user_query"]},
        ],
    )

    state["llm_response"] = response.choices[0].message.content
    return state

def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    print("\n Evaluate_response function called with state:", state)
    if state["llm_response"] is None:
        return "endnode"

    return "chatbot_gemini"

def chatbot_gemini(state: State):
    print("\n Chatbot_gemini function called with state:", state)
    response = client.chat.completions.create(
        model="gemini-1.5",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": state["user_query"]},
        ],
    )

    state["llm_response"] = response.choices[0].message.content
    return state

def endnode(state: State):
    print("\n Endnode function called with state:", state)
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", "evaluate_response")

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "What is the capital of France?"}))   
print("\n\nUpdated state after graph invocation:", updated_state)