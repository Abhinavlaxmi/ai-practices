from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import START, StateGraph, END
from langchain.chat_models import init_chat_model

load_dotenv()
llm = init_chat_model(model_name="gpt-4o", model_provider="openai")

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    print("\n Chatbot function called with state:", state)
    return {"messages": [response]}

def sampleModal(state: State):
    print("\n SampleModal function called with state:", state)
    return {"messages": "This message from sampleModal function"}

graph_builder = StateGraph(State)


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sampleModal", sampleModal)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sampleModal")
graph_builder.add_edge("sampleModal", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hey, This is a test message"]}))
print("\n\nUpdated state after graph invocation:", updated_state)