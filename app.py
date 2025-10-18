import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
from utils.extract_raw_text import extract_raw_text
from utils.get_text_chunks import get_text_chunks
from utils.get_vectorstore import get_vectorstore
from utils.get_conversation_chain import get_conversation_chain
from huggingface_hub import login
from htmlTemplates import css, bot_template, user_template

HF_TOKEN = (
    os.getenv("HUGGINGFACEHUB_API_TOKEN")
    or os.getenv("HUGGINGFACE_HUB_TOKEN")
    or os.getenv("HF_TOKEN")
)

if HF_TOKEN:
    os.environ["HF_TOKEN"] = HF_TOKEN
    os.environ["HUGGINGFACE_HUB_TOKEN"] = HF_TOKEN
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN
    try:
        login(HF_TOKEN)
    except Exception:
        pass


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    st.set_page_config(page_title="Multi PDF RAG", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    st.header("Multi PDF RAG :books:")
    user_question = st.text_input("Ask anything: ")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs and click process", accept_multiple_files=True)
        
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = extract_raw_text(pdf_docs)
                chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(chunks, hf_token=HF_TOKEN)
                st.session_state.conversation = get_conversation_chain(vectorstore)
                


if __name__ == '__main__':
    main()