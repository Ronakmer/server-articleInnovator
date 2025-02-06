from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_detail_serializer
from apiApp.models import user_detail, role, workspace
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q


# show user profile
@api_view(['GET'])
def list_user_profile(request):
    try:
        request_user = request.user
        try:
            user_obj = user_detail.objects.get(user_id=request_user.id) 
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": f"user data does not exist."
            }, status=400)

        if user_obj.role_id.name == 'admin':
           
            profile_obj = user_obj 
            print(profile_obj,'profile_obj')
           
            user_data = {
                "user_id": user_obj.user_id.email,
                "role_id": user_obj.role_id.name if user_obj.role_id else None,
                "workspace_id": [{
                    "name": workspace.name,
                    "slug_id": workspace.slug_id
                } for workspace in profile_obj.workspace_id.all()],
                # "email": request_user.email,
                "full_name": profile_obj.full_name,
                "profile_image": profile_obj.profile_image.url if profile_obj.profile_image else None,
                "article_limitation": profile_obj.article_limitation,
                "domain_limitation": profile_obj.domain_limitation,
                "workspace_limitation": profile_obj.workspace_limitation,
                "slug_id": profile_obj.slug_id,
            }

        else:
            user_data = {
                "user_id": user_obj.user_id.email,
                # "email": request_user.email,
                "full_name": user_obj.full_name,
                "profile_image": user_obj.profile_image.url if user_obj.profile_image else None,
            }

        return JsonResponse({
            "redirect": "",
            "user_data": user_data,
        }, status=200)

    except Exception as e:
        print("This error is list_user_profile --->: ", e)
        return JsonResponse({"error": "Internal Server error."}, status=500)
