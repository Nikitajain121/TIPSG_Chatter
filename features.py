from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.qa_with_sources.loading import (
    load_qa_with_sources_chain,
    BaseCombineDocumentsChain,
)
from langchain.tools.base import BaseTool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import requests
import io
from io import BytesIO
import streamlit as st
from pdfplumber import PDF
import textract
import csv
import pandas as pd
from webask import get_response, get_vectorstore_from_url

def process_document(document, chat_history):
    if isinstance(document, (PDF, BytesIO)):
        raw_text = ""
        if isinstance(document, PDF):
            for i, page in enumerate(document.pages):
                content = page.extract_text()
                if content:
                    raw_text += content
        else:
            with PDF(document) as pdf:
                for i, page in enumerate(pdf.pages):
                    content = page.extract_text()
                    if content:
                        raw_text += content
    elif isinstance(document, str):
        raw_text = document

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=200, length_function=len
    )
    texts = text_splitter.split_text(raw_text)

    if texts:
        embeddings = OpenAIEmbeddings()
        document_search = FAISS.from_texts(texts, embeddings)

        chain = load_qa_chain(OpenAI(), chain_type="stuff")

        query = st.text_input("Enter your query")
        if st.button("Submit Query"):
            docs = document_search.similarity_search(query)
            response = chain.run(input_documents=docs, question=query)
            chat_history.append((query, response))
            st.write(response)
    else:
        st.write("No text found in the uploaded document.")


def process_webpage(url, chat_history):
    from webask import get_response, get_vectorstore_from_url

    if url:
        if url.endswith(".pdf"):
            response = requests.get(url)
            pdf_file = BytesIO(response.content)
            process_document(pdf_file, chat_history)
        else:
            if "vector_store" not in st.session_state:
                st.session_state.vector_store = get_vectorstore_from_url(url)

            query = st.text_input("Enter your query")
            if st.button("Get Answers"):
                if query:
                    response = get_response(query)
                    chat_history.append((query, response))
                    st.write(response)


def display_chat_history(chat_history):
    st.subheader("Chat History")
    for i, (query, response) in enumerate(chat_history, start=1):
        st.write(f"Query {i}: {query}")
        st.write(f"Response {i}: {response}")
        st.write("--" * 20)
