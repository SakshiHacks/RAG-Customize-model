from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

from backend.rag.pdf_loader import load_pdfs
from backend.rag.vector_store import create_vectorstore


def get_rag_chain():
    documents = load_pdfs()
    vectorstore = create_vectorstore(documents)

    llm_pipeline = pipeline(
        "text-generation",
        model="gpt2",
        max_new_tokens=200
    )

    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )

    return qa_chain
