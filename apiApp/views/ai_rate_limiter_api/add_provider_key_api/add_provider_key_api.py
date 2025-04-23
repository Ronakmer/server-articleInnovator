

import requests
import json 
from django.conf import settings
import os
AI_RATE_LIMITER_BASE_URL = os.getenv("AI_RATE_LIMITER_BASE_URL")



def add_provider_key_api(workspace_slug_id, provider_data):
    try:

        url = f'{AI_RATE_LIMITER_BASE_URL}/workspace/{workspace_slug_id}/key'

        models = provider_data.get("api_model", "").split(",")
        print(models,'modelsssssssssssssssssssss')

        headers = {
            'Content-Type': 'application/json',
            # 'Authorization': f'Basic {credentials}',
        }
        
        for model in models:
            data = {
                "provider": provider_data.get("api_provider", "OpenAI").lower(),
                "api_key": provider_data.get("api_key", ""),
                "config": {"model": model.strip()},
                "rate_limit": provider_data.get("rate_limit", 1000),  # Use a valid default value
                "rate_limit_period": provider_data.get("rate_limit_period", 60)  # Use a valid default value
            }
            
            print(data,'data........')

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                print('codess',response.status_code)
                print('codess',response.json())
                return response.json(), None  # Return JSON response
            else:
                return None, f"API Error: {response.status_code}, {response.text}"
            
            
    except Exception as e:
        print("This error is add_provider_key_api --->: ", e)







