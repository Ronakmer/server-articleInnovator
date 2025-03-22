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


@api_view(['POST'])
def admin_login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status=400)

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)    
            # request.session['username'] = email
            request_user = request.user

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)  # This creates a new refresh token on first login
            access_token = str(refresh.access_token)  # Access token from the refresh token
            

            if not user.is_superuser:
                try:
                    user_obj = User.objects.get(email = email)
                    user_detail_obj = user_detail.objects.get(user_id = user_obj)
                    
                    workspaces_obj = user_detail_obj.workspace_id.all()

                    if not workspaces_obj.exists():
                        return JsonResponse({
                            "message": "you not have any workspace so plz.", 
                            # "workspaces_status": False,
                            "access_token": access_token,
                            "refresh_token": str(refresh),
                            "success": True,
                        }, status=200)  # Redirect to the boarding screen

                except Exception as e:
                    return JsonResponse({"error": "user detail not match."}, status=500)


            return JsonResponse({
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": str(refresh),
                # "workspaces_status": True,
                "email":email,
                "success": True,
            }, status=200)

        else:
            return JsonResponse({"error": "Email and Password do not match.","success": False}, status=401)
    except Exception as e:
        print("This error is admin_login --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



