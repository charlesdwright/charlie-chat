# inspect_vectorstore.py

import logging

from langchain.vectorstores import Chroma

from config.defaults import CONFIG
from nlp.embed.model import CloudflareEmbeddings  # Import Cloudflare Embeddings

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def inspect_chroma_store():
    # Initialize Cloudflare Embeddings
    embeddings = CloudflareEmbeddings(model_name=CONFIG["CLOUDFLARE"]["EMBED_MODEL"])

    # Load the Chroma vector store
    try:
        db = Chroma(
            collection_name=CONFIG["CHROMA"]["COLLECTION_NAME"],
            persist_directory=CONFIG["CHROMA"]["PERSIST_DIR"],
            embedding_function=embeddings,
        )
        logger.info("✅ Chroma vector store loaded successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to load Chroma vector store: {e}")
        return

    # Fetch the number of stored documents
    try:
        count = db._collection.count()
        logger.info(f"🔍 Total documents in vector store: {count}\n")

        # Optionally show a few sample documents
        if count > 0:
            docs = db._collection.get(include=["documents"])  # includes full text
            logger.info("Displaying the first 5 documents:")
            for i, doc in enumerate(docs["documents"][:5]):
                logger.info(f"--- Document {i + 1} ---\n{doc}\n")
        else:
            logger.warning("No documents found in the vector store.")

    except Exception as e:
        logger.error(f"❌ Error while fetching documents: {e}")


if __name__ == "__main__":
    inspect_chroma_store()
