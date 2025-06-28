# PDF Chat Application

A Streamlit-based application that allows you to chat with your PDF documents using AI. The application uses local language models and embeddings to provide intelligent responses based on the content of your uploaded PDFs.

## Features

- 📄 **PDF Upload**: Upload multiple PDF documents
- 🤖 **AI Chat**: Ask questions about your PDF content
- 🧠 **Local AI**: Uses Ollama with local language models (no API costs)
- 🔍 **Semantic Search**: Advanced document retrieval using sentence transformers
- 💬 **Chat Interface**: Beautiful chat UI with user and bot avatars
- 📝 **Memory**: Remembers conversation context

## Prerequisites

Before running this application, make sure you have:

1. **Python 3.8+** installed
2. **Ollama** installed and running locally
3. **Required Python packages** (see installation section)

### Installing Ollama

1. Download Ollama from [https://ollama.com/download](https://ollama.com/download)
2. Install and start Ollama
3. Pull the required model:
   ```bash
   ollama pull deepseek-r1:1.5b
   ```

## Installation

1. **Clone or download** this project to your local machine

2. **Navigate to the project directory**:

   ```bash
   cd PDF_Chat
   ```

3. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **API Keys**:
   Obtain your hugging face api key and add it to the `.env` file in the project directory

   ```bash
   HUGGINGFACEHUB_API_KEY=your_api_key
   ```

6. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application**:

   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and go to the URL shown in the terminal (usually `http://localhost:8501`)

3. **Upload PDF documents**:

   - Use the sidebar to upload one or more PDF files
   - Click the "Process" button to index the documents

4. **Start chatting**:
   - Type your questions in the text input
   - The AI will answer based on the content of your uploaded PDFs

## How It Works

1. **Document Processing**: PDFs are converted to text and split into chunks
2. **Embedding Generation**: Text chunks are converted to vector embeddings using sentence transformers
3. **Vector Storage**: Embeddings are stored in a FAISS vector database for fast retrieval
4. **Question Answering**: When you ask a question:
   - The question is converted to an embedding
   - Similar document chunks are retrieved
   - The local language model generates an answer based on the retrieved context

## Technical Stack

- **Frontend**: Streamlit
- **PDF Processing**: PyPDF2
- **Text Splitting**: LangChain CharacterTextSplitter
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: FAISS
- **Language Model**: Ollama with deepseek-r1:1.5b
- **Conversation Management**: LangChain ConversationalRetrievalChain

## File Structure

```
Chat_with_pdfs/
├── .env
├── app.py              # Main Streamlit application
├── htmlTemplates.py    # CSS styles and HTML templates
├── README.md          # This file
└── venv/              # Virtual environment (created during setup)
```

## Customization

### Changing the Language Model

To use a different Ollama model, modify the `get_conversation_chain` function in `app.py`:

```python
def get_conversation_chain(vectorstore):
    llm = Ollama(model="your-preferred-model")  # Change this line
    # ... rest of the function
```

### Modifying the Chat Interface

Edit `htmlTemplates.py` to customize:

- Chat message styling
- Avatar images
- Colors and layout

## Troubleshooting

### Common Issues

1. **"Ollama model not found" error**:

   - Make sure Ollama is running
   - Pull the required model: `ollama pull deepseek-r1:1.5b`

2. **Import errors**:

   - Ensure all packages are installed in your virtual environment
   - Check that you're using the correct Python version

3. **PDF processing issues**:
   - Ensure PDFs are not password-protected
   - Check that PDFs contain extractable text

### Performance Tips

- For large PDFs, processing may take some time
- The first question after processing might be slower as the model loads
- Consider using smaller chunk sizes for faster processing

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Ollama](https://ollama.ai/)
- Uses [LangChain](https://langchain.com/) for AI workflows
- Embeddings provided by [Sentence Transformers](https://www.sbert.net/)
