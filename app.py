import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama
from htmlTemplates import css,bot_template, user_template
import re

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts= text_chunks, embedding= embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = Ollama(model="deepseek-r1:1.5b")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_user_input(user_question):
    if st.session_state.conversation is None:
        st.error("Please upload and process a PDF first before asking questions.")
        return
    response = st.session_state.conversation({"question": user_question})
    
    # Extract the answer and clean it up
    answer = response.get("answer", "")
    # Remove <think> tags and their content
    answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL)
    # Clean up extra whitespace and newlines
    answer = re.sub(r'\n\s*\n', '\n\n', answer).strip()
    
    # Display user question in user template
    st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
    
    # Display bot answer in bot template
    st.write(bot_template.replace("{{MSG}}", answer), unsafe_allow_html=True)
    
    st.session_state.chat_history = response["chat_history"]

def main():
    load_dotenv() 
    st.set_page_config(page_title="Chat with PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
        
    st.header("Chat with PDFs")
    user_question = st.text_input("Ask a question about the documents")
    if user_question:
        handle_user_input(user_question)
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", type="pdf", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                # create vector store
                vectorstore = get_vectorstore(text_chunks)  
                
                # conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)  

if __name__ == "__main__":
    main()