# tests/retriever_setup.py

import logging
import sys

from nlp.retrieve.retriever_setup import get_retriever


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


def main():
    logger = configure_logging()

    try:
        logger.info("📂 Loading retriever...")
        retriever = get_retriever()
        logger.info("✅ Retriever is ready.")

        # Get the query from command-line arguments or use default
        query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What about the pope?"
        logger.info(f"📨 Query: {query}")

        results = retriever.get_relevant_documents(query)

        if not results:
            logger.warning("⚠️ No documents were retrieved.")
            return

        print(f'\n🔍 Results for query: "{query}"\n')
        for i, doc in enumerate(results, 1):
            content = getattr(doc, "page_content", None)
            if content:
                print(f"--- Result {i} ---")
                print(content)
                print()
            else:
                print(f"--- Result {i} ---")
                print("[No content found in document]")
                print()

    except Exception as e:
        logger.exception(f"❌ Failed to query retriever: {e}")


if __name__ == "__main__":
    main()
