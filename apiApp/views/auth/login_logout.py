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
from apiApp.models import user_detail, workspace
from apiApp.serializers import workspace_serializer

# Create your views here.


@api_view(['POST'])
def admin_login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        print(email,'000')
        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status=400)

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            # request.session['username'] = email
            request_user = request.user
            workspaces_data = []

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)  # This creates a new refresh token on first login
            access_token = str(refresh.access_token)  # Access token from the refresh token
            
            if user.is_superuser:
                workspaces_obj = workspace.objects.all()
                workspaces_data = workspace_serializer(workspaces_obj, many=True).data

            else:
            # if not request_user.is_superuser:
                try:
                    user_obj = User.objects.get(email = email)
                    user_detail_obj = user_detail.objects.get(user_id = user_obj)
                    print(user_detail_obj,'0.289')
                    
                    workspaces_obj = user_detail_obj.workspace_id.all()
                    print(workspaces_obj,'012')

                    if not workspaces_obj.exists():
                        return JsonResponse({
                            "message": "you not have any workspace so plz.", 
                            "workspaces_status": False,
                            "access_token": access_token,
                            "refresh_token": str(refresh),
                        }, status=200)  # Redirect to the boarding screen

                    workspaces_data = workspace_serializer(workspaces_obj, many=True).data

                except Exception as e:
                    return JsonResponse({"error": "user detail not match."}, status=500)


            return JsonResponse({
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": str(refresh),
                "workspaces_data":workspaces_data,
                "redirect": "list_dashboard",
                "workspaces_status": True,
            }, status=200)

            # return JsonResponse({"redirect": "list_dashboard"}, status=200)
        else:
            return JsonResponse({"error": "Email and Password do not match."}, status=401)
    except Exception as e:
        print("This error is admin_login --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)





@csrf_exempt
def admin_logout(request):
    try:
        if request.method == "POST":
            logout(request)
            return JsonResponse({"redirect": "login"}, status=200)
        else:
            return JsonResponse({"error": "Method not allowed."}, status=405)
    except Exception as e:
        print("This error is admin_logout --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)


