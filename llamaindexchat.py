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

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

@st.cache_resource(show_spinner=True)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        # Customize the system prompt for the chatbot's persona
        system_prompt = """
        You are an expert QnA chatbot for TIPS-G, a company. Your task is to provide answers to questions based on the information in a given PDF book.
        When answering, follow these guidelines:

        1. Provide concise answers in 1 to 3 sentences.
        2. Greet the user and ask for their name at the beginning of the conversation.
        3. Use the user's name in your responses when appropriate.
        4. If the user's question cannot be answered based on the provided context, politely inform them and suggest rephrasing or providing additional context.
        5. Remember conversation history, as the user can ask follow-up questions.
        """
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4", temperature=0.5, max_tokens=500, system_prompt=system_prompt))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    return index

index = load_data()
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# Initialize the session state with an empty list for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set up the chatbot interface
st.title("TIPS-G Chatbot")
st.markdown("Ask me anything about TIPS-G!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=USER_AVATAR if message["role"] == "user" else BOT_AVATAR):
        st.write(message["content"])

# Input for user question
prompt = st.chat_input("Your question:")

# Generate response if new input is given
if prompt:
    # Save user input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display the user's input
    with st.chat_message("user", avatar=USER_AVATAR):
        st.write(prompt)

    # Generate assistant response
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.response})

# Clear chat history button
if st.button("Clear Chat"):
    st.session_state.messages = []
