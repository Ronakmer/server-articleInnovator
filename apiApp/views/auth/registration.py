from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
import random, math
from django.conf import settings
from django.http import JsonResponse
import json
from apiApp.models import invitation_code_detail, role, user_detail
from rest_framework.decorators import api_view
from django.core.cache import cache
from datetime import datetime
from apiApp.serializers import user_detail_serializer
from django.views.decorators.csrf import csrf_exempt
from apiApp.views.base.generate_otp.generate_otp import generate_otp



#  check invitation code
@api_view(['POST'])
def check_invitation_code(request):
    try:
        invitation_code = request.data.get('invitation_code')

        try:
            invitation_code_details_obj = invitation_code_detail.objects.get(invitation_code=invitation_code)
        except invitation_code_detail.DoesNotExist:
            return JsonResponse({
                "error": "invitation code detail not found.",
                "success": False,
            }, status=404)   

        used = invitation_code_details_obj.used
        print(used,'used')
        if used == False:
            message = 'Registration Now'
        return JsonResponse({
            "success": True,
            "used":used,
            "message":message
        }, status=200)

    except Exception as e:
        print("This error is check_invitation_code --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)




#  registration
@api_view(['POST'])
def admin_registration(request):
    try:
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        password = request.data.get('password')
        invitation_code = request.data.get('invitation_code')

        if not (full_name and email and password):
            return JsonResponse({"error": "All fields (full_name, email, password) are required."}, status=400)
  
        create_otp = generate_otp()
        
        try:
            invitation_code_details_obj = invitation_code_detail.objects.get(invitation_code=invitation_code)
        except invitation_code_detail.DoesNotExist:
            return JsonResponse({
                "error": "invitation code detail not found.",
            }, status=404)   

        used = invitation_code_details_obj.used
        
        if used == True:
            return JsonResponse({"message": "The invitation code has already been used."}, status=409)

        try:
            # Send OTP to user via email
            send_mail(
                subject='OTP Request',
                message=f'Your OTP is {create_otp}',
                # from_email=settings.DEFAULT_FROM_EMAIL,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
        except Exception as e:
            return JsonResponse({"error": "Failed to send OTP."}, status=500)

        
        # Validate and store data in cache
        cache.set(f"admin_data_{email}", {
            "full_name": full_name,
            "email": email,
            "password": password,
            "invitation_code": invitation_code,
            "otp": create_otp,
        }, timeout=300) 
        print('done')

        return JsonResponse({"message": "OTP sent successfully."}, status=200)

    except Exception as e:
        print("This error is admin_registration --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# save registration data
@api_view(['POST'])
def registration_check_otp(request):
    try:
        email = request.data.get('email')
        user_otp = request.data.get('otp')
        admin_data = cache.get(f"admin_data_{email}")

        if not (email and user_otp):
            return JsonResponse({"error": "All fields (email, otp) are required."}, status=400)
        
        if not admin_data:
            return JsonResponse({"error": "Data expired or not found. Restart the registration process."}, status=410)

        if admin_data['otp'] != user_otp:
            return JsonResponse({"error": "Invalid OTP. Please try again."}, status=401)
        if admin_data['email'] != email:
            return JsonResponse({"error": "Invalid email. Please try again."}, status=401)

        # Registration logic (e.g., saving data to the database)
        full_name = admin_data["full_name"]
        email = admin_data["email"]
        password = admin_data["password"]
        invitation_code = admin_data["invitation_code"]

        current_date = datetime.now()

        try:
            invitation_code_details_obj = invitation_code_detail.objects.get(invitation_code=invitation_code)
        except invitation_code_detail.DoesNotExist:
            return JsonResponse({
                "error": "invitation code detail not found.",
            }, status=404)   

        used = invitation_code_details_obj.used
        
        if used == True:
            return JsonResponse({"message": "The invitation code has already been used."}, status=409)

        # Create new user and save details
        user_id_obj = User()
        user_id_obj.username = email
        user_id_obj.email = email
        user_id_obj.password = make_password(password)
        user_id_obj.save()

        # Save admin details
        invitation_code_details_obj = invitation_code_detail.objects.get(invitation_code=invitation_code)
        article_limitation = invitation_code_details_obj.article_limitation
        domain_limitation = invitation_code_details_obj.domain_limitation
        workspace_limitation = invitation_code_details_obj.workspace_limitation
        
        role_id_obj = role.objects.get(name='admin')

        admin_obj = user_detail()
        admin_obj.user_id = user_id_obj
        admin_obj.role_id = role_id_obj
        admin_obj.article_limitation = article_limitation
        admin_obj.domain_limitation = domain_limitation
        admin_obj.workspace_limitation = workspace_limitation
        admin_obj.full_name = full_name
        admin_obj.save()


        # Mark the invitation code as used
        invitation_code_details_obj.used = True
        invitation_code_details_obj.used_date = current_date
        invitation_code_details_obj.email = user_id_obj
        invitation_code_details_obj.save()

        serialized_data = user_detail_serializer(admin_obj).data

        return JsonResponse({
            "message": "user registration successfully.",
            "user_detail":serialized_data
        }, status=200)


    except Exception as e:
        print("This error is registration_check_otp --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)
    