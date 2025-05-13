# scripts/pipeline.py

import json
import logging
import os
import sys
import uuid
from pathlib import Path
from typing import List

import chromadb
import tiktoken
from bs4 import BeautifulSoup
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurations
CHUNK_SIZE = 50
CHUNK_OVERLAP = 10
CHUNKS_FILE = "outputs/chunked_docs.jsonl"
PERSIST_DIR = "persist/db/chroma"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "document_collection"


def get_files(source_path: Path) -> List[Path]:
    """List all HTML files in the source directory and its subdirectories."""
    files = []
    for file_path in source_path.rglob("*"):
        logger.info(f"Found file: {file_path}")
        if file_path.suffix.lower() == ".html":
            files.append(file_path)
        else:
            logger.warning(f"⚠️ Skipping unsupported file type: {file_path.name}")
    return files


def parse_html(file_path: str) -> List[Document]:
    """Parse HTML file into langchain Document objects."""
    documents = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            text = soup.get_text()
            documents.append(
                Document(page_content=text, metadata={"source": file_path})
            )
    except Exception as e:
        logger.warning(f"⚠️ Failed to parse HTML file {file_path}: {e}")
    return documents


def load_documents_from_path(source_path: Path) -> List[Document]:
    """Load documents from a specified directory."""
    files = get_files(source_path)
    logger.info(f"📂 Found {len(files)} HTML file(s).")
    documents = []
    for file in files:
        documents.extend(parse_html(str(file)))
    logger.info(f"✅ Parsed {len(documents)} document(s).")
    return documents


def chunker(documents, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Chunks documents into smaller pieces."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size, chunk_overlap=overlap, length_function=len
    )

    chunked_documents = []

    for doc_index, document in enumerate(documents):
        chunks = text_splitter.split_text(document.page_content)
        logger.debug(f"Doc {doc_index + 1}: {len(chunks)} chunks")

        for chunk in chunks:
            chunked_documents.append(
                {
                    "chunk_id": str(uuid.uuid4()),
                    "text": chunk.strip(),
                    "source": document.metadata.get("source", "unknown"),
                }
            )

    logger.info(f"✅ Total chunks generated: {len(chunked_documents)}")
    return chunked_documents


def compute_token_length(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)


def save_to_jsonl(chunked_documents, filename_or_path=CHUNKS_FILE):
    """Saves chunked documents to a .jsonl file."""
    os.makedirs("outputs", exist_ok=True)
    try:
        with open(filename_or_path, "w", encoding="utf-8") as f:
            for chunk in chunked_documents:
                f.write(json.dumps(chunk) + "\n")
        logger.info(f"✅ Saved {len(chunked_documents)} chunks to {filename_or_path}")
    except Exception as e:
        logger.error(f"❌ Error saving chunks: {e}")


def embed_and_store(
    documents,
    persist_dir=PERSIST_DIR,
    model_name=EMBED_MODEL_NAME,
    collection_name=COLLECTION_NAME,
):
    """Embed documents and store them in Chroma."""
    logger.info(f"📦 Using HuggingFace model: {model_name}")
    embedding_function = HuggingFaceEmbeddings(model_name=model_name)

    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(collection_name)

    for c in client.list_collections():
        if c.name != collection_name:
            logger.info(f"🗑️ Deleting unused collection: {c.name}")
            client.delete_collection(c.name)

    for document in documents:
        content = document.page_content.strip()
        if len(content) < 50:
            continue
        doc_id = str(uuid.uuid4())
        embedding = embedding_function.embed_documents([content])[0]
        collection.add(
            documents=[content],
            metadatas=[document.metadata],
            embeddings=[embedding],
            ids=[doc_id],
        )

    logger.info(
        f"✅ Embedded and stored {len(documents)} documents in '{collection_name}' collection."
    )


def run_pipeline(source_path: Path):
    """Run the entire document processing pipeline."""
    documents = load_documents_from_path(source_path)
    chunks = chunker(documents)

    for document in documents:
        token_count = compute_token_length(document.page_content)
    logger.info(f"Token count for document: {token_count}")

    save_to_jsonl(chunks)
    embed_and_store(documents)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <path_to_docs>")
        sys.exit(1)

    path_arg = Path(sys.argv[1])
    if not path_arg.exists() or not path_arg.is_dir():
        print(f"❌ Invalid directory: {path_arg}")
        sys.exit(1)

    run_pipeline(path_arg)
