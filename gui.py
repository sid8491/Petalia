import streamlit as st

from vector_store import FlowerShopVectorStore

st.set_page_config(
    page_title="Flower Shop Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

vector_store = FlowerShopVectorStore()

if "message_history" not in st.session_state:
    st.session_state.message_history = [
        {"content": "Hey! I am a Petalia. How can I help you?", "type": "assistant"}
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
        related_questions = vector_store.query_inventories(user_input)
        st.session_state.message_history.append(
            {
                "content": user_input,
                "type": "user",
            }
        )
        st.session_state.message_history.append(
            {
                "content": related_questions,
                "type": "assistant",
            }
        )

    for message in reversed(st.session_state.message_history):
        message_box = st.chat_message(message["type"])
        message_box.markdown(message.get("content", ""))


# 3. State variables

with right_col:
    st.text(st.session_state.message_history)
