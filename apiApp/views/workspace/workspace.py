from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import workspace_serializer
from apiApp.models import workspace, user_detail
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from django.db.models import Q
from apiApp.views.base.dynamic_avatar_image_process.dynamic_avatar_image_process import dynamic_avatar_image_process
from apiApp.views.base.process_pagination.process_pagination import process_pagination


@api_view(['GET'])
# @workspace_permission_required
def list_workspace(request):
    try:
        request_user = request.user
        
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()
        if slug_id:
            filters &= Q(slug_id=slug_id)

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if search:
            filters &= Q(name__icontains=search) 

        
        if request_user.is_superuser:      
            obj = workspace.objects.filter(filters).order_by(order_by)
            
        if request.is_admin:
            workspace_ids = user_detail.objects.filter(user_id=request_user).values_list('workspace_id', flat=True)
            obj = workspace.objects.filter(filters, id__in=workspace_ids).order_by(order_by)
            
        # Apply pagination using offset and limit
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        # Serialize the data
        serialized_data = workspace_serializer(obj, many=True)
        
        return JsonResponse({
            "data": serialized_data.data,
            "success": True,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },
        }, status=200)

    except Exception as e:
        print("This error occurred in list_workspace --->: ", e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add workspace
@api_view(['POST'])
# @workspace_permission_required
def add_workspace(request):
    try:
        # Check if the user has exceeded their workspace limit
        request_user = request.user
        # print(request.abc,'request.abc')
        
        if not request_user.is_superuser:   
            try:
                # Get the user's workspace limit
                user_obj = user_detail.objects.get(user_id=request_user.id)
                workspace_count_obj = user_obj.workspace_id.count()
                workspace_limit = user_obj.workspace_limitation

                # If the user has exceeded the workspace limit, return an error response
                if workspace_count_obj >= workspace_limit:
                    return JsonResponse({
                        "error": "Workspace limit exceeded. Please upgrade your limit.",
                        "success": False,
                    }, status=409)
                    
            except user_detail.DoesNotExist:
                return JsonResponse({"error": "User details not found.","success": False}, status=404)            

        logo = request.FILES.get("logo")
        avatar_image_path = request.data.get("avatar_image_path")

        # Check if either the logo file or the avatar_image_path is provided
        if not logo and not avatar_image_path:
            return JsonResponse({
                "error": "Please provide either a logo or an avatar image path.",
                "success": False,
            }, status=400)

        # Optionally handle cases where both are provided
        if logo and avatar_image_path:
            return JsonResponse({
                "error": "Please provide only one of logo or avatar image path, not both.",
                "success": False,
            }, status=400)
            
        if avatar_image_path:
            if not avatar_image_path.startswith('avatar/workspace_'):
                return JsonResponse({"error": "Invalid image path.","success": False}, status=400)

        #  set dynamic avatar image
        logo = dynamic_avatar_image_process(logo, avatar_image_path)
        if not logo:
            return JsonResponse({"error": "logo processing failed so give me correct image.","success": False}, status=400)

        data = request.data.copy()
        data["created_by"] = request_user.id 
        data["logo"] = logo


        serialized_data = workspace_serializer(data=data)

        if serialized_data.is_valid():
            try:
                # serialized_data.save()
                workspace_obj = serialized_data.save()

                if not request.user.is_superuser:
                    user_obj = user_detail.objects.get(user_id=request_user.id)
                    user_obj.workspace_id.add(workspace_obj)
                    user_obj.save()


                return JsonResponse({
                    "message": "Data added successfully.",
                    "data": serialized_data.data,
                    "success": True,
                }, status=200)
            except:
                return JsonResponse({
                    "error": "workspace already exists. Please use a unique name.",
                    "success": False,
                }, status=400)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is add_workspace --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    

# update workspace
@api_view(['PATCH'])
@workspace_permission_required
def update_workspace(request, slug_id):
    try:

        try:
            obj = workspace.objects.get(slug_id=slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found.",
                "success": False,
            }, status=404)   
        
        
        logo = request.FILES.get("logo")
        avatar_image_path = request.data.get("avatar_image_path")


        if logo and avatar_image_path:
            return JsonResponse({
                "error": "Please provide only one of logo or avatar image path, not both.",
                "success": False,
            }, status=400)

        if avatar_image_path:
            if not avatar_image_path.startswith('avatar/workspace_'):
                return JsonResponse({"error": "Invalid image path.","success": False}, status=400)

        logo = logo or obj.logo
        avatar_image_path = avatar_image_path or obj.logo


        #  set dynamic avatar image
        logo = dynamic_avatar_image_process(logo, avatar_image_path)
        
        if not logo:
            return JsonResponse({"error": "logo processing failed so give me correct image.","success": False}, status=400)

        # Remove 'created_by' from the update request data as it should not be updated
        data = request.data.copy()
        data['created_by'] = obj.created_by.id
        data["logo"] = logo
        
        serialized_data = workspace_serializer(instance=obj, data=data, partial=True)        
        
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
        print("This error is update_workspace --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# delete workspace
@api_view(['DELETE'])
@workspace_permission_required
def delete_workspace(request, slug_id):
    try:
        try:
            obj = workspace.objects.get(slug_id=slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace detail not found.",
                "success": False,
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_workspace --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


