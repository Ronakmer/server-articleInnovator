
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_detail_serializer
from apiApp.models import user_detail, role, workspace
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from apiApp.views.base.dynamic_avatar_image_process.dynamic_avatar_image_process import dynamic_avatar_image_process


# show user profile
@api_view(['GET'])
def list_user_profile(request):
    try:
        request_user = request.user
        
        try:
            user_obj = user_detail.objects.get(user_id=request_user.id)
        except user_detail.DoesNotExist:
            return JsonResponse({"error": "User data does not exist.","success": False}, status=400)

        user_data = {
            "full_name": user_obj.full_name,
            "profile_image": user_obj.profile_image.url if user_obj.profile_image else None,
        }
            
        return JsonResponse({
            "user_data": user_data,
            "success": True,
        }, status=200)
        

    except Exception as e:
        print("This error is list_user_profile --->: ", e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)







# add user detail
@api_view(['PATCH'])
def update_user_profile(request):
    try:
        request_user = request.user 

        full_name=request.data.get('full_name')
        password = request.data.get('password')
        profile_image=request.FILES.get('profile_image')
        avatar_image_path = request.data.get("avatar_image_path")

        # Optionally handle cases where both are provided
        if profile_image and avatar_image_path:
            return JsonResponse({
                "error": "Please provide only one of profile image or avatar image path, not both."
            }, status=400)
            
        if avatar_image_path:
            if not avatar_image_path.startswith('avatar/profile_'):
                return JsonResponse({"error": "Invalid image path."}, status=400)
        
        if profile_image or avatar_image_path:
            #  set dynamic avatar image
            profile_image = dynamic_avatar_image_process(profile_image, avatar_image_path)
            if not profile_image:
                return JsonResponse({"error": "profile image processing failed so give me correct image."}, status=400)

        try:
            user_obj = user_detail.objects.get(user_id=request_user)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "user detail not found.",
            }, status=404)      
        
        if full_name:
            user_obj.full_name = full_name
        if password:
            user_obj.user_id.password = make_password(password)
        if profile_image:
            user_obj.profile_image = profile_image
            
        user_obj.user_id.save()
        user_obj.save()
        
        serialized_user_data = user_detail_serializer(user_obj).data
        
        return JsonResponse({
            "message": "Data update successfully.",
            "user_detail": serialized_user_data,
        }, status=200)

    except Exception as e:
        print("This error is update_user_profile --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)
    
    