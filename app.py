import streamlit as st
from dotenv import load_dotenv




def main():
    load_dotenv()
    st.set_page_config(page_title="Multi PDF RAG", page_icon=":books:")
    st.header("Multi PDF RAG :books:")
    st.text_input("Ask anything: ")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs and click process", accept_multiple_files=True)
        
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                


if __name__ == '__main__':
    main()