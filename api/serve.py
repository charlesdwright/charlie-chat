# server/serve.py

from fastapi import FastAPI
from langserve import add_routes
from langchain.schema import HumanMessage
from langchain.llms.base import LLM
from config.defaults import CONFIG, build_cf_url
import requests

class CloudflareWorkerLLM(LLM):
    def _call(self, prompt: str, **kwargs) -> str:
        url = build_cf_url()
        headers = {
            "Authorization": f"Bearer {CONFIG['CLOUDFLARE']['api_token']}",
            "Content-Type": "application/json"
        }
        payload = {"messages": [{"role": "user", "content": prompt}]}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()["result"]["response"]

    @property
    def _llm_type(self) -> str:
        return "cloudflare-worker"

app = FastAPI()
llm = CloudflareWorkerLLM()
add_routes(app, llm, path="/chat")
