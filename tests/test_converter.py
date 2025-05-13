# - tests/test_converter.py

from nlp.utils.converter import dicts_to_documents
from langchain.schema import Document

def test_dicts_to_documents():
    # Sample input data
    test_data = [
        {"page_content": "This is the first document.", "metadata": {"source": "file1.txt"}},
        {"page_content": "Here is another document.", "metadata": {"source": "file2.txt", "author": "Alice"}},
        {"page_content": "The third document has no metadata."}
    ]

    # Call the function
    output_documents = dicts_to_documents(test_data)

    # Check and print the results
    print("Testing dicts_to_documents function:")

    # Check if the output is a list of Document objects
    if isinstance(output_documents, list):
        print("Output is a list.")
    else:
        print("Output is NOT a list.")

    # Check if all elements are instances of Document
    all_documents = all(isinstance(doc, Document) for doc in output_documents)
    if all_documents:
        print("All elements are Document objects.")
    else:
        print("Not all elements are Document objects.")

    # Print content and metadata of each document
    for idx, doc in enumerate(output_documents):
        print(f"Document {idx + 1}:")
        print(f"  - Page Content: {doc.page_content}")
        print(f"  - Metadata: {doc.metadata}")

def main():
    test_dicts_to_documents()

if __name__ == "__main__":
    main()
