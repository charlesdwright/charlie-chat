import json

# Load the chunked_docs.jsonl file
with open('outputs/chunked_docs.jsonl', 'r') as file:
    lines = file.readlines()

# Check for empty chunks and print them
empty_chunks = []
for line in lines:
    chunk = json.loads(line)

    # Get the original and stripped text
    original_text = chunk['text']
    stripped_text = original_text.strip()

    # Print the chunk_id and both text lengths
    print(f"Checking chunk_id: {chunk['chunk_id']}")
    print(f"Original Text Length: {len(original_text)}")  # Length of original text
    print(f"Stripped Text Length: {len(stripped_text)}")  # Length of stripped text

    # Check if the stripped text is empty
    if not stripped_text:  # If the stripped text is empty (only whitespace or non-visible characters)
        empty_chunks.append(chunk)

print(f"Empty Chunks: {len(empty_chunks)}")

# Optionally, print out the details of the empty chunks
if empty_chunks:
    for chunk in empty_chunks:
        print(json.dumps(chunk, indent=2))  # Pretty print the chunk details
