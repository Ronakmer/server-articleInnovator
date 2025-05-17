


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import ai_configuration_serializer
from apiApp.models import prompt, workspace, article_type, user_detail, domain, ai_configuration
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from apiApp.views.decorator.domain_decorator import domain_permission_required
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination
import json
import os, requests
AI_RATE_LIMITER_BASE_URL = os.getenv("AI_RATE_LIMITER_BASE_URL")  



@api_view(['POST'])
def scale_ai_rate_limiter_worker(request):
    try:
        
        count = request.data.get('count')
        workspace_slug_id = request.data.get('workspace_slug_id')

        url = f'{AI_RATE_LIMITER_BASE_URL}/workers/scale/{workspace_slug_id}'
        
        payload = {
            "count": count,
        }
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload)

        print(response,'responsexxx')
        # response.raise_for_status()
        data = response.json()
        print(data,'sssssssssssssssdddddddddddddddddd')
    
        if response.status_code in [200, 201]:
            return JsonResponse({
                "message": f"Worker scaled successfully.",
                "success": True
            })
        else:
            return JsonResponse({
                "error": f"Failed to scale worker: {response.status_code} - {response.text}",
                "success": False
            }, status=response.status_code)


    except Exception as e:
        print("This error is scale_ai_rate_limiter_worker --->: ", e)
        return {"error": "Internal Server error.", "success": False}



