import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

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


left_col, main_col, right_col = st.columns([1, 2, 1])

# 1. buttons for chat - clear button
with left_col:
    if st.button("Clear chat"):
        st.session_state.message_history = []


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
            message_box = st.chat_message("user")
        else:
            message_box = st.chat_message("assistant")
        message_box.markdown(message.content)


# 3. State variables

with right_col:
    st.write(customer_db)
    st.json(st.session_state.message_history)
