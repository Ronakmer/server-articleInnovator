
import requests
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['POST'])
def verify_ai_configuration(request):
    try:
        api_key = request.data.get("api_key")
        api_provider = request.data.get("api_provider")
        api_model = request.data.get("api_model")
        anthropic_version= request.data.get("anthropic_version")

        success = False
        if api_provider == "Claude":
            headers = {
                'x-api-key': api_key, # dynamic
                # 'anthropic-version': '2023-06-01', # dynamic
                'anthropic-version': anthropic_version, # dynamic
                'content-type': 'application/json',
            }

            json_data = {
                # 'model': 'claude-3-opus-20240229', # dynamic
                'model': api_model, # dynamic
                'max_tokens': 1024, 
                'messages': [
                    {
                        'role': 'user',
                        'content': 'How many moons does Jupiter have?',
                    },
                ],
            }
            response = requests.post('https://api.anthropic.com/v1/messages', headers=headers, json=json_data)
            print(response.json())
            if response.status_code == 200:
                success = True

        elif api_provider == "OpenAI":
            url = "https://api.openai.com/v1/models"  # Replace with OpenAI's endpoint
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(url, headers=headers)
            print(response.json(),'//')
            if response.status_code == 200:
                success = True

        # return JsonResponse({'success': success})
        return JsonResponse({
            "message": success,
        }, status=200)

    
    except Exception as e:
        print("This error is verify_ai_configuration --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)

