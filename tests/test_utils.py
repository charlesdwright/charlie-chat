# - tests/test_utils.py

from nlp.embed.utils import load_chunks
import logging

logger = logging.getLogger(__name__)

def compare_retrieved_with_original(response_source_docs):
    """
    Compare retrieved documents against the original chunked data from the .jsonl file.
    
    Args:
        response_source_docs (list): List of retrieved documents from the response.
        
    Returns:
        bool: True if all retrieved documents are found in the original chunks, False otherwise.
    """
    # Load original chunks
    original_chunks = load_chunks()
    original_texts = {chunk.page_content.strip(): chunk.metadata for chunk in original_chunks}

    all_matched = True
    for doc in response_source_docs:
        content = doc.page_content.strip()
        if content in original_texts:
            logger.info(f"✅ Retrieved document matched original chunk (source: {doc.metadata.get('source', 'unknown')})")
        else:
            logger.warning(f"⚠️ Retrieved document NOT found in original chunks (source: {doc.metadata.get('source', 'unknown')})")
            all_matched = False
    return all_matched
