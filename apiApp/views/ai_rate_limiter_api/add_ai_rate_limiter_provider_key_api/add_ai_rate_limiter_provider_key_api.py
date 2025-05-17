

import requests
import json 
from django.conf import settings
import os
AI_RATE_LIMITER_BASE_URL = os.getenv("AI_RATE_LIMITER_BASE_URL")


def add_ai_rate_limiter_provider_key_api(workspace_slug_id, provider_data):
    url = f'{AI_RATE_LIMITER_BASE_URL}/provider-key/add'
    headers = {'Content-Type': 'application/json'}

    try:
        api_key = provider_data.get("api_key", "")
        provider = provider_data.get("api_provider", "openai").lower()
        models = provider_data.get("api_model", "").split(",")
        rate_limit = provider_data.get("rate_limit", 1000)
        rate_limit_period = provider_data.get("rate_limit_period", 60)

        for model in models:
            config = {
                "model": model.strip()
            }

            # Add optional fields only if they are present in provider_data
            if "api_version" in provider_data:
                config["api_version"] = provider_data["api_version"]
            if "endpoint" in provider_data:
                config["endpoint"] = provider_data["endpoint"]

            payload = {
                "workspace_id": workspace_slug_id,
                "name": provider,
                "api_key": api_key,
                "config": config or None,
                "rate_limit": rate_limit,
                "rate_limit_period": rate_limit_period
            }

            print(f"Sending data to AI Rate Limiter: {payload}")
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code in [200, 201]:

                print(f"Response [200]: {response.json()}")
                return response.json(), None
            else:
                print(f"Error response [{response.status_code}]: {response.text}")
                return None, f"API Error: {response.status_code}, {response.text}"

    except Exception as e:
        print("Exception in add_ai_rate_limiter_provider_key_api:", e)
        return None, str(e)





