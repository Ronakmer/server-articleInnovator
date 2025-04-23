

import requests
import json 
from django.conf import settings
import os
AI_RATE_LIMITER_BASE_URL = os.getenv("AI_RATE_LIMITER_BASE_URL")



def register_workspace_api(workspace_slug_id):
    try:

        url = f'{AI_RATE_LIMITER_BASE_URL}/register_workspace'
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$',url)


        headers = {
            'Content-Type': 'application/json',
            # 'Authorization': f'Basic {credentials}',
        }
        data = {
            "workspace_id": workspace_slug_id,
            "providers": [
                {
                    "name": "",
                    "api_key": "",
                    "rate_limit": 0,
                    "rate_limit_period": 0,
                    "config": {
                        "model": ""
                    }
                }
            
            ]
        }


        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print('codess',response.status_code)
            return response.json(), None  # Return JSON response
        else:
            return None, f"API Error: {response.status_code}, {response.text}"
            
            
    except Exception as e:
        print("This error is register_workspace --->: ", e)
