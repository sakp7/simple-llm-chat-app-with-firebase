import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
import time

# Streamlit app title
st.title("AI Assistant Chat")

# Firebase Firestore setup
project_id='qrproject-e7f3e'
session_id = 'session_1'
collection_name = 'llm_history'

st.success("Connection live")
client = firestore.Client(project=project_id)

# Initializing Firestore chat message history
chat_history = FirestoreChatMessageHistory(
    session_id=session_id,
    collection=collection_name,
    client=client
)

llm = ChatGroq(groq_api_key=st.secrets['api_key'])

# system message at the start of the chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    chat_history.add_message(SystemMessage(content='You are an AI assistant'))

# Function to handle user input and generate AI response with streaming effect
def handle_query(user_input):
    chat_history.add_user_message(user_input)
    response = llm.invoke(chat_history.messages)
    chat_history.add_ai_message(response.content)
    return response.content

# Streaming function to display word-by-word responses
def stream_response(response_text, container):
    words = response_text.split()
    response = ""
    for word in words:
        response += word + " "
        with container:
            st.write(response.strip())
        time.sleep(0.1)

# Main chat container
chat_placeholder = st.container()

# Chat history rendering
with chat_placeholder:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(message["content"])

# User input box (bottom)
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        response_container = st.empty() 

    time.sleep(0.5) 

    # stream response
    ai_response = handle_query(user_input)
    stream_response(ai_response, response_container)

    # Adding AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
