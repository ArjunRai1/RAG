from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFaceHub
import os
def get_conversation_chain(vectorstore):
    hf_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    try:
        import streamlit as st
        hf_token = st.secrets.get("HUGGINGFACEHUB_API_TOKEN", hf_token)
    except Exception:
        pass

    if not hf_token:
        raise RuntimeError(
            "HUGGINGFACEHUB_API_TOKEN is missing. Set it in environment "
            "or Streamlit secrets."
        )
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-xxl",  
        task="text2text-generation",
        huggingfacehub_api_token=hf_token,
        model_kwargs={"temperature":0.5, "max_length":512}
    ) 
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever=vectorstore.as_retriever(),
        memory = memory
    )
    return conversation_chain
