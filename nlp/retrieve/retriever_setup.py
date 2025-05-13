# - nlp/retrieve/retriever_setup.py

import logging
from langchain.vectorstores import Chroma
from config.defaults import CONFIG
from nlp.embed.model import CloudflareEmbeddings

# Configs
provider = CONFIG["DEFAULT_PROVIDER"]
vectordb = CONFIG["DEFAULT_VECTORDB"]

PERSIST_DIR = CONFIG[vectordb]["PERSIST_DIR"]
COLLECTION_NAME = CONFIG[vectordb]["COLLECTION_NAME"]

def get_retriever():
    logging.info("📂 Loading vector store and initializing retriever...")

    embedding_function = CloudflareEmbeddings()  # Only one provider in beta

    vectordb = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR,
        embedding_function=embedding_function,
    )

    logging.info("✅ Retriever is ready.")
    return vectordb.as_retriever()
