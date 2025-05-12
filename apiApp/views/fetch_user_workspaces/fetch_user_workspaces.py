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



# #  get request user permissions 
# def get_user_permissions(user):
    
#     if user.is_superuser:
#         return list(permission.objects.values_list('name', flat=True))
    
#     try:
#         user_detail_obj = user_detail.objects.get(user_id=user)
#         role_permissions = role_has_permissions.objects.filter(role_id=user_detail_obj.role_id)
#         return list(role_permissions.values_list('permission_id__name', flat=True))
#     except user_detail.DoesNotExist:
#         return []

        
        
        
        

# @api_view(['POST'])
# def fetch_user_workspaces(request):
#     try:
#         email = request.data.get('email')
#         workspaces_data = []

#         request_user = request.user
        
#         permissions_data = get_user_permissions(request_user)
#         print(permissions_data,'permissions_data')
#         print(type(permissions_data),'permissions_data')

#         if request_user.is_superuser:
#             workspaces_obj = workspace.objects.all()
#         else:
#             try:
#                 user_obj = User.objects.get(email = email)
#                 user_detail_obj = user_detail.objects.get(user_id = user_obj)
#                 print(user_detail_obj,'0.289')
                
#                 workspaces_obj = user_detail_obj.workspace_id.all()
#                 print(workspaces_obj,'012')

#                 if not workspaces_obj.exists():
#                     return JsonResponse({
#                         "message": "you not have any workspace so plz.", 
#                         "workspaces_status": False,
#                         "permissions_data": permissions_data,
#                         "success": True,
#                     }, status=200)  # Redirect to the boarding screen

#                 if not workspaces_obj.filter(user_details__user_id=request_user).exists():
#                     return JsonResponse({
#                         "message": "You do not have permission to access these workspaces.",
#                         "workspaces_status": False,
#                         "success": False,
#                     }, status=403)

#             except Exception as e:
#                 return JsonResponse({"error": "user detail not match."}, status=500)

#         workspaces_data = workspace_serializer(workspaces_obj, many=True).data

#         return JsonResponse({
#             "message": "Login successful",
#             "workspaces_data":workspaces_data,
#             "workspaces_status": True,
#             "permissions_data": permissions_data,
#             "success": True,
            
#         }, status=200)

#     except Exception as e:
#         print("This error is fetch_user_workspaces --->: ",e)
#         return JsonResponse({"error": "Internal Server error."}, status=500)









        
        
        

@api_view(['GET'])
def fetch_user_workspaces(request):
    try:
        # email = request.data.get('email')
        workspaces_data = []

        request_user = request.user
        
        if request_user.is_superuser:
            workspaces_obj = workspace.objects.all()
        else:
            try:
                # user_obj = User.objects.get(email = email)
                # user_detail_obj = user_detail.objects.get(user_id = user_obj)
                user_detail_obj = user_detail.objects.get(user_id=request_user)
                print(user_detail_obj,'0.289')
                
                workspaces_obj = user_detail_obj.workspace_id.all()
                print(workspaces_obj,'012')

                if not workspaces_obj.exists():
                    return JsonResponse({
                        "message": "you not have any workspace so plz.", 
                        "workspaces_status": False,
                        # "permissions_data": permissions_data,
                        "success": True,
                    }, status=200)  # Redirect to the boarding screen

                if not workspaces_obj.filter(user_details__user_id=request_user).exists():
                    return JsonResponse({
                        "message": "You do not have permission to access these workspaces.",
                        "workspaces_status": False,
                        "success": False,
                    }, status=403)

            except Exception as e:
                return JsonResponse({"error": "user detail not match."}, status=500)

        workspaces_data = workspace_serializer(workspaces_obj, many=True).data
        print(workspaces_data,'workspaces_datax')
        return JsonResponse({
            "message": "Login successful",
            "workspaces_data":workspaces_data,
            "workspaces_status": True,
            # "permissions_data": permissions_data,
            "success": True,
            
        }, status=200)

    except Exception as e:
        print("This error is fetch_user_workspaces --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)

