# - nlp/llms/cloudflare.py

import requests
from typing import Optional, List
from langchain.llms.base import LLM
from config.defaults import CONFIG

from pydantic import Field

class CloudflareLLM(LLM):
    model_input_key: str = "prompt"
    model_id: Optional[str] = Field(default=None)
    endpoint_url: Optional[str] = Field(default=None)
    token: Optional[str] = Field(default=None)

    def __init__(self, model_name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)  # important for pydantic
        cf_config = CONFIG["CLOUDFLARE"]
        self.model_id = model_name or cf_config["llm_model"]
        self.endpoint_url = cf_config["gateway_endpoint"].format(
            account_id=cf_config["account_id"],
            gateway_id=cf_config["gateway_id"],
            model_id=self.model_id
        )
        self.token = cf_config["api_token"]


    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        payload = {self.model_input_key: prompt}
        if stop:
            payload["stop"] = stop

        response = requests.post(self.endpoint_url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()

        try:
            text = result["result"]["response"]
            if not isinstance(text, str):
                raise TypeError(f"Expected response text to be a string, got: {type(text)}")
        except Exception as e:
            raise ValueError(f"Unexpected LLM response format: {result}") from e

        return text.strip()

    @property
    def _llm_type(self) -> str:
        return "cloudflare"
