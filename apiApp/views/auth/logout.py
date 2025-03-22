
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,auth
from django.http import  JsonResponse
import json
from rest_framework.decorators import api_view


@api_view(['POST'])
def admin_logout(request):
    try:
        logout(request)
        return JsonResponse({"message": "Logout successful","success": True}, status=200)
    except Exception as e:
        print("This error is admin_logout --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)


