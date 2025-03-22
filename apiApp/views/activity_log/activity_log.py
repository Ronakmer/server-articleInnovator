from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import activity_log_serializer
from apiApp.models import  workspace, activity_log
from django.db.models import Q
from datetime import date, timedelta
from apiApp.views.base.process_pagination.process_pagination import process_pagination



# show activity_log
@api_view(['GET'])
def list_activity_log(request):
    try:
        request_user = request.user
        
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        workspace_slug_id = request.GET.get('workspace_slug_id', None)    
    
        # Initialize filters
        filters = Q()
    
        if search:
            filters &= Q(level__icontains=search) 

        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id_id=workspace_obj)
                
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found ",
                    "success": False,
                }, status=404)

        if not request_user.is_superuser:
            filters &= Q(user_status=True)
            
        try:
            obj = activity_log.objects.filter(filters, user_status=True).order_by(order_by)
        except activity_log.DoesNotExist:
            return JsonResponse({
                "error": "log record not found",
                "success": False,
            }, status=404)
  
  
        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        serialized_data = activity_log_serializer(obj, many=True)
        
        return JsonResponse({
            "data":serialized_data.data,
            "success": True,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },
             
        }, status=200)

    except Exception as e:
        print("This error is list_activity_log --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)
