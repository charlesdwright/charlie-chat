# config/defaults.py

import os

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define the CONFIG dictionary for visual clarity
CONFIG = {
    "DEFAULT_PROVIDER": "CLOUDFLARE",  # default LLM provider
    "DEFAULT_VECTORDB": "CHROMA",  # default vector database
    "CLOUDFLARE": {
        "gateway_endpoint": "https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/workers-ai/{model_id}",
        "llm_model": "@cf/openchat/openchat-3.5-0106",  # Cloudflare's LLM model
        "EMBED_MODEL": "@cf/baai/bge-small-en-v1.5",  # Cloudflare's embedding model
        "api_token": os.getenv("CLOUDFLARE_API_TOKEN"),
        "account_id": os.getenv("CLOUDFLARE_ACCOUNT_ID"),
        "gateway_id": os.getenv("CLOUDFLARE_GATEWAY_ID"),
        "chunk_overlap": 50,
        "similarity_threshold": 0.75,
        "debug_mode": True,  # Enable debug mode
    },
    "OPENAI": {
        "api_base": "https://api.openai.com/v1",
        "embedding_model": "text-embedding-ada-002",
        "chat_model": "gpt-4",
        "max_tokens": 400,
        "api_key": os.getenv("OPENAI_API_KEY"),  # OpenAI API key
    },
    "CHROMA": {
        "PERSIST_DIR": "nlp/persist/db/chroma",  # Directory for the Chroma DB
        "COLLECTION_NAME": "document_collection",  # Collection name in the vector DB
    },
    "GENERAL": {
        "default_similarity_top_k": 3,  # Top K results for similarity
        "max_tokens": 100,  # Token limit for the models
        "tokenizer_encoding": "gpt2",  # Tokenizer to use
        "CHUNK_SIZE": 500,  # Chunk size for document splitting
        "CHUNK_OVERLAP": 100,  # Chunk overlap for document splitting
        "CHUNK_FILE": "outputs/chunked_docs.jsonl",  # Path for chunked documents
    },
}

# Optional: Validate required environment variables for Cloudflare and OpenAI
required_vars = [
    "CLOUDFLARE_API_TOKEN",
    "CLOUDFLARE_ACCOUNT_ID",
    "CLOUDFLARE_GATEWAY_ID",
    "OPENAI_API_KEY",
]
for var in required_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")


# Utility function to build the Cloudflare LLM URL
def build_cf_url(model_id: str = None) -> str:
    cf = CONFIG["CLOUDFLARE"]
    model_id = model_id or cf["llm_model"]
    return cf["gateway_endpoint"].format(
        account_id=cf["account_id"],
        gateway_id=cf["gateway_id"],
        model_id=model_id.lstrip("@cf/"),  # Clean any leading '@cf/' prefix
    )
