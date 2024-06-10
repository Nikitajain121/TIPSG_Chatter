import streamlit as st

from llama_index.core import ServiceContext, Document
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader
import os
from dotenv import load_dotenv
from connector import store_user_info
import streamlit.components.v1 as components
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb
from llama_index.core import StorageContext

from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,ServiceContext,PromptTemplate

from dataloader import load_data

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

MAX_QUESTIONS = 15  # Maximum number of questions allowed per session

index = load_data()
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# Initialize the session state with an empty list for messages and num_questions
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_greeting = "Hi, I'm Alex, your AI assistant. How can I assist you today?"
    st.session_state.messages.append({"role": "ALEX", "content": initial_greeting})

if "num_questions" not in st.session_state:
    st.session_state.num_questions = 0

st.title("Alex AI - The TIPS-G Chatbot")

with st.form("user_info_form"):
    st.write("Please provide your name, contact:")
    user_name = st.text_input("Name:")
    contact = st.text_input("Contact:")
    mail_id = st.text_input("Email:")
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        store_user_info(user_name, contact, mail_id)
        st.session_state.messages.append({"role": "ALEX", "content": f"Thanks for providing your information, {user_name}!"})

# Function to summarize responses
def summarize_response(response, sentence_count=3):
    parser = PlaintextParser.from_string(response, Tokenizer('english'))
    summarizer = LsaSummarizer()  # Or TextRankSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return ' '.join([str(sentence) for sentence in summary])

# Custom CSS for responsive design
st.markdown("""
    <style>
    .stApp {
        overflow: hidden;
    }
    .chat-bubble {
        background-color: #ADD8E6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        word-wrap: break-word;
    }
    .bot-bubble {
        background-color: #FFC0CB;
    }
    .chat-message {
        font-size: 16px;
    }
    .chat-message-user::before {
        content: "👤";
        margin-right: 10px;
        font-size: 1.5em;
    }
    .chat-message-alex::before {
        content: "🤖";
        margin-right: 10px;
        font-size: 1.5em;
    }
    @media (max-width: 600px) {
        .chat-bubble, .bot-bubble {
            padding: 5px;
            font-size: 14px;
        }
        .stTextInput, .stButton {
            width: 100%;
            font-size: 14px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-bubble">
                    <span class="chat-message chat-message-user">{message["content"]}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-bubble bot-bubble">
                    <span class="chat-message chat-message-alex">{message["content"]}</span>
                </div>
            """, unsafe_allow_html=True)

# Function to handle text input submission
def submit():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ""

# Input for user question
input_container = st.container()
with input_container:
    text_input = st.text_input(" ", key="widget", on_change=submit, placeholder="Your question...", label_visibility='collapsed')

    prompt = st.session_state.user_input if "user_input" in st.session_state else None

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.num_questions += 1

        if st.session_state.num_questions > MAX_QUESTIONS:
            st.warning(f"You have reached the maximum number of questions allowed in this session. For more details, you can contact us at +91 7023340831, or visit us at Chanda Tower, Girnar Colony, Gandhi Path Road, Vaishali Nagar, Jaipur -302021")
        else:
            with chat_container:
                st.markdown(f"""
                    <div class="chat-bubble">
                        <span class="chat-message chat-message-user">{prompt}</span>
                    </div>
                """, unsafe_allow_html=True)

                with st.spinner("Thinking..."):
                    response = chat_engine.chat(prompt)
                    response.response = " " + response.response

                    # Summarize if too long
                    max_words = 35
                    if len(response.response.split()) > max_words:
                        summarized_response = summarize_response(response.response, sentence_count=2)
                        st.session_state.messages.append({"role": "ALEX", "content": summarized_response})
                        st.markdown(f"""
                            <div class="chat-bubble bot-bubble">
                                <span class="chat-message chat-message-alex">{summarized_response}</span>
                            </div>
                        """, unsafe_allow_html=True)
                    else:  # Response is within the word limit
                        st.session_state.messages.append({"role": "ALEX", "content": response.response})
                        st.markdown(f"""
                            <div class="chat-bubble bot-bubble">
                                <span class="chat-message chat-message-alex">{response.response}</span>
                            </div>
                        """, unsafe_allow_html=True)

if st.button("Clear Chat"):
    st.session_state.clear()
    st.experimental_rerun()
