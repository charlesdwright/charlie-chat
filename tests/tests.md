### Chunking Documents with LangChain's RecursiveCharacterTextSplitter

- **Purpose**: This script is responsible for chunking large documents into smaller parts using LangChain's `RecursiveCharacterTextSplitter`. This helps break down long texts into manageable pieces that can be processed more effectively by language models.

#### Key Components:
1. **RecursiveCharacterTextSplitter**: A LangChain utility used to split long text documents into smaller chunks of a specified size, with overlap between chunks.
2. **Chunking Configuration**: The size of each chunk and the amount of overlap are configurable and fetched from the global configuration.
3. **Logging**: The process logs debug messages for each chunk created, including the content preview (first 60 characters), and the total number of chunks generated at the end.
4. **UUID**: Each chunk is assigned a unique `chunk_id` to differentiate it.
5. **Chunk Metadata**: Each chunk includes metadata such as the source of the document for easy traceability.

#### Functionality:
- **Input**: A list of LangChain `Document` objects.
- **Output**: A list of dictionaries, each containing:
  - `chunk_id`: Unique identifier for each chunk.
  - `text`: The chunked text itself.
  - `source`: The source of the original document.

#### Example:
For a document with content like:
- "LangChain is a powerful framework for building AI-driven applications. It provides seamless integration with various LLMs..."
It might be chunked into:
- "LangChain is a powerful framework for building AI-driven applications..."
- "It provides seamless integration with various LLMs..."

### Test Embedding for Cloudflare Embeddings

- **Purpose**: This script tests the functionality of the embedding process using the `CloudflareEmbeddings` class.
- **Steps**:
  1. **Create the Embedding Instance**: An instance of `CloudflareEmbeddings` is initialized.
  2. **Test Embedding of Documents**: A list of test documents is passed to the `embed_documents()` method to verify the embedding functionality.
  3. **Test Embedding of Query**: A test query is passed to the `embed_query()` method to verify query embedding.
  4. **Validate Embedding Format**: Ensures the response from the embedding API is in the expected format (list of floats).
  5. **Error Handling**: Catches and logs any exceptions that occur during execution.

### Logging

- **Level**: Logs are generated at the `INFO` level.
- **Output**: Logs include status updates on the embedding process, as well as any errors encountered.


### Test Query for Retrieval Chain

- **Purpose**: This script tests the functionality of the retrieval chain.
- **Steps**:
  1. **Create the RetrievalQA Chain**: Initializes the chain using the `create_retrieval_qa_chain()` function.
  2. **Define the Query**: A test query ("What is LangChain?") is defined.
  3. **Log Query Information**: Logs the query and its type to ensure it is a string.
  4. **Execute the Query**: The query is executed through the chain, and the response is logged.
  5. **Log Sources**: Logs the source documents related to the response.
- **Error Handling**: Catches and logs any exceptions that occur during execution.

### Logging

- **Level**: Logs are generated at the `DEBUG` level.
- **Output**: Logs include query type, response details, source documents, and any errors encountered.
