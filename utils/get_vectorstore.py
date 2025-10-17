from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
import os

def get_vectorstore(chunks, hf_token=None):
    hf_token = hf_token or os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN") or os.getenv("HF_TOKEN")
    model_kwargs = {}
    if hf_token: 
        model_kwargs["token"] = hf_token
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl", model_kwargs=model_kwargs, encode_kwargs={"normalize_embeddings": True})
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore