# nlp/embed/model.py

import logging
from typing import List

import requests
from langchain.embeddings.base import Embeddings

from config.defaults import CONFIG

# Set up logging
logger = logging.getLogger(__name__)


def get_embedding_function(model_name: str = None):
    """Return the embedding function instance."""
    return CloudflareEmbeddings()


class CloudflareEmbeddings(Embeddings):
    print("CloudflareEmbeddings initialized!")  # Add this line

    def __init__(self, model_name: str = None):
        cf_config = CONFIG["CLOUDFLARE"]
        model_id = model_name or cf_config["EMBED_MODEL"]  # use model_name if given

        self.endpoint_url = cf_config["gateway_endpoint"].format(
            account_id=cf_config["account_id"],
            gateway_id=cf_config["gateway_id"],
            model_id=model_id,
        )
        self.token = cf_config["api_token"]
        logger.info(f"Cloudflare embeddings initialized with model {model_id}.")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents."""
        if not all(isinstance(text, str) for text in texts):
            raise ValueError("All input texts must be of type str.")
        logger.debug(f"Embedding {len(texts)} documents.")
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        if not isinstance(text, str):
            raise ValueError(f"Input text must be of type str, but got {type(text)}.")
        logger.debug(f"Embedding query: {text}")
        return self._embed(text)

    def _embed(self, text: str) -> List[float]:
        """Internal method to embed text using Cloudflare API."""
        if not isinstance(text, str):
            raise ValueError(f"Expected a string, but got {type(text)} instead.")

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        payload = {"text": text}
        logger.debug(f"Sending request to Cloudflare with payload: {payload}")

        try:
            response = requests.post(self.endpoint_url, json=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

        result = response.json()
        logger.debug(f"Response from Cloudflare: {len(result['result']['data'][0])}")

        if "result" in result and "data" in result["result"]:
            embedding = result["result"]["data"][0]
            if isinstance(embedding, list):
                return embedding
            else:
                raise ValueError(f"Embedding is not a list: {embedding}")
        else:
            raise ValueError(f"Unexpected response format: {result}")
