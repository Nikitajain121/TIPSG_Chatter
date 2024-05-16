import streamlit as st
from llama_index.core import ServiceContext, Document
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, PromptTemplate
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
@st.cache_resource(show_spinner=True)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4", temperature=0.5, max_tokens=500, system_prompt = "You are an expert QnA chatbot for TIPS-G, a company. Your task is to provide answers to questions based on the information in a given PDF book. When answering, follow these guidelines:\n\n1. Provide concise answers in 1 to 3 sentences.\n2. Greet the user and ask for their name at the beginning of the conversation.\n3. Use the user's name in your responses when appropriate.\n4. If the user's question cannot be answered based on the provided context, politely inform them and suggest rephrasing or providing additional context.Also remember conversation history, as user can a follow-up question."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    return index

index = load_data()
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# Initialize the session state with an empty list for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("Your question"):
    # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)