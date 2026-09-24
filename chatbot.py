import os 
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# load the env variables
load_dotenv()

# streamlit page setup
st.set_page_config(
    page_title="Chatbot",
    page_icon="🦾",
    layout="centered",
)

st.title("💬 Marty Chatbot")

# initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
    temperature = 0.0,
)

# input box
user_prompt = st.chat_input("Ask Chatbot ...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = llm.invoke(
        input=[{"role": "system", "content": "You are a helpful assistant"}, *st.session_state.chat_history]
    )

    # Estrai il testo, gestendo sia stringhe semplici che liste di blocchi
    if isinstance(response.content, list):
        assistant_response = " ".join(
            block.get("text", "") for block in response.content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    else:
        assistant_response = response.content
    
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)