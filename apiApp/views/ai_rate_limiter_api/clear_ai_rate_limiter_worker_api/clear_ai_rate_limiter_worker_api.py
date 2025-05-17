
import requests
import json 
from django.conf import settings
import os
AI_RATE_LIMITER_BASE_URL = os.getenv("AI_RATE_LIMITER_BASE_URL")
from rest_framework.decorators import api_view
from django.http import JsonResponse


@api_view(['POST'])
def clear_ai_rate_limiter_worker(request):
    try:
        workspace_slug_id = request.data.get('workspace_slug_id')

        url = f'{AI_RATE_LIMITER_BASE_URL}/workspace/clear/{workspace_slug_id}'

        response = requests.post(url)  # No payload/body, just POST

        if response.status_code in [200, 201]:
            print("Workspace cleared successfully.")
            response_obj = response.json()
            return JsonResponse({
                "message": f"Worker cleared successfully.",
                "success": True,
                "data": response.json(),
            })

            # return Response(response_obj, status=response.status_code)
        else:
            print("Failed to clear workspace:", response.status_code, response.text)
            return JsonResponse({
                "error": f"Failed to clear worker",
                "success": False
            }, status=response.status_code)

            # return Response(
            #     {"error": f"API Error: {response.status_code}, {response.text}"},
            #     status=response.status_code
            # )

    except Exception as e:
        print("Exception in clear_ai_rate_limiter_worker:", e)
        return None, str(e)
