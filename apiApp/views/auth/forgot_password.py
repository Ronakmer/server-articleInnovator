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
from django.core.cache import cache

# Create your views here.


def generate_otp() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


    
@api_view(['POST'])
def send_otp(request):
    try:
        email = request.data.get('email')

        if not email:
            return JsonResponse({"error": "Email is required."}, status=400)

        try:
            user = User.objects.get(email=email)
        except:
            return JsonResponse({"error": "Email does not exist."}, status=404)

        # Generate OTP
        otp = generate_otp()

        # Validate and store data in cache
        cache.set(f"otp_{user.email}", {
            "stored_otp": otp,
            "stored_user_email": user.email,
        }, timeout=900) 
        
        otp_data = cache.get(f"otp_merronak14@gmail.com")
        print(otp_data)

        send_mail(
            subject='OTP Request',
            message=f'Your OTP is {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return JsonResponse({"message": "OTP sent successfully", "user_email": user.email, "redirect": "check_otp"}, status=200)

    except Exception as e:
        print("This error is send_otp --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)





@api_view(['POST'])
def check_otp(request):
    try:
        otp = request.data.get('otp')
        user_email = request.data.get('user_email')

        otp_data = cache.get(f"otp_{user_email}")
        print(otp_data)
        if not otp_data:
            return JsonResponse({"error": "Data expired or not found."}, status=400)

        stored_otp = otp_data["stored_otp"]
        stored_user_email = otp_data["stored_user_email"]
        
        if otp and user_email:
            if stored_otp == otp:
                if stored_user_email == user_email:
                    return JsonResponse({"message": "OTP verified successfully", "id": user_email, "redirect": "set_new_password"}, status=200)
                else:
                    return JsonResponse({"error": "User ID is invalid."}, status=400)
            else:
                return JsonResponse({"error": "OTP is incorrect."}, status=400)
        else:
            return JsonResponse({"error": "All fields are required."}, status=400)

    except Exception as e:
        print("This error is check_otp --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)




@api_view(['POST'])
def set_new_password(request):
    try:
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        user_email = request.data.get('user_email')
        otp = request.data.get('otp')

        otp_data = cache.get(f"otp_{user_email}")
        
        if not otp_data:
            return JsonResponse({"error": "Data expired or not found."}, status=400)

        stored_otp = otp_data["stored_otp"]
        stored_user_email = otp_data["stored_user_email"]

        if user_email != stored_user_email or otp != stored_otp:
            return JsonResponse({"error": "Invalid OTP or email address."}, status=400)

        if new_password and confirm_password and user_email:
            if new_password == confirm_password:
                try:
                    user = User.objects.get(email = user_email)
                    user.set_password(new_password)
                    user.save()
                    return JsonResponse({"message": "Password changed successfully", "redirect": "login"}, status=200)
                except User.DoesNotExist:
                    return JsonResponse({"error": "User does not exist."}, status=400)
            else:
                return JsonResponse({"error": "Passwords do not match."}, status=400)
        else:
            return JsonResponse({"error": "All fields are required."}, status=400)
    except Exception as e:
        print("This error is set_new_password --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



    