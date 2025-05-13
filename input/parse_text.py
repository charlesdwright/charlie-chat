# - scripts/load/parser_text.py

import logging

import chardet
from langchain.schema import Document

logger = logging.getLogger(__name__)


def parse_text(file_path: str):
    documents = []
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)["encoding"]
            text = raw_data.decode(encoding or "utf-8", errors="replace")
            documents.append(
                Document(page_content=text, metadata={"source": file_path})
            )
            logger.info(f"✅ Parsed text file: {file_path}")
    except Exception as e:
        logger.error(f"❌ Failed to parse text file {file_path}: {e}")
    return documents
