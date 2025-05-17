

import requests
import json 
from django.conf import settings
import os
AI_RATE_LIMITER_BASE_URL = os.getenv("AI_RATE_LIMITER_BASE_URL")



def update_ai_rate_limiter_provider_key_api(workspace_slug_id, provider_data):
    try:
        print(provider_data, 'provider_datazx')

        ai_rate_key_id = provider_data.get("ai_rate_key_id", "")
        print(ai_rate_key_id,'ai_rate_key_idx')
        url = f'{AI_RATE_LIMITER_BASE_URL}/provider-key/update/{ai_rate_key_id}'

        # Extract and prepare model list
        api_models = provider_data.get("api_model", "")
        models = [m.strip() for m in api_models.split(",") if m.strip()]
        model = models[0] if models else ""

        # Set default values and override if provided
        api_version = provider_data.get("api_version", "")
        endpoint = provider_data.get("api_url", "")
        provider_name = provider_data.get("api_provider", "").lower()

        payload = {
            "api_key": provider_data.get("api_key", ""),
            "config": {
                "api_version": api_version,
                "endpoint": endpoint,
                "model": model
            },
            "name": provider_name,
            "rate_limit": int(provider_data.get("rate_limit", 1000)),
            "rate_limit_period": str(provider_data.get("rate_limit_period", 600)),
        }

        headers = {
            'Content-Type': 'application/json',
        }

        print("Request payload:", payload)

        response = requests.put(url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            print("API key updated successfully.")
            return response.json(), None
        else:
            print("Failed to update API key:", response.status_code, response.text)
            return None, f"API Error: {response.status_code}, {response.text}"

    except Exception as e:
        print("Exception in update_ai_rate_limiter_provider_key_api:", e)
        return None, str(e)
