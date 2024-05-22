import streamlit as st
from llama_index.core import ServiceContext, Document
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, PromptTemplate
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader
import os
from dotenv import load_dotenv
from connector import store_user_info
import speech_recognition as sr
import streamlit.components.v1 as components
from llama_index.core import Settings
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

MAX_QUESTIONS = 15  # Maximum number of questions allowed per session

@st.cache_resource(show_spinner=True)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()

        system_prompt = """
        Your name is Alex. You are an expert QnA chatbot for TIPS-G, a company. Your task is to provide answers to questions based on the information in a given PDF book.
        When answering, follow these guidelines:

        1. Provide concise answers in 1 to 2 sentences ( as short as u cans)
        2. Use the user's name in your responses when appropriate.
        3. If the user's question cannot be answered based on the provided context, politely inform them and suggest rephrasing or providing additional context.
        4. Remember conversation history, as the user can ask follow-up questions.
        """
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, max_tokens=300, system_prompt=system_prompt))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)

    return index

index = load_data()
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# Initialize the session state with an empty list for messages and num_questions
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_greeting = "Hi, I'm Alex, your AI assistant. How can I assist you today? May I know your name?"
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

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=USER_AVATAR if message["role"] == "user" else BOT_AVATAR):
            if message["role"] == "user":
                st.markdown(f"""
                    <div style="background-color: #FFFFE0; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                        <span style="font-size: 16px;">{message["content"]}</span>
                        <span style="font-size: 16px; font-weight: bold; margin-left: 10px;"> </span>
                        <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCAxMDAlIj48cGF0aCBmaWxsPSIjMDAwMDAwIiBkPSJNMjUuNjU2MjUgMTYuMjY0NjkgTDI0LjYyNjU2IDI3Ljk3MjE5TDI2LjkyNjU2IDMwLjY4MjE5TDI2Ljg2NjU2IDMwLjY4MjE5TDI1LjY1NjI1IDE2LjI2NDY5eiIvPjwvc3ZnPg==" alt="Chat Bubble Tail" width="20" height="20" style="margin-left: 10px; position: relative; top: -2px;">
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background-color: #FFC0CB; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                        <span style="font-size: 16px; font-weight: bold; margin-right: 10px;">{message["role"]} </span>
                        <span style="font-size: 16px;">{message["content"]}</span>
                        <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCAxMDAlIj48cGF0aCBmaWxsPSIjMDAwMDAwIiBkPSJNMjUuNjU2MjUgMTYuMjY0NjkgTDI0LjYyNjU2IDI3Ljk3MjE5TDI2LjkyNjU2IDMwLjY4MjE5TDI2Ljg2NjU2IDMwLjY4MjE5TDI1LjY1NjI1IDE2LjI2NDY5eiIvPjwvc3ZnPg==" alt="Chat Bubble Tail" width="20" height="20" style="margin-left: 10px; position: relative; top: -2px;">
                    </div>
                """, unsafe_allow_html=True)

# Voice Input Feature
r = sr.Recognizer()
microphone = sr.Microphone()

def listen_for_audio():
    with microphone as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)

# Input for user question (text or voice)
# Input for user question (text or voice)
# Input for user question (text or voice)
# Input for user question (text or voice)
input_container = st.container()
with input_container:
    col1, col2 = st.columns([10, 1])
    with col1:
        text_input = st.text_input(" ", key="user_input", placeholder="Your question...")

    with col2:
        voice_input = st.button("🎙️", key="voice_input_btn")

    if voice_input:
        prompt = listen_for_audio()
    elif text_input:
        prompt = text_input
    else:
        prompt = None

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.num_questions += 1

        if st.session_state.num_questions > MAX_QUESTIONS:
            st.warning(f"You have reached the maximum number of questions allowed in this session. For more details, you can contact us at +91 7023340831, or visit us at Chanda Tower, Girnar Colony, Gandhi Path Road, Vaishali Nagar, Jaipur -302021")
        else:
            with chat_container:
                with st.chat_message("user", avatar=USER_AVATAR):
                    st.markdown(f"""
                        <div style="background-color: #FFFFE0; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                            <span style="font-size: 16px;">{prompt}</span>
                            <span style="font-size: 16px; font-weight: bold; margin-left: 10px;"> </span>
                            <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCAxMDAlIj48cGF0aCBmaWxsPSIjMDAwMDAwIiBkPSJNMjUuNjU2MjUgMTYuMjY0NjkgTDI0LjYyNjU2IDI3Ljk3MjE5TDI2LjkyNjU2IDMwLjY4MjE5TDI2Ljg2NjU2IDMwLjY4MjE5TDI1LjY1NjI1IDE2LjI2NDY5eiIvPjwvc3ZnPg==" alt="Chat Bubble Tail" width="20" height="20" style="margin-left: 10px; position: relative; top: -2px;">
                        </div>
                    """, unsafe_allow_html=True)

                with st.chat_message("ALEX", avatar=BOT_AVATAR):
                    with st.spinner("Thinking..."):
                        response = chat_engine.chat(prompt)
                        response.response = " " + response.response
                        st.markdown(f"""
                            <div style="background-color: #FFC0CB; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center;">
                                <span style="font-size: 16px; font-weight: bold; margin-right: 10px;"> ALEX </span>
                                <span style="font-size: 16px;">{response.response}</span>
                                <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCAxMDAlIj48cGF0aCBmaWxsPSIjMDAwMDAwIiBkPSJNMjUuNjU2MjUgMTYuMjY0NjkgTDI0LjYyNjU2IDI3Ljk3MjE5TDI2LjkyNjU2IDMwLjY4MjE5TDI2Ljg2NjU2IDMwLjY4MjE5TDI1LjY1NjI1IDE2LjI2NDY5eiIvPjwvc3ZnPg==" alt="Chat Bubble Tail" width="20" height="20" style="margin-left: 10px; position: relative; top: -2px;">
                            </div>
                        """, unsafe_allow_html=True)

                st.session_state.messages.append({"role": "ALEX", "content": response.response})

# Clear chat history button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.num_questions = 0
