
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

from apiApp.views.ai_rate_limiter_api.get_ai_rate_limiter_provider_key_api.get_ai_rate_limiter_provider_key_api import get_ai_rate_limiter_provider_data
from apiApp.views.ai_rate_limiter_api.get_ai_rate_limiter_worker_api.get_ai_rate_limiter_worker_api import get_ai_rate_limiter_worker_data


# show ai_rate_limiter
@api_view(['GET'])
# @workspace_permission_required
def list_ai_rate_limiter(request):
    try:
        request_user = request.user
        
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        article_type_slug_id = request.GET.get('article_type_slug_id', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()
        if slug_id:
            filters &= Q(slug_id=slug_id)
        # if search:
        #     # filters &= Q(name__icontains=search)
        #     filters &= (
        #         Q(name__icontains=search) |
        #         Q(article_type_id__slug_id__icontains=search)
        #     )
            
        print(search,'searchx')


        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
            filters &= Q(workspace_id=workspace_obj)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found.",
                "success": False,
            }, status=404)  
            
        
        # try:
        #     obj = ai_configuration.objects.filter(filters).order_by(order_by)
        # except ai_configuration.DoesNotExist:
        #     return JsonResponse({
        #         "error": "ai_configuration not found.",
        #         "success": False,
        #     }, status=404) 
        
        
        
        ai_rate_limiter_provider_data = get_ai_rate_limiter_provider_data(workspace_obj.slug_id) 
        print(ai_rate_limiter_provider_data,'ai_rate_limiter_provider_dataxxxxx')
        
        provider_status = ai_rate_limiter_provider_data.get("success")
        if provider_status == False: 
            return JsonResponse({"error": ai_rate_limiter_provider_data.get("error", "Unknown error"), "success": False}, status=500)
        
        
        ai_rate_limiter_worker_data = get_ai_rate_limiter_worker_data(workspace_obj.slug_id)
        worker_status = ai_rate_limiter_worker_data.get("success")
        if worker_status == False: 
            return JsonResponse({"error": ai_rate_limiter_worker_data.get("error", "Unknown error"), "success": False}, status=500)
        
        
        ai_rate_limiter_provider_data.pop("success", None)
        ai_rate_limiter_worker_data.pop("success", None)
        ai_rate_limiter_obj={
            'ai_rate_limiter_provider_data':ai_rate_limiter_provider_data,
            'ai_rate_limiter_worker_data':ai_rate_limiter_worker_data,
        }
        
        return JsonResponse({
            "data":ai_rate_limiter_obj,
            "success": True,
            "pagination": {
                "total_count": "",
                "page": "",
                "page_size": "",
                "total_pages": ""
            },            
        }, status=200)

    except Exception as e:
        print("This error is list_ai_rate_limiter --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)











