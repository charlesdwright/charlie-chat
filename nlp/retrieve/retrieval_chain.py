# nlp/retrieve/retrieval_chain.py

import logging

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from nlp.llms.cloudflare import CloudflareLLM
from nlp.retrieve.retriever_setup import get_retriever

logger = logging.getLogger(__name__)


def create_retrieval_qa_chain():
    retriever = get_retriever()
    llm = CloudflareLLM()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
    )
    logger.info("✅ ConversationalRetrievalChain created successfully.")
    return qa_chain
