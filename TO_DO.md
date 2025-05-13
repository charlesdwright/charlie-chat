### To-Do: Add Title Metadata to Document Chunks

- **Goal**: Modify the chunking process to include the document title (e.g., as the filename) in the metadata for each chunk.

- **Impact**:
  1. **Metadata in Vector Store**: Each chunk will contain document title metadata, improving traceability.
  2. **Query Output**: Titles will be available in search results to provide context on where each chunk came from.
  3. **Contextual Relevance**: Titles can help with ranking and filtering search results based on the document.
  4. **Performance**: Slight increase in storage size and minimal impact on query speed.
  5. **Consistency**: Ensure filenames are sanitized for consistency and avoid conflicts.
  6. **Ingestion Complexity**: Slight increase in ingestion time but minimal for small to medium datasets.

- **Action**: Update `chunker.py` to add title metadata to each chunk when processing documents.
