# - splitters/tokenizer.py

import logging
import tiktoken
from langchain.schema import Document

# Set up logging
logger = logging.getLogger(__name__)

def count_tokens(doc: Document, model: str = "gpt-3.5-turbo") -> int:
    """
    Counts the number of tokens in the input document using tiktoken.

    Args:
        doc (Document): The input document object from LangChain.
        model (str): The model name (default is "gpt-3.5-turbo").

    Returns:
        int: The number of tokens in the document content.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        tokens = encoding.encode(doc.page_content)
        token_count = len(tokens)
        logger.info(
            f"Token count for document '{doc.metadata.get('source', 'unknown')}': {token_count}"
        )
        return token_count
    except Exception as e:
        logger.error(
            f"Error tokenizing document '{doc.metadata.get('source', 'unknown')}': {e}"
        )
        raise


def tokenize_documents(documents: list, model: str = "gpt-3.5-turbo") -> list:
    """
    Tokenizes a list of documents and returns a list of token counts.

    Args:
        documents (list): List of Document objects.
        model (str): The model name (default is "gpt-3.5-turbo").

    Returns:
        list: A list of token counts for each document.
    """
    token_counts = []
    for i, doc in enumerate(documents, 1):
        try:
            token_count = count_tokens(doc, model)
            token_counts.append((i, token_count))
        except Exception:
            logger.warning(f"Token count failed for document {i}")
            token_counts.append((i, None))  # Append None in case of failure
    return token_counts


def count_and_log_token_info(documents: list, model: str = "gpt-3.5-turbo"):
    """
    Count tokens for each document and log the results.

    Args:
        documents (list): List of Document objects.
        model (str): The model name (default is "gpt-3.5-turbo").
    """
    token_counts = tokenize_documents(documents, model)
    for doc_id, token_count in token_counts:
        if token_count is not None:
            logger.info(f"Document {doc_id} token count: {token_count}")
        else:
            logger.warning(f"Document {doc_id} token count failed.")
