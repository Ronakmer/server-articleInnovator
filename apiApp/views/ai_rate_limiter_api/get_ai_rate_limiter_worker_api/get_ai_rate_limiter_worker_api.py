
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





def get_ai_rate_limiter_worker_data(workspace_slug_id):
    try:
        print(workspace_slug_id, 'workspace_slug_idxxxx')
        
        url = f'{AI_RATE_LIMITER_BASE_URL}/workers/{workspace_slug_id}'
        
        params = {
            'workspace_id': workspace_slug_id,
            'status':'running',
        }

        response = requests.get(url, params=params)
        print(response,'responsexxx')

        data = response.json()
        print(data,'dataxsxsxs')

        if response.status_code in [200, 201]:
            worker_data = data.get("workers", [])
            return {"success": True, "worker_data": data}
        else:
            return {"error": "ai-rate-limiter Request failed", "success": False}

    except Exception as e:
        print("This error is get_ai_rate_limiter_worker_data --->: ", e)
        return {"error": "Internal Server error.", "success": False}




