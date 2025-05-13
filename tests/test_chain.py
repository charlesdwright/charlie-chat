# - tests/test_chain.py

import logging
import argparse
from nlp.retrieve.retrieval_chain import create_retrieval_qa_chain
from tests.test_utils import compare_retrieved_with_original  # Import the helper function

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Test the retrieval QA chain.")
    parser.add_argument("--query", type=str, help="Question to ask the QA chain")
    args = parser.parse_args()

    # If no query was passed, prompt the user
    query = args.query
    if not query:
        query = input("🔍 Enter your query: ").strip()
        while not query:
            print("⚠️  Please enter a non-empty query.")
            query = input("🔍 Enter your query: ").strip()

    # Create the RetrievalQA chain
    chain = create_retrieval_qa_chain()
    logger.info(f"📝 Query: {query} (type: {type(query)})")

    try:
        # Execute the query through the chain
        response = chain(query)
        logger.debug(f"Response type: {type(response)}")
        logger.info("\n✅ Answer:")
        logger.info(response["result"])

        # Log the source documents
        logger.info("\n📚 Sources:")
        for doc in response.get("source_documents", []):
            logger.info(f"- {doc.metadata.get('source', 'unknown')}")

        # Compare retrieved documents with original chunks
        all_matched = compare_retrieved_with_original(response.get("source_documents", []))
        if all_matched:
            logger.info("✅ All retrieved documents matched the original data.")
        else:
            logger.warning("⚠️ Some retrieved documents did not match the original data.")

    except Exception as e:
        logger.error(f"❌ Error during chain execution: {e}", exc_info=True)

if __name__ == "__main__":
    main()
