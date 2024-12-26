import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from tools import query_knowledge_base, search_for_product_recommendations

load_dotenv()

prompt = """#Purpose
You are customer service chatbot for a flower shop company. Your name is Petalia.
You can help the customer acheive the goals listed below.

#Goals
1. Answer questions the user might have relating to services offered
2. Recommed products to the user based on their preferences

#Tone
* Helpful and friendly
* Use flower related puns or gen-z emojis to keep things light and fun
* Dont use words like 'according to our records' or 'as per our database' or 'as per the knowledge base'
* Use bullet points whenever possible (if you think it will make response better)"""

chat_template = ChatPromptTemplate.from_messages(
    [("system", prompt), ("placeholder", "{messages}")]
)

tools = [query_knowledge_base, query_knowledge_base]

llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
llm_with_prompt = chat_template | llm.bind_tools(tools=tools)


def call_agent(message_state: MessagesState):
    response = llm_with_prompt.invoke(message_state)
    return {"messages": [response]}


tool_node = ToolNode(tools)
graph = StateGraph(MessagesState)


def is_there_tool_calls(state: MessagesState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END


graph.add_node("agent", call_agent)
graph.add_node("tools", tool_node)

graph.add_conditional_edges("agent", is_there_tool_calls)
graph.add_edge("tools", "agent")

graph.set_entry_point("agent")

checkpointer = MemorySaver()

app = graph.compile(checkpointer=checkpointer)

# to export the graph as an image, you can use the following code:
png_data = app.get_graph().draw_mermaid_png()
with open("output_graph.png", "wb") as f:
    f.write(png_data)
