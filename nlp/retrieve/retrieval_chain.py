# nlp/retrieve/retrieval_chain.py

import logging
from langchain.chains import RetrievalQA
from nlp.llms.cloudflare import CloudflareLLM
from nlp.retrieve.retriever_setup import get_retriever

logger = logging.getLogger(__name__)

def create_retrieval_qa_chain():
    """Create the RetrievalQA chain using Cloudflare's LLM and retriever."""
    logger.info("📂 Initializing retriever...")
    retriever = get_retriever()
    logger.info("✅ Retriever initialized.")

    logger.info("🧠 Initializing Cloudflare LLM...")
    llm = CloudflareLLM()
    logger.info("✅ Cloudflare LLM initialized.")

    logger.info("🔗 Creating RetrievalQA chain...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    logger.info("✅ RetrievalQA chain created successfully.")
    return qa_chain
