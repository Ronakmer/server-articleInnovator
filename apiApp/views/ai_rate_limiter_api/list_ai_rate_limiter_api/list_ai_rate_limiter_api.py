
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
RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")  



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
        if search:
            # filters &= Q(name__icontains=search)
            filters &= (
                Q(name__icontains=search) |
                Q(article_type_id__slug_id__icontains=search)
            )
            
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
        
        
        
        ai_rate_limiter_obj = get_ai_rate_limiter_data(workspace_obj.slug_id) 
        if not ai_rate_limiter_obj.get("success"):
            return JsonResponse({"error": ai_rate_limiter_obj.get("error", "Unknown error"), "success": False}, status=500)
        queue_results = ai_rate_limiter_obj.get("providers", [])
       
        # limit = 2
        total_count = len(queue_results)  # Count the total number of queue results
        queue_results = queue_results[offset:offset + limit]  # Apply pagination
        
        page = (offset // limit) + 1 if limit > 0 else 1
        total_pages = (total_count // limit) + (1 if total_count % limit > 0 else 0)

        
        
        return JsonResponse({
            "data":queue_results,
            "success": True,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },            
        }, status=200)

    except Exception as e:
        print("This error is list_ai_rate_limiter --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)













def get_ai_rate_limiter_data(workspace_slug_id):
    try:
        print(workspace_slug_id, 'workspace_slug_idxxxx')
        

        url = f'{RABBITMQ_BASE_URL}/workspace/{workspace_slug_id}/keys'
        response = requests.get(url)

        # response.raise_for_status()
        data = response.json()

        if "providers" in data:
            return {"success": True, "providers": data["providers"]}
        else:
            return {"error": "Missing 'providers' in response.", "success": False}


    except Exception as e:
        print("This error is get_ai_rate_limiter_data --->: ", e)
        return {"error": "Internal Server error.", "success": False}
