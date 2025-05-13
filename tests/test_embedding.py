# - tests/test_embedding.py

import logging

from nlp.embed.model import CloudflareEmbeddings

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_embedding():
    """Test embedding to ensure the Cloudflare embedding functionality is working."""

    # Initialize the embedding instance
    embedding = CloudflareEmbeddings()

    # Define a list of test documents
    documents = [
        "LangChain is a framework for building AI applications.",
        "Embedding transforms text into vector representations.",
        "This is a test document to check the embedding functionality.",
    ]

    # Test embedding of documents
    try:
        logger.info("📄 Embedding documents...")
        embedded_documents = embedding.embed_documents(documents)
        logger.info(f"✅ Successfully embedded {len(embedded_documents)} documents.")

        # Ensure the embedding is a list of floats
        if all(
            isinstance(embedding, list)
            and all(isinstance(val, float) for val in embedding)
            for embedding in embedded_documents
        ):
            logger.info("✅ Document embeddings are in the correct format.")
        else:
            logger.error("❌ Document embeddings are not in the correct format.")

    except Exception as e:
        logger.error(f"❌ Error embedding documents: {e}", exc_info=True)

    # Test embedding of a single query
    query = "What is LangChain?"
    try:
        logger.info(f"🔍 Embedding query: {query}")
        embedded_query = embedding.embed_query(query)
        logger.info(
            f"✅ Query embedded successfully: {embedded_query[:5]}..."
        )  # Show first 5 values of embedding

        # Validate the format of the embedding
        if isinstance(embedded_query, list) and all(
            isinstance(val, float) for val in embedded_query
        ):
            logger.info("✅ Query embedding is in the correct format.")
        else:
            logger.error("❌ Query embedding is not in the correct format.")

    except Exception as e:
        logger.error(f"❌ Error embedding query: {e}", exc_info=True)


if __name__ == "__main__":
    test_embedding()
