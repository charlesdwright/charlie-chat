# input/utils/filtering.py

import logging
from langchain.schema import Document

logger = logging.getLogger(__name__)

def filter_documents(documents, min_length=50, stopwords=None):
    """Filter out documents that are too short or contain only trivial content."""
    if stopwords is None:
        stopwords = {"api", "experimental"}

    filtered = []
    for doc in documents:
        content = doc.page_content.strip()

        if len(content) < min_length:
            logger.debug(f"🛑 Skipping short doc: {content[:30]!r}")
            continue

        if content.lower() in stopwords:
            logger.debug(f"🚫 Skipping trivial content: {content[:30]!r}")
            continue

        filtered.append(doc)

    logger.info(f"✅ Filtered: kept {len(filtered)} / {len(documents)} documents")
    return filtered
