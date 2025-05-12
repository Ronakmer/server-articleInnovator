

import requests
import json 
from django.conf import settings
import os
AI_RATE_LIMITER_BASE_URL = os.getenv("AI_RATE_LIMITER_BASE_URL")



def update_ai_rate_limiter_provider_key_api(workspace_slug_id, provider_data):
    try:
        print(provider_data, 'provider_datazx')

        url = f'{AI_RATE_LIMITER_BASE_URL}/workspace/{workspace_slug_id}/key'

        # Get model from comma-separated string
        api_models = provider_data.get("api_model", "")
        models = [m.strip() for m in api_models.split(",") if m.strip()]
        model = models[0] if models else ""

        # Build request payload
        payload = {
            "provider": provider_data.get("api_provider", "OpenAI").lower(),
            "api_key": provider_data.get("api_key", ""),
            "config": {"model": model},
            "rate_limit": int(provider_data.get("rate_limit", 1000)),
            "rate_limit_period": int(provider_data.get("rate_limit_period", 60))
        }

        headers = {
            'Content-Type': 'application/json',
        }

        print("Request payload:", payload)

        # Send request
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print("API key updated successfully.")
            return response.json(), None
        else:
            print("Failed API key update:", response.status_code, response.text)
            return None, f"API Error: {response.status_code}, {response.text}"

    except Exception as e:
        print("Exception in update_ai_rate_limiter_provider_key_api:", e)
        return None, str(e)
