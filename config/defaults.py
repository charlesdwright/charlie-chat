import os

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

CONFIG = {
    "DEFAULT_PROVIDER": "CLOUDFLARE",
    "DEFAULT_VECTORDB": "CHROMA",
    "CLOUDFLARE": {
        "gateway_endpoint": "https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/workers-ai/{model_id}",
        "llm_model": "@cf/openchat/openchat-3.5-0106",
        "EMBED_MODEL": "@cf/baai/bge-small-en-v1.5",
        "api_token": os.getenv("CLOUDFLARE_API_TOKEN"),
        "account_id": os.getenv("CLOUDFLARE_ACCOUNT_ID"),
        "gateway_id": os.getenv("CLOUDFLARE_GATEWAY_ID"),
        "chunk_overlap": 50,
        "similarity_threshold": 0.75,
        "debug_mode": True,
    },
    "OPENAI": {
        "api_base": "https://api.openai.com/v1",
        "embedding_model": "text-embedding-ada-002",
        "chat_model": "gpt-4",
        "max_tokens": 400,
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    "CHROMA": {
        "PERSIST_DIR": "nlp/persist/db/chroma",
        "COLLECTION_NAME": "document_collection",
    },
    "GENERAL": {
        "default_similarity_top_k": 3,
        "max_tokens": 100,
        "tokenizer_encoding": "gpt2",
        "CHUNK_SIZE": 500,
        "CHUNK_OVERLAP": 100,
        "CHUNK_FILE": "outputs/chunked_docs.jsonl",
    },
    "MEMORY": {
        # Options: "buffer", "window", "summary"
        "type": "window",
        "window_size": 3,  # Used if type == "window"
        "max_token_limit": 8000,  # Used if type == "summary"
    },
    "CHAIN": {
        "return_source_documents": True  # Set to True if you want debug/tracing mode
    },
}

# Optional: Validate required environment variables
required_vars = [
    "CLOUDFLARE_API_TOKEN",
    "CLOUDFLARE_ACCOUNT_ID",
    "CLOUDFLARE_GATEWAY_ID",
    "OPENAI_API_KEY",
]
for var in required_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")


# Utility function to build Cloudflare LLM endpoint URL
def build_cf_url(model_id: str = None) -> str:
    cf = CONFIG["CLOUDFLARE"]
    model_id = model_id or cf["llm_model"]
    return cf["gateway_endpoint"].format(
        account_id=cf["account_id"],
        gateway_id=cf["gateway_id"],
        model_id=model_id.lstrip("@cf/"),
    )
