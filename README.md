# Streamlit QnA Chatbot

This project implements a Question-and-Answer (QnA) chatbot using Streamlit and the LLAMA Index framework. The chatbot leverages the OpenAI GPT-4 model to provide answers to user questions based on information extracted from a given PDF book.

## Features

- **Streamlit Interface**: The chatbot is presented through a Streamlit interface, making it easy to interact with.
- **QnA Capabilities**: It can answer user questions based on the content of a provided PDF book.
- **Conversational Context**: The chatbot maintains a conversation history and can handle follow-up questions.
- **Personalization**: It greets users by name and incorporates their name into responses when appropriate.
- **Informative Messages**: If a user's question cannot be answered based on the provided context, the chatbot politely informs them and suggests rephrasing or providing additional context.


## Directory Structure:

├── audioRecognition.py
├── chroma_db
│   ├── cb326a45-9b84-4c2d-8865-61ecab212c14
│   │   ├── data_level0.bin
│   │   ├── header.bin
│   │   ├── length.bin
│   │   └── link_lists.bin
│   └── chroma.sqlite3
├── connector.py
├── data
│   ├── output.txt
│   ├── TIPS-G_Course_details.pdf
│   └── tips_resource.pdf
├── dataloader.py
├── folder_structure.txt
├── llamaindexchat.py
├── pics
│   ├── flowDiag.png
│   └── llamaindex_flow.png
├── README.md
├── requirements.txt
├── tree.py
└── WebAppFiles
    ├── htmlembed.html
    ├── srapper.py
    └── style.css


## Usage

1. **Clone Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: Install the required dependencies by running `pip install -r requirements.txt`.
3. **Setup Environment**: Set up environment variables, particularly the OpenAI API key.
4. **Run the Application**: Execute the Streamlit app by running `streamlit run app.py` in your terminal.
5. **Interact with the Chatbot**: Once the app is running, interact with the chatbot by asking questions in the provided input field.




## Requirements

- Python 3.x
- Streamlit
- LLAMA Index
- OpenAI API Key
- PDF Book (for content extraction) / (Data Resource)

## GPT4 + LLamaindex + ChromaDB

Leveraging GPT-4's advanced language understanding and generation capabilities, LlamaIndex's efficient data indexing and semantic representation, and ChromaDB's high-performance vector storage and retrieval, this trio empowers the creation of a powerful, intelligent, and highly responsive custom interactive chatbot.


## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
