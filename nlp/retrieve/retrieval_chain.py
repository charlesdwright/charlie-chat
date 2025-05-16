# - nlp/retrieve/retrieval_chain.py

import logging

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryBufferMemory,
)

from config.defaults import CONFIG
from nlp.llms.cloudflare import CloudflareLLM
from nlp.retrieve.retriever_setup import get_retriever

logger = logging.getLogger(__name__)


def get_memory():
    mem_cfg = CONFIG.get("MEMORY", {})
    mem_type = mem_cfg.get("type", "buffer")

    if mem_type == "window":
        return ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=mem_cfg.get("window_size", 3),
            return_messages=True,
            output_key="answer",
        )
    elif mem_type == "summary_buffer":
        return ConversationSummaryBufferMemory(
            llm=CloudflareLLM(),
            max_token_limit=mem_cfg.get("max_token_limit", 8000),
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )
    else:  # fallback to 'buffer'
        return ConversationBufferMemory(
            memory_key="chat_history", return_messages=True, output_key="answer"
        )


def create_retrieval_qa_chain():
    retriever = get_retriever()
    llm = CloudflareLLM()
    memory = get_memory()

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=CONFIG.get("CHAIN", {}).get(
            "return_source_documents", False
        ),
    )

    logger.info("✅ ConversationalRetrievalChain created successfully.")
    return qa_chain
