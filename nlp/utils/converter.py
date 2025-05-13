# utils/converters.py

from typing import Dict, List

from langchain.schema import Document


def dicts_to_documents(data: List[Dict]) -> List[Document]:
    """
    Converts a list of dictionaries with 'page_content' and 'metadata' keys
    into LangChain Document objects.
    """
    print(f"[dicts_to_documents] Converting {len(data)} items")

    for i, item in enumerate(data[:3]):
        print(f"[Input {i + 1}] Content length: {len(item.get('page_content', ''))}")
        print(f"[Input {i + 1}] Preview: {item.get('page_content', '')[:100]}")
        print(f"[Input {i + 1}] Metadata: {item.get('metadata', {})}")

    documents = []
    for item in data:
        content = item.get("page_content", "")
        metadata = item.get("metadata", {})
        documents.append(Document(page_content=content, metadata=metadata))

    return documents
