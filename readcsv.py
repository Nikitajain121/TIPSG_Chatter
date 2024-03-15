from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain.docstore.document import Document
import pandas as pd
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_csv(df, chat_history):
    csv_text = df.to_csv(index=False)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(csv_text)

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
        st.write("No text found in the uploaded CSV file.")

