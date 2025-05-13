# Embedding Process

The embedding process involves transforming text into vector representations (embeddings) that can be used for document retrieval and analysis. Below is a breakdown of the key steps in the process:

1. **Initialization**
   - The `CloudflareEmbeddings` class is initialized with the necessary API endpoint and authentication token, provided via the configuration (`CONFIG`).

2. **Embed Documents**
   - The `embed_documents` method accepts a list of text documents (strings) and generates embeddings for each document using the Cloudflare API.
   - The embedding is done by calling the `_embed` method, which sends a POST request to the Cloudflare endpoint with the text and returns a vector.

3. **Embed Single Query**
   - The `embed_query` method works similarly to `embed_documents`, but it is designed to process a single query and return its embedding.

4. **Interaction with Cloudflare API**
   - The actual embedding process takes place in the `_embed` method, where a POST request is made to the Cloudflare API endpoint.
   - The request includes the text to be embedded, and the response contains the vector embedding for that text.

5. **Error Handling**
   - The system checks for correct input types (strings) and ensures the API response format is correct. If an issue arises (e.g., non-string input or unexpected response format), an error is raised.

6. **Return Embeddings**
   - The embeddings are returned as lists of floating-point values representing the vectorized form of the input text.

### Example of Embedding a Query
```python
    embedding = CloudflareEmbeddings().embed_query("What is LangChain?")

### Example of Embedding Documents
'''python
    embeddings = CloudflareEmbeddings().embed_documents(["Text 1", "Text 2"])

### Key Components

- **CloudflareEmbeddings**: Custom class for embedding text using Cloudflare's API.
- **Requests**: Used for making API calls to Cloudflare.
- **Error Handling**: Ensures input validation and API response correctness.
- **Embedding Function**: Converts text into embeddings (vector representations).



## Detailed Breakdown of Processes

> Fresh run, clean vectorstore
>
>     # python
>     ingest.py [source folder] --purge
>
> Resume from disk and purge
>
>     # python
>     ingest.py [source folder] --from-disk --purge
>
> Debugging with purge
>
>     # python
>     ingest.py [source folder] --debug --purge

### 1. Set up embedding function
    # python
    embedding_function = CloudflareEmbeddings(model_name=model_name)

-   **What happens**: This line initializes the embedding function that will convert your document content into vectors (embeddings).

-   **Why**: The  `CloudflareEmbeddings`  class is used to wrap the Cloudflare Embedding model. You pass the model name (`model_name`) as a parameter to specify which model to use.


----------

### 2. Initialize Chroma Client
    # python
    client = chromadb.PersistentClient(path=persist_dir)

-   **What happens**: This creates a persistent client connected to Chroma, using the specified  `persist_dir`  to store the vector database on disk.

-   **Why**: Chroma is the vector database where the embeddings will be stored. By using a persistent client, the client can read and write to the vector store, and it will maintain its state across runs.


----------

### 3. Purge the Vector Store (if  `purge=True`)
    # python
    if purge:
	    try:
            logger.warning(f"🧨 Purging vectorstore collection: {collection_name}'...")
            client.delete_collection(collection_name)
         except Exception as e:
            logger.warning(f"⚠️ Failed to delete collection '{collection_name}': {e}")

-   **What happens**: This part is the  **new functionality**  we added based on the  `purge`  parameter:

    -   If  `purge`  is set to  `True`, it will try to  **delete**  the  **existing collection**  in the Chroma vector store (the one with the name specified in  `collection_name`).

    -   A warning is logged when it starts purging (`🧨 Purging vectorstore collection`).

    -   If there’s an issue with deleting (for example, if the collection doesn't exist), it will catch the error and log a warning (`⚠️ Failed to delete`).

-   **Why**: Purging ensures that if you're re-ingesting new data and you don’t want to retain old embeddings, this step clears out the vector store before inserting new ones. This is useful when you want a completely fresh set of embeddings, without the risk of old or obsolete data being mixed in.


----------

### 4. Create/Get Collection

python
`collection = client.get_or_create_collection(collection_name)`

-   **What happens**: If the collection doesn’t exist, this line creates a new collection with the name  `collection_name`. If it already exists, it simply retrieves the existing collection.

-   **Why**: You need a collection in Chroma to store embeddings. By using  `get_or_create_collection()`, the function ensures that there’s always a valid collection available — either by getting the existing one or creating a new one.


----------

### 5. Clean up other collections (optional)

    # python
    for c in client.list_collections():
    	if c.name != collection_name:
            logger.info(f"🗑️ Deleting unused collection: {c.name}")
            client.delete_collection(c.name)

-   **What happens**: This checks all collections in the Chroma vector store and deletes any collection that  **doesn't match**  the desired  `collection_name`.

-   **Why**: This step helps keep the vector store clean by ensuring that there are no unnecessary collections hanging around. If you’re only interested in one collection for the current session, deleting others can keep things organized and reduce clutter.


----------

### 6. Embed and Add Documents
    # python
    for document in documents:
        content = document.page_content.strip()
        if not content:
    	    logger.warning( f"❌ Document {document.metadata.get('chunk_id')} has empty content."
            )
    	continue

-   **What happens**: We loop over each document and extract the text (`content`). If the content is empty, we skip processing that document and log a warning.

-   **Why**: You don’t want to embed empty content — this step ensures that only valid, non-empty documents are processed.


----------

### 7. Generate Embedding for Each Document

    # python
    doc_id = str(document.metadata.get("chunk_id") or uuid.uuid4())
    try:
	    embedding = embedding_function.embed_documents([content])[0]
	    if  not embedding:
		    logger.warning(f"❌ Empty embedding for {doc_id}")
		    continue
	    logger.debug(f"Embedding for {doc_id}: {embedding[:5]}...")

-   **What happens**:

    -   A unique document ID (`doc_id`) is generated. It’s either pulled from the document metadata (specifically  `chunk_id`) or a new UUID is generated.

    -   The content of the document is passed through the embedding function, which returns a vector embedding.

    -   If the embedding is empty, it skips that document and logs a warning. The first few values of the embedding are logged for debugging purposes.

-   **Why**: You need to generate embeddings for the content of each document to store it in the vector store. If any embedding fails, we log the issue and continue with the next document to avoid halting the whole process.


----------

### 8. Add Embedding to Collection

    # python
    collection.add(
        documents=[content],
        metadatas=[document.metadata],
        embeddings=[embedding],
        ids=[doc_id],
    )
    successful_additions += 1`

-   **What happens**: The embedding (vector) for each document is stored in the Chroma collection along with the original content and metadata (like  `chunk_id`).

    -   `documents=[content]`: The text content of the document.

    -   `metadatas=[document.metadata]`: The metadata associated with the document (like source, chunk ID, etc.).

    -   `embeddings=[embedding]`: The generated embedding vector.

    -   `ids=[doc_id]`: The unique document ID.

-   **Why**: This adds the embedding to the Chroma vector store. This is the key operation where your embeddings are actually saved in the database.


----------

### 9. Summary Logging
    # python
    logger.info(f"✅ Embedded and stored {successful_additions} documents in {persist_dir}")
    logger.info(f"Collection '{collection_name}' now contains {collection.count()} documents.")

-   **What happens**: After all documents have been processed, the function logs:

    -   The number of successfully embedded and stored documents.

    -   The total count of documents in the Chroma collection after the process is complete.

-   **Why**: This provides a summary of the operation, so you know how many documents were added and the current state of the collection.


----------

## Conclusion

-   **Purging**: The  `purge`  functionality is useful when you want to start fresh and delete old data. It deletes the collection from the Chroma store if requested.

-   **Embedding and Storing**: The function processes each document, generates embeddings, and stores them in Chroma, cleaning up old data along the way.
