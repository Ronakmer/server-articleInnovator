from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import motivation_serializer
from apiApp.models import motivation, workspace
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show motivation
@api_view(['GET'])
def list_motivation(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(quote__icontains=search) 

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
            obj = motivation.objects.filter(filters).order_by(order_by)
        except motivation.DoesNotExist:
            return JsonResponse({
                "error": "motivation not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        serialized_data = motivation_serializer(obj, many=True)
        
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
        print("This error is list_motivation --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add motivation
@api_view(['POST'])
def add_motivation(request):
    try:
        request_user = request.user

        # Retrieve workspace using slug ID
        workspace_slug_ids = request.data.get("workspace_slug_id")  
        if not workspace_slug_ids:
            return JsonResponse({
                "error": "workspace slug id is required.",
                "success": False,
            }, status=400)
        
        if workspace_slug_ids:
            workspace_slugs = workspace_slug_ids.split(",") 

        try:
            workspace_objs = workspace.objects.filter(slug_id__in=workspace_slugs)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found ",
                "success": False,
            }, status=404)
            
        data = request.data.copy()
        data['created_by'] = request_user.id 

        # print(data,'data')
        serialized_data = motivation_serializer(data=data)
        
        if serialized_data.is_valid():
            motivation_obj = serialized_data.save()
            motivation_obj.workspace_id.set(workspace_objs)              
            
            return JsonResponse({
                "message": "Data added successfully.",
                "data": serialized_data.data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is add_motivation --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update motivation
@api_view(['PATCH'])
def update_motivation(request, slug_id):
    try:
        request_user = request.user
        
        try:
            obj = motivation.objects.get(slug_id=slug_id)
        except motivation.DoesNotExist:
            return JsonResponse({
                "error": "motivation not found.",
                "success": False,
            }, status=404)   
            
        # Retrieve workspace using slug ID
        workspace_slug_ids = request.data.get("workspace_slug_id")  
        if not workspace_slug_ids:
            return JsonResponse({
                "error": "workspace slug id is required.",
                "success": False,
            }, status=400)
            
        if workspace_slug_ids:
            workspace_slugs = workspace_slug_ids.split(",") 

        try:
            workspace_objs = workspace.objects.filter(slug_id__in=workspace_slugs)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found ",
                "success": False,
            }, status=404)
            
        if not request_user.is_superadmin:    
            if not set(workspace_objs).intersection(set(obj.workspace_id.all())):
                return JsonResponse({"error": "You don't have permission.","success": False}, status=403)

        serialized_data = motivation_serializer(instance=obj, data=request.data, partial=True)        
        
        if serialized_data.is_valid():
            obj = serialized_data.save()
            obj.workspace_id.set(workspace_objs)
            
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "data": serialized_data.data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is update_motivation --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# delete motivation
@api_view(['DELETE'])
def delete_motivation(request, slug_id):
    try:
        request_user = request.user
        
        # Fetch the motivation object
        try:
            obj = motivation.objects.get(slug_id=slug_id)
        except motivation.DoesNotExist:
            return JsonResponse({"error": "Motivation not found.","success": False}, status=404)

        # Get workspace_slug_id from request
        workspace_slug_id = request.GET.get("workspace_slug_id")
        if not workspace_slug_id:
            return JsonResponse({"error": "Workspace slug ID is required.","success": False}, status=400)

        # Check if the user has permission (i.e., workspace_slug_id exists in obj.workspace_id)
        workspace_objs = obj.workspace_id.all()
        if not request_user.is_superadmin:
            if not any(ws.slug_id == workspace_slug_id for ws in workspace_objs):
                return JsonResponse({"error": "You don't have permission.","success": False}, status=403)

        # Delete the motivation object
        obj.delete()

        return JsonResponse({"message": "Data deleted successfully.","success": True}, status=200)

    except Exception as e:
        print("Error in delete_motivation --->:", str(e))
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


