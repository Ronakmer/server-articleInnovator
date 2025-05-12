from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User,auth
import random, math
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from apiApp.models import user_detail, workspace, permission, role_has_permissions
from apiApp.serializers import workspace_serializer

# Create your views here.



#  get request user permissions 
def get_user_permissions(user):
    
    if user.is_superuser:
        return list(permission.objects.values_list('name', flat=True))
    
    try:
        user_detail_obj = user_detail.objects.get(user_id=user)
        role_permissions = role_has_permissions.objects.filter(role_id=user_detail_obj.role_id)
        return list(role_permissions.values_list('permission_id__name', flat=True))
    except user_detail.DoesNotExist:
        return []

        
        
        
@api_view(['GET'])
def fetch_user_permissions(request):
    try:
        request_user = request.user
        permissions_data = get_user_permissions(request_user)
        print(permissions_data, 'permissions_data')
        print(type(permissions_data), 'permissions_data')

        return JsonResponse({
            "message": "Permissions fetched successfully",
            "permissions_data": permissions_data,
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is fetch_user_permissions --->: ", e)
        return JsonResponse({"error": "Internal Server error."}, status=500)
