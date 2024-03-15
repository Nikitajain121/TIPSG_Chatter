import os
import streamlit as st
from streamlit_ace import st_ace
from pdfplumber import PDF
from docx import Document as DocxDocument
import textract
import pandas as pd
from features import process_document, process_webpage, display_chat_history
from readcsv import process_csv
import requests
from io import BytesIO

os.environ["OPENAI_API_KEY"] = ""

def main():
    st.title("Document Query App")

    upload_option = st.radio("Choose input method", ["Upload File", "Enter URL", "Upload CSV"])

    chat_history = []

    if upload_option == "Upload File":
        file = st.file_uploader("Upload a file", type=["pdf", "txt", "docx"])
        if file is not None:
            if file.type == "application/pdf":
                process_document(file, chat_history)
            elif file.type == "text/plain":
                process_document(file.read().decode("utf-8"), chat_history)
            elif file.type in {"application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"}:
                doc = DocxDocument(file)
                full_text = "\n".join([p.text for p in doc.paragraphs])
                process_document(full_text, chat_history)
    elif upload_option == "Enter URL":
        url = st.text_input("Enter the URL")
        if url:
            if url.endswith(".pdf"):
                response = requests.get(url)
                pdf_file = BytesIO(response.content)
                process_document(pdf_file, chat_history)
            else:
                process_webpage(url, chat_history)
    elif upload_option == "Upload CSV":
        csv_file = st.file_uploader("Upload a CSV file", type="csv")
        if csv_file is not None:
            df = pd.read_csv(csv_file)
            process_csv(df, chat_history)


    display_chat_history(chat_history)

if __name__ == "__main__":
    main()
