from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_detail_serializer
from apiApp.models import user_detail, role, workspace
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from django.db.models import Q
from apiApp.views.base.dynamic_avatar_image_process.dynamic_avatar_image_process import dynamic_avatar_image_process
from apiApp.views.base.process_pagination.process_pagination import process_pagination


@api_view(['GET'])
@workspace_permission_required
def list_user_detail(request):
    try:
        request_user = request.user

        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        workspace_slug_id = request.GET.get('workspace_slug_id', None)

        # Initialize filters
        filters = Q()
        if slug_id:
            filters &= Q(slug_id=slug_id)

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if search:
            filters &= Q(name__icontains=search) 

        # Filter by role if provided
        try:
            role_obj = role.objects.get(name='user')
        except role.DoesNotExist:
            return JsonResponse({
                "error": f"role data does not exist.",
                "success": False,
            }, status=404)
            
        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id=workspace_obj.id)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found",
                    "success": False,
                }, status=404)


        # Filter user details
        try:
            if request_user.is_superuser:
                obj = user_detail.objects.filter(filters, role_id=role_obj).order_by(order_by)
            if request.is_admin:
                obj = user_detail.objects.filter(filters, role_id=role_obj).order_by(order_by)
        
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": f"user data does not exist.",
                "success": False,
            }, status=404)

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        # Serialize the data
        serialized_data = user_detail_serializer(obj, many=True)

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
        print("This error is list_user_detail --->: ", e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)


# add user detail
@api_view(['POST'])
@workspace_permission_required
def add_user_detail(request):
    try:
        request_user = request.user 

        full_name=request.POST.get('full_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        profile_image=request.FILES.get('profile_image')
        logo = profile_image
        avatar_image_path = request.data.get("avatar_image_path")

        role_id=role.objects.get(name='user')                

        workspace_slugs_str = request.POST.get('workspace_slug_id')
        if workspace_slugs_str:
            workspace_slugs = workspace_slugs_str.split(",") 
            print(workspace_slugs,'workspace_slugs')  
        
        if User.objects.filter(username=email).exists():
            return JsonResponse({
                "error": "User with this email already exists.",
                "success": False,
            }, status=409)
    
    
        # Check if either the profile_image file or the avatar_image_path is provided
        if not profile_image and not avatar_image_path:
            return JsonResponse({
                "error": "Please provide either a profile image or an avatar image path.",
                "success": False,
            }, status=400)

        # Optionally handle cases where both are provided
        if profile_image and avatar_image_path:
            return JsonResponse({
                "error": "Please provide only one of profile image or avatar image path, not both.",
                "success": False,
            }, status=400)
            
        if avatar_image_path:
            if not avatar_image_path.startswith('avatar/profile_'):
                return JsonResponse({"error": "Invalid image path.","success": False}, status=400)
        
        #  set dynamic avatar image
        profile_image = dynamic_avatar_image_process(profile_image, avatar_image_path)
        if not profile_image:
            return JsonResponse({"error": "profile image processing failed so give me correct image.","success": False}, status=400)

        
        user_id_obj = User()
        user_id_obj.username = email
        user_id_obj.email = email
        user_id_obj.password = make_password(password)
        user_id_obj.save()
        
        user_obj = user_detail()
        user_obj.user_id = user_id_obj
        user_obj.role_id = role_id
        
        user_obj.full_name = full_name
        user_obj.profile_image = profile_image
        user_obj.created_by = request_user
        user_obj.save()
        
        if workspace_slugs:
            valid_workspaces = workspace.objects.filter(slug_id__in=workspace_slugs)
            user_obj.workspace_id.add(*valid_workspaces)

        serialized_user_data = user_detail_serializer(user_obj).data


        return JsonResponse({
            "message": "Data added successfully.",
            "data": serialized_user_data,
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is add_user_detail --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)
    
    


# update uservdetail
@api_view(['PATCH'])
@workspace_permission_required
def update_user_detail(request, slug_id):
    try:
        
        try:
            user_obj = user_detail.objects.get(slug_id=slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "user detail not found.",
                "success": False,
            }, status=404) 
            
            
        status = request.data.get("status")
        
        if status is not None and status != "":
            user_obj.status = status
            user_obj.save()
            serialized_admin_data = user_detail_serializer(user_obj).data

            return JsonResponse({
                "message": "Status updated successfully.",
                "success": True,
                "data": serialized_admin_data,
            }, status=200)   
        
        full_name=request.POST.get('full_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role_id=role.objects.get(name='user')                
        workspace_slugs_str = request.POST.get('workspace_slug_id')
        profile_image=request.FILES.get('profile_image')
        logo = profile_image
        avatar_image_path = request.data.get("avatar_image_path")
                     
        if not user_obj.user_id.email == email:
            if User.objects.filter(username=email).exists():
                return JsonResponse({
                    "error": "User with this email already exists.",
                    "success": False,
                }, status=409)
        

        # Optionally handle cases where both are provided
        if logo and avatar_image_path:
            return JsonResponse({
                "error": "Please provide only one of logo or avatar image path, not both.",
                "success": False,
            }, status=400)
            
        if avatar_image_path:
            if not avatar_image_path.startswith('avatar/profile_'):
                return JsonResponse({"error": "Invalid image path.","success": False}, status=400)
        
        logo = logo or user_obj.profile_image
        avatar_image_path = avatar_image_path or user_obj.profile_image


        #  set dynamic avatar image
        logo = dynamic_avatar_image_process(logo, avatar_image_path)
        if not logo:
            return JsonResponse({"error": "logo processing failed so give me correct image.","success": False}, status=400)

    

        user_obj.user_id.username = email
        user_obj.user_id.email = email
        
        if password:
            user_obj.user_id.password = make_password(password)
        user_obj.full_name = full_name
        if logo:
            user_obj.profile_image = logo
        
        user_obj.user_id.save()
        user_obj.save()
        
        if workspace_slugs_str:
            workspace_slugs = workspace_slugs_str.split(",") 
            valid_workspaces = workspace.objects.filter(slug_id__in=workspace_slugs)
            user_obj.workspace_id.set(valid_workspaces)

        serialized_user_data = user_detail_serializer(user_obj).data

        return JsonResponse({
            "message": "Data updated successfully.",
            "data": serialized_user_data,
            "success": True,
        }, status=200)
        
    except Exception as e:
        print("This error is update_user_detail --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)




# delete user detail
@api_view(['DELETE'])
@workspace_permission_required
def delete_user_detail(request, slug_id):
    try:
        try:
            obj = user_detail.objects.get(slug_id=slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "user detail not found.",
                "success": False,
            }, status=404) 
        
        workspace_slug_id = request.GET.get('workspace_slug_id')

        if not (workspace_slug_id):
            return JsonResponse({"error": "workspace slug required fields.","success": False}, status=400)

        # if (obj.workspace_id.slug_id != workspace_slug_id):
        #     return JsonResponse({
        #         "error": "You Don't have permission."
        #     }, status=404)
        if not obj.workspace_id.filter(slug_id=workspace_slug_id).exists():
            return JsonResponse({
                "error": "You don't have permission.",
                "success": False,
            }, status=403)
            
        
        if obj.user_id:
            obj.user_id.delete()       
        obj.delete()

        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_user_detail --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



