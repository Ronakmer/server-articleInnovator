from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import notification_serializer
from apiApp.models import notification, workspace
from django.db.models import Q
from datetime import date, timedelta
from django.utils import timezone
from apiApp.views.base.process_pagination.process_pagination import process_pagination




# show notification
@api_view(['GET'])
def list_notification(request):
    try:
        request_user = request.user
        
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        read_status = request.GET.get('read_status', '')
        workspace_slug_id = request.GET.get('workspace_slug_id', None)

        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if read_status:
            filters &= Q(read=read_status)
        if search:
            filters &= Q(message__icontains=search) 
        
        if workspace_slug_id:
            try:
                workspace_slug_id = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id=workspace_slug_id)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found.",
                    "success": False,
                }, status=404) 

        try:
            obj = notification.objects.filter(filters)
        except notification.DoesNotExist:
            return JsonResponse({
                "error": "notification not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        serialized_data = notification_serializer(obj, many=True)

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
        print("This error is list_notification --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)





# process notification
@api_view(['PATCH'])
def process_notification(request):
    try:
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace is required fields.",
                "success": False,
            }, status=404)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found.",
                "success": False,
            }, status=404)  
            
            
        try:
            notification_obj = notification.objects.filter(workspace_id = workspace_obj)
        except notification.DoesNotExist:
            return JsonResponse({
                "error": "notification not found.",
                "success": False,
            }, status=404) 
            
        notification_obj.update(seen_time=timezone.now(), read=True)

        serialized_data = notification_serializer(notification_obj, many=True, partial=True)

        return JsonResponse({
            "message": "notifications updated successfully.",
            "data": serialized_data.data,
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is process_notification --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)





# delete notification
@api_view(['DELETE'])
def delete_notification(request, slug_id):
    try:
        request_user = request.user
        try:
            obj = notification.objects.get(slug_id=slug_id)
        except notification.DoesNotExist:
            return JsonResponse({
                "error": "notification not found.",
                "success": False,
            }, status=404) 
        
        workspace_slug_id = request.GET.get("workspace_slug_id")
          
        if not request_user.is_superuser:
            if not workspace_slug_id:
                return JsonResponse({
                    "error": "workspace slug id is required.",
                    "success": False,
                }, status=400)
                
            if (obj.workspace_id.slug_id != workspace_slug_id):
                return JsonResponse({
                    "error": "You Don't have permission.",
                    "success": False,
                }, status=403)

        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_notification --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)





