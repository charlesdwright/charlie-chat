# - scripts/load/parse_html.py

import logging
import re

import chardet
from bs4 import BeautifulSoup
from langchain.schema import Document

logger = logging.getLogger(__name__)


def remove_non_ascii(text: str) -> str:
    """Remove characters outside basic printable ASCII range."""
    return re.sub(r"[^\x20-\x7E\n]+", "", text)


def parse_html(file_path: str):
    documents = []
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)["encoding"]
            text = raw_data.decode(encoding or "utf-8", errors="replace")

            # Parse HTML and extract visible text
            soup = BeautifulSoup(text, "html.parser")
            cleaned_text = soup.get_text(separator="\n", strip=True)

            # Remove non-ASCII characters and extra whitespace
            cleaned_text = remove_non_ascii(cleaned_text)
            cleaned_text = re.sub(
                r"\n\s*\n+", "\n\n", cleaned_text
            )  # collapse blank lines
            cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)  # normalize spaces
            cleaned_text = cleaned_text.strip()
            # cleaned_text = cleaned_text.replace("\n", " ")

            # Only add the document if there's actual content
            if cleaned_text:
                documents.append(
                    Document(page_content=cleaned_text, metadata={"source": file_path})
                )
                logger.info(f"✅ Parsed HTML file: {file_path}")
            else:
                logger.warning(
                    f"⚠️ Skipped HTML file with no extractable text: {file_path}"
                )

    except Exception as e:
        logger.error(f"❌ Failed to parse HTML {file_path}: {e}")

    return documents
