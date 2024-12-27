import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages.tool import ToolMessage

from chatbot import app
from tools import customer_db

st.set_page_config(
    page_title="Flower Shop Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


if "message_history" not in st.session_state:
    st.session_state.message_history = [
        AIMessage(content="Hey! I am a Petalia. How can I help you?")
    ]

if "tools" not in st.session_state:
    st.session_state.tools = {}


left_col, main_col, right_col = st.columns([1, 2, 1])

# 1. buttons for chat - clear button
with left_col:
    if st.button("Clear chat"):
        st.session_state.message_history = []

    st.markdown("## Customer")
    st.write(customer_db)


# 2. Chat history and input field

with main_col:
    user_input = st.chat_input("Type here...")

    if user_input:
        st.session_state.message_history.append(HumanMessage(content=user_input))

        response = app.invoke(
            {"messages": st.session_state.message_history},
        )

        st.session_state.message_history = response["messages"]

    for message in reversed(st.session_state.message_history):
        if isinstance(message, HumanMessage):
            if message.content:
                message_box = st.chat_message("user")
                message_box.markdown(message.content)
        elif isinstance(message, AIMessage):
            if message.content:
                message_box = st.chat_message("assistant")
                message_box.markdown(message.content)
        elif isinstance(message, ToolMessage):
            st.session_state.tools = {"data": message.content, "tool": message.name}
            if message.name:
                message_box = st.chat_message("ai")
                message_box.markdown(f"Calling tool: {message.name}")


# 3. State variables

with right_col:
    st.markdown("## State Management")
    st.write(st.session_state.tools)
