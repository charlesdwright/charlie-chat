# scripts/load/source/parser.py

import logging
from pathlib import Path
from typing import List
from langchain.schema import Document
from input.registry import PARSER_REGISTRY

logger = logging.getLogger(__name__)


def parse_files(files: List[Path]) -> List[Document]:
    """Parse files using the registered parser functions."""
    documents = []
    for file_path in files:
        parser = PARSER_REGISTRY.get(file_path.suffix.lower())
        if parser:
            documents.extend(parser(str(file_path)))
        else:
            logger.warning(f"⚠️ No parser registered for {file_path.suffix} file.")
    return documents
