# - scripts/load/parser_pdf.py

import logging

from langchain.schema import Document

# TODO: from pdfminer.high_level import extract_text

logger = logging.getLogger(__name__)


def parse_pdf(file_path: str):
    documents = []
    try:
        text = extract_text(file_path)
        if text:
            documents.append(
                Document(page_content=text, metadata={"source": str(file_path)})
            )
            logger.info(f"✅ Parsed PDF file: {file_path}")
        else:
            logger.warning(f"⚠️ Empty PDF or unreadable: {file_path}")
    except Exception as e:
        logger.error(f"❌ Failed to parse PDF {file_path}: {e}")
    return documents
