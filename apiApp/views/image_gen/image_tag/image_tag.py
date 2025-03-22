from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import image_tag_serializer
from apiApp.models import image_tag, workspace
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination



# show image tag
@api_view(['GET'])
def list_image_tag(request):
    try:
        request_user = request.user

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
            filters &= Q(name__icontains=search)

        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id=workspace_obj)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found.",
                    "success": False,
                }, status=404)  
            
        try:
            if request_user.is_superuser:
                obj = image_tag.objects.filter(filters).order_by(order_by)
            if request.is_admin:
                if not workspace_slug_id:
                    return JsonResponse({
                        "error": "workspace not found.",
                        "success": False,
                    }, status=404)
                    
                obj = image_tag.objects.filter(filters).order_by(order_by)
        except image_tag.DoesNotExist:
            return JsonResponse({
                "error": "image tag not found.",
                "success": False,
            }, status=404)  

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)


        serialized_data = image_tag_serializer(obj, many=True)
        
        return JsonResponse({
            "data":serialized_data.data,
            "success": False,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },
        }, status=200)

    except Exception as e:
        print("This error is list_image_tag --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add image tag
@api_view(['POST'])
def add_image_tag(request):
    try:
        request_user = request.user
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace is required fields.",
                "success": False,
            }, status=400)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found.",
                "success": False,
            }, status=404)  
            

        # Prepare the data for the serializer, replacing slug with the workspace instance's PK
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id 
        data["created_by"] = request_user.id


        serialized_data = image_tag_serializer(data=data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "success": True,
                "data": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is add_image_tag --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update image tag
@api_view(['PATCH'])
def update_image_tag(request, slug_id):
    try:

        try:
            obj = image_tag.objects.get(slug_id=slug_id)
        except image_tag.DoesNotExist:
            return JsonResponse({
                "error": "image tag not found.",
                "success": False,
            }, status=404)  
        
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace is required fields.",
                "success": False,
            }, status=400)

        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission.",
                "success": False,
            }, status=403)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found.",
                "success": False,
            }, status=404)  
        

        # Remove 'created_by' from the update request data as it should not be updated
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id
        data['created_by'] = obj.created_by.id 
        
        serialized_data = image_tag_serializer(instance=obj, data=data, partial=True)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
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
        print("This error is update_image_tag --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)





# delete image tag
@api_view(['DELETE'])
def delete_image_tag(request, slug_id):
    try:
        try:
            obj = image_tag.objects.get(slug_id=slug_id)
        except image_tag.DoesNotExist:
            return JsonResponse({
                "error": "image tag not found.",
                "success": False,
            }, status=404) 
                
        workspace_slug_id = request.GET.get("workspace_slug_id")  
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
        print("This error is delete_image_tag --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


