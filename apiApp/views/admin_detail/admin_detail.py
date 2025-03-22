from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_detail_serializer
from apiApp.models import user_detail, role, workspace
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from apiApp.views.base.dynamic_avatar_image_process.dynamic_avatar_image_process import dynamic_avatar_image_process
from apiApp.views.base.process_pagination.process_pagination import process_pagination



# show admin detail
@api_view(['GET'])
def list_admin_detail(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        slug_id = request.GET.get('slug_id', None)
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)

        # Filter by role if provided
        try:
            role_obj = role.objects.get(name='admin')
        except role.DoesNotExist:
            return JsonResponse({
                "error": f"role data does not exist.",
                "success": False,
            }, status=404)

        # Filter user details
        try:
            obj = user_detail.objects.filter(filters, role_id=role_obj).order_by(order_by)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": f"admin data does not exist.",
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
        print("This error is list_admin_detail --->: ", e)
        return JsonResponse({"error": "Internal Server error.","success": False,}, status=500)



# add admin detail
@api_view(['POST'])
def add_admin_detail(request):
    try:
        request_user = request.user 

        full_name=request.POST.get('full_name')
        profile_image=request.FILES.get('profile_image')
        password = request.POST.get('password')
        email = request.POST.get('email')
        article_limitation = request.POST.get('article_limitation')
        domain_limitation = request.POST.get('domain_limitation')
        workspace_limitation = request.POST.get('workspace_limitation')
                    
        avatar_image_path = request.data.get("avatar_image_path")

        workspace_slugs_str = request.POST.get('workspace_slug_id')
        if workspace_slugs_str:
            workspace_slugs = workspace_slugs_str.split(",") 
            print(workspace_slugs,'workspace_slugs')  

        try:
            role_id=role.objects.get(name='admin')                            
        except role.DoesNotExist:
            return JsonResponse({"error": "role detail not found.","success": False}, status=404)
        
        if User.objects.filter(username=email).exists():
            return JsonResponse({
                "error": "User with this email already exists."
            }, status=400)
            
        # Check if either the profile_image file or the avatar_image_path is provided
        if not profile_image and not avatar_image_path:
            return JsonResponse({
                "error": "Please provide either a profile image or an avatar image path.",
                "success": False
            }, status=400)

        # Optionally handle cases where both are provided
        if profile_image and avatar_image_path:
            return JsonResponse({
                "error": "Please provide only one of profile image or avatar image path, not both.",
                "success": False
            }, status=400)
            
        if avatar_image_path:
            if not avatar_image_path.startswith('avatar/profile_'):
                return JsonResponse({"error": "Invalid image path."}, status=400)
        
        #  set dynamic avatar image
        profile_image = dynamic_avatar_image_process(profile_image, avatar_image_path)
        if not profile_image:
            return JsonResponse({"error": "profile image processing failed so give me correct image.","success": False}, status=400)


        user_id_obj = User()
        user_id_obj.username = email
        user_id_obj.email = email
        user_id_obj.password = make_password(password)
        user_id_obj.save()
        
        admin_obj = user_detail()
        admin_obj.user_id = user_id_obj
        admin_obj.role_id = role_id
        admin_obj.article_limitation = article_limitation
        admin_obj.domain_limitation = domain_limitation
        admin_obj.workspace_limitation = workspace_limitation
        admin_obj.full_name = full_name
        admin_obj.profile_image = profile_image
        admin_obj.created_by = request_user
        admin_obj.save()
        if workspace_slugs:
            valid_workspaces = workspace.objects.filter(slug_id__in=workspace_slugs)
            admin_obj.workspace_id.add(*valid_workspaces)

    
        serialized_admin_data = user_detail_serializer(admin_obj).data

        return JsonResponse({
            "message": "Data added successfully.",
            "success": True,
            "data": serialized_admin_data,
        }, status=200)

    except Exception as e:
        print("This error is add_admin_detail --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)
    


# update admin detail
@api_view(['PATCH'])
def update_admin_detail(request, slug_id):
    try:
        full_name=request.POST.get('full_name')
        profile_image=request.FILES.get('profile_image')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role_id=role.objects.get(name='admin')                
        article_limitation = request.POST.get('article_limitation')
        domain_limitation = request.POST.get('domain_limitation')
        workspace_limitation = request.POST.get('workspace_limitation')
        
        if User.objects.filter(username=email).exists():
            return JsonResponse({
                "error": "User with this email already exists.",
                "success": False,
            }, status=400)


        try:
            admin_obj = user_detail.objects.get(slug_id=slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "admin detail not found.",
                "success": False,
            }, status=404) 

        admin_obj.article_limitation = article_limitation
        admin_obj.domain_limitation = domain_limitation
        admin_obj.workspace_limitation = workspace_limitation

        if password:
            admin_obj.user_id.password = make_password(password)
        admin_obj.full_name = full_name
        if profile_image:
            admin_obj.profile_image = profile_image
        
        admin_obj.user_id.save()
        admin_obj.save()
        
        serialized_admin_data = user_detail_serializer(admin_obj).data

        return JsonResponse({
            "message": "Data updated successfully.",
            "success": True,
            "data": serialized_admin_data,
        }, status=200)
        
    except Exception as e:
        print("This error is update_admin_detail --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# delete admin detail
@api_view(['DELETE'])
def delete_admin_detail(request, slug_id):
    try:
        try:
            obj = user_detail.objects.get(slug_id=slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "admin detail not found.",
                "success": False,
            }, status=404) 

        if obj.user_id:
            obj.user_id.delete()       

        obj.delete()

        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_admin_detail --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



