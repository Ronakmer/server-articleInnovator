

import requests
import json 
from django.conf import settings

import os
AI_RATE_LIMITER_BASE_URL = os.getenv("AI_RATE_LIMITER_BASE_URL")


def delete_workspace_api(workspace_slug_id):
    try:

        url = f'{AI_RATE_LIMITER_BASE_URL}/workspace/{workspace_slug_id}'
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$',url)

        headers = {
            "Accept": "application/json"
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            print("Response Code:", response.status_code)
            return response.json(), None  # Success
        else:
            return None, f"API Error: {response.status_code}, {response.text}"
            
    except Exception as e:
        print("This error is register_workspace --->: ", e)
