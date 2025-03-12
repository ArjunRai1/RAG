import streamlit as st



def main():
    st.set_page_config("RAG")
    st.header("PDF Query")

    with st.sidebar:
        st.title("Input")
        pdf_docs = st.file_uploader("Upload PDF files and click submit", accept_multiple_files=True)
        if st.button("Submit"):
            with st.spinner("Processing"):
                st.success("Done")


if __name__ == "__main__":
    main()