# - scripts/load/chunker.py

import logging
from uuid import uuid4

from langchain.text_splitter import RecursiveCharacterTextSplitter

from config.defaults import (
    CONFIG,  # Assuming the provided CONFIG dictionary is in defaults.py
)

# Configure logging
logger = logging.getLogger(__name__)

# Fetch chunk size and overlap from the configuration
CHUNK_SIZE = CONFIG["GENERAL"]["CHUNK_SIZE"]
CHUNK_OVERLAP = CONFIG["GENERAL"]["CHUNK_OVERLAP"]


def chunker(documents, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size, chunk_overlap=overlap, length_function=len
    )

    chunked_documents = []

    for doc_index, document in enumerate(documents):
        chunks = text_splitter.split_text(document.page_content)
        for i, chunk in enumerate(chunks, start=1):
            chunk = chunk.strip()
            if not chunk:
                logger.debug(f"⚠️ Skipped empty chunk from doc {doc_index + 1}")
                continue

            chunk_id = str(uuid4())

            chunked_documents.append(
                {
                    "page_content": chunk,
                    "metadata": {
                        "chunk_id": chunk_id,
                        "source": document.metadata.get("source", "unknown"),
                    },
                }
            )

    logger.info(f"✅ Total chunks generated: {len(chunked_documents)}")

    return chunked_documents
