# scripts/ingest.py

import logging
import os
from pathlib import Path

from config.defaults import CONFIG
from input.get_files import load_documents_from_cli
from nlp.chunk.chunker import chunker
from nlp.embed.utils import embed_and_store
from nlp.utils.converter import dicts_to_documents
from nlp.utils.io_jsonl import load_from_jsonl, save_to_jsonl

# no spies
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

# Config
CHUNK_FILE = CONFIG["GENERAL"]["CHUNK_FILE"]
CHUNK_SIZE = CONFIG["GENERAL"]["CHUNK_SIZE"]
CHUNK_OVERLAP = CONFIG["GENERAL"]["CHUNK_OVERLAP"]


def chunk_documents(documents):
    if not documents:
        logger.warning("⚠️ No documents provided for chunking.")
        return []
    logger.info("✂️ Chunking documents...")
    chunks = chunker(documents, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    logger.info(f"✅ Chunked into {len(chunks)} chunk(s).")
    return chunks


def save_chunks_to_file(chunks):
    if not chunks:
        logger.warning("⚠️ No chunks to save.")
        return
    try:
        logger.info("💾 Saving chunks to file...")
        save_to_jsonl(chunks, CHUNK_FILE)
        logger.info(f"✅ Saved chunks to {CHUNK_FILE}.")
    except Exception as e:
        logger.error(f"Failed to save chunks: {e}")


def convert_chunks_to_documents(chunks):
    if not chunks:
        logger.warning("⚠️ No chunks to convert.")
        return []
    logger.debug(f"🧠 Sample chunk before conversion: {chunks[0]}")
    documents = dicts_to_documents(chunks)
    logger.info(f"✅ Converted {len(documents)} chunk(s) to Document objects.")
    return documents


def run_pipeline(
    source_path: Path, from_disk: bool = False, purge_vectorstore: bool = False
):
    logger.info("🚀 Starting the ingestion pipeline...")

    # Step 1: Load chunks
    if from_disk:
        logger.info(f"📥 Loading chunks from {CHUNK_FILE}...")
        chunks = load_from_jsonl(CHUNK_FILE)
    else:
        documents = load_documents_from_cli(source_path)
        chunks = chunk_documents(documents)
        save_chunks_to_file(chunks)

    # Step 2: Convert and embed
    documents = convert_chunks_to_documents(chunks)
    embed_and_store(documents, purge=purge_vectorstore)

    logger.info("✅ Ingestion pipeline completed.")


if __name__ == "__main__":
    import argparse

    # Argument parsing
    parser = argparse.ArgumentParser(description="Ingest and process documents.")
    parser.add_argument("source_path", type=str, help="Path to source documents.")
    parser.add_argument(
        "--from-disk",
        action="store_true",
        help="Load chunks from existing .jsonl file.",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument(
        "--purge", action="store_true", help="Flush VectorDB - for new docs."
    )
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Run the pipeline with --purge logic added
    run_pipeline(
        Path(args.source_path), from_disk=args.from_disk, purge_vectorstore=args.purge
    )
