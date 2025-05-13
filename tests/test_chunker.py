# - test/test_chunker.py

import logging
from nlp.chunk.chunker import chunker
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_chunker():
    """Test the chunker function to ensure documents are properly chunked."""

    # Create sample documents
    documents = [
        Document(page_content="LangChain is a powerful framework for building AI-driven applications. It provides seamless integration with various LLMs and NLP tools.", metadata={"source": "doc1"}),
        Document(page_content="Chunking is essential for processing large documents. This functionality ensures that texts are split into manageable pieces.", metadata={"source": "doc2"})
    ]

    # Call the chunker function to split documents into chunks
    logger.info("⏳ Testing chunker function...")
    chunked_documents = chunker(documents)

    # Check if the chunking process returns a list of dictionaries with the expected keys
    assert isinstance(chunked_documents, list), "Expected chunked_documents to be a list."
    assert all(isinstance(doc, dict) for doc in chunked_documents), "Each chunk should be a dictionary."
    assert all('chunk_id' in doc and 'text' in doc and 'source' in doc for doc in chunked_documents), "Each chunk should have 'chunk_id', 'text', and 'source' keys."

    # Log the results
    logger.info(f"✅ Chunking successful. Total chunks: {len(chunked_documents)}")

    # Optionally log the first chunk for verification
    logger.info(f"First chunk details: {chunked_documents[0]}")

if __name__ == "__main__":
    test_chunker()
