# - script/load/utils/save_to_jsonl.py

import json
import os


def save_to_jsonl(chunked_documents, filename_or_path="test_chunks.jsonl"):
    """
    Saves chunked documents to a .jsonl file.

    Args:
        chunked_documents (list): List of chunk dicts.
        filename_or_path (str): File name or full path to write to.
                                If only a filename is given, it saves to the 'outputs/' directory.
    """
    # If only a filename is passed, prepend 'outputs/' directory
    if not os.path.isabs(filename_or_path) and not filename_or_path.startswith(
        "outputs/"
    ):
        os.makedirs("outputs", exist_ok=True)
        file_path = os.path.join("outputs", filename_or_path)
    else:
        file_path = filename_or_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write the chunks to the file
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for chunk in chunked_documents:
                f.write(json.dumps(chunk) + "\n")
        print(f"✅ Saved {len(chunked_documents)} chunks to {file_path}")
    except Exception as e:
        print(f"Error saving chunks to {file_path}: {e}")


# utils/load_from_jsonl.py
def load_from_jsonl(filepath):
    with open(filepath, "r") as f:
        return [json.loads(line) for line in f]
