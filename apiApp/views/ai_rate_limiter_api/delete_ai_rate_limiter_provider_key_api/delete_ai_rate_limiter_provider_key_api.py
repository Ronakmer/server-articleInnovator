

import requests
import json 
from django.conf import settings
import os
AI_RATE_LIMITER_BASE_URL = os.getenv("AI_RATE_LIMITER_BASE_URL")


def delete_ai_rate_limiter_provider_key_api(workspace_slug_id, ai_rate_key_id):
    try:

        # url = f'{AI_RATE_LIMITER_BASE_URL}/workspace/{workspace_slug_id}/key/{ai_rate_key_id}'
        url = f'{AI_RATE_LIMITER_BASE_URL}/provider-key/delete/{ai_rate_key_id}'
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$',url)

        headers = {
            "Accept": "application/json"
        }

        response = requests.delete(url, headers=headers)

        if response.status_code in [200, 201]:
            print("Response Code:", response.status_code)
            return response.json(), None  # Success
        else:
            return None, f"API Error: {response.status_code}, {response.text}"
            
    except Exception as e:
        print("This error is delete_ai_rate_limiter_provider_key_api --->: ", e)




