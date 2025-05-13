# - input/get_files.py

import logging
from pathlib import Path
from typing import List

from langchain.schema import Document

from input.parser import parse_files
from input.registry import PARSER_REGISTRY
from input.utils.filtering import filter_documents  # 👈 New import

logger = logging.getLogger(__name__)


def get_files(source_path: Path) -> List[Path]:
    """List all supported files in the source directory and its subdirectories."""
    files = []
    for file_path in source_path.rglob("*"):
        if file_path.suffix.lower() in PARSER_REGISTRY:
            files.append(file_path)
        elif file_path.is_dir():
            logger.warning(f"⚠️ Skipping directory: {file_path.name}")
        else:
            logger.warning(f"⚠️ Skipping unsupported file type: {file_path.name}")
    return files


def load_documents_from_cli(source_path: Path) -> List[Document]:
    """CLI interface to load and clean documents from the provided directory path."""
    files = get_files(source_path)
    logger.info(f"📂 Found {len(files)} supported file(s).")

    documents = parse_files(files)
    logger.info(f"✅ Parsed {len(documents)} document(s).")

    # 🧹 Filter trivial/invalid documents
    documents = filter_documents(documents, min_length=50)
    logger.info(f"✅ Retained {len(documents)} document(s) after filtering.")

    return documents
