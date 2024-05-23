import streamlit as st
from llama_index.core import ServiceContext, Document
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader
import os
from dotenv import load_dotenv
from connector import store_user_info
import speech_recognition as sr
import streamlit.components.v1 as components

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext



chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("data_collection")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


@st.cache_resource(show_spinner=True)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()

        system_prompt = """
        Your name is Alex. You are an expert QnA chatbot for TIPS-G, a company. Your task is to provide answers to questions based on the information in a given PDF book.
        When answering, follow these guidelines:

        1. Provide concise answers in 1 to 2 sentences (as short as you can).
        2. Use the user's name in your responses when appropriate.
        3. If the user's question cannot be answered based on the provided context, politely inform them and suggest rephrasing or providing additional context.
        4. Remember conversation history, as the user can ask follow-up questions.
        """
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, max_tokens=500, system_prompt=system_prompt))
        index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)

    return index
