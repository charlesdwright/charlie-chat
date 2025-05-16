# nlp/llms/cloudflare.py

import os
import requests
from langchain.llms.base import LLM
from langchain.embeddings.base import Embeddings

class CloudflareLLM(LLM):
    model = "@cf/openchat/openchat-3.5-0106"
    base_url = "https://gateway.ai.cloudflare.com/v1"
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    gateway_id = os.getenv("CLOUDFLARE_GATEWAY_ID")

    @property
    def _llm_type(self) -> str:
        return "cloudflare"

    def _call(self, prompt: str, **kwargs) -> str:
        url = f"{self.base_url}/{self.account_id}/{self.gateway_id}/workers-ai/{self.model.lstrip('@cf/')}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.post(url, json={"prompt": prompt}, headers=headers)
        result = response.json()
        return result["result"]["response"]


class CloudflareEmbeddings(Embeddings):
    model = "@cf/baai/bge-small-en-v1.5"
    base_url = "https://gateway.ai.cloudflare.com/v1"
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    gateway_id = os.getenv("CLOUDFLARE_GATEWAY_ID")

    def embed_documents(self, texts, **kwargs):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        url = f"{self.base_url}/{self.account_id}/{self.gateway_id}/workers-ai/{self.model.lstrip('@cf/')}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.post(url, json={"text": text}, headers=headers)
        return response.json()["result"]["embedding"]
