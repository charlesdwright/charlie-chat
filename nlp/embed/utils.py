# - nlp/embed/utils.py

import logging
import uuid

import chromadb

from config.defaults import CONFIG
from nlp.embed.model import CloudflareEmbeddings

# Setup logging
logger = logging.getLogger(__name__)

# Configs
provider = CONFIG["DEFAULT_PROVIDER"]
CHUNK_FILE = CONFIG["GENERAL"]["CHUNK_FILE"]
PERSIST_DIR = CONFIG["CHROMA"]["PERSIST_DIR"]
COLLECTION_NAME = CONFIG["CHROMA"]["COLLECTION_NAME"]
EMBED_MODEL_NAME = CONFIG[provider]["EMBED_MODEL"]


def embed_and_store(
    documents,
    persist_dir=PERSIST_DIR,
    model_name=EMBED_MODEL_NAME,
    collection_name=COLLECTION_NAME,
    purge=False,
):
    """Embed documents and store them in Chroma using Cloudflare Embeddings."""
    logger.info(f"📦 Using Cloudflare model: {model_name}")
    embedding_function = CloudflareEmbeddings(model_name=model_name)

    client = chromadb.PersistentClient(path=persist_dir)

    # 💣 Optional: Purge collection if requested
    if purge:
        try:
            logger.warning(f"🧨 Purging vectorstore collection: '{collection_name}'...")
            client.delete_collection(collection_name)
        except Exception as e:
            logger.warning(f"⚠️ Failed to delete collection '{collection_name}': {e}")

    # (Re)create the target collection
    logger.warning(f"🧨 (Re)creating vectorstore collection: '{collection_name}'...")
    collection = client.get_or_create_collection(collection_name)

    # Optional cleanup of other collections
    for c in client.list_collections():
        if c.name != collection_name:
            logger.info(f"🗑️ Deleting unused collection: {c.name}")
            client.delete_collection(c.name)

    successful_additions = 0
    for document in documents:
        content = document.page_content.strip()
        if not content:
            logger.warning(
                f"❌ Document {document.metadata.get('chunk_id')} has empty content."
            )
            continue

        doc_id = str(document.metadata.get("chunk_id") or uuid.uuid4())

        try:
            embedding = embedding_function.embed_documents([content])[0]
            if not embedding:
                logger.warning(f"❌ Empty embedding for {doc_id}")
                continue
            logger.debug(f"Embedding for {doc_id}: {embedding[:5]}...")
        except Exception as e:
            logger.warning(f"❌ Failed to embed {doc_id}: {e}")
            continue

        logger.warning(
            f"🧨 Adding embed to vectorstore collection: '{collection_name}'..."
        )
        collection.add(
            documents=[content],
            metadatas=[document.metadata],
            embeddings=[embedding],
            ids=[doc_id],
        )
        successful_additions += 1

    logger.info(
        f"✅ Embedded and stored {successful_additions} documents in {persist_dir}"
    )
    logger.info(
        f"Collection '{collection_name}' now contains {collection.count()} documents."
    )
