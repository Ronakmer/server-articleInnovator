
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def login_page(request):
    try:
        return render(request,'frontendApp/auth/login.html')
    except Exception as e:
        print("This error is login_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


# @csrf_exempt
def registration_enter_otp_page(request):
    try:
        return render(request,'frontendApp/auth/registration_enter_otp.html')
    except Exception as e:
        print("This error is registration_enter_otp_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})




# @csrf_exempt
# def admin_logout(request):
#     try:
#         if request.method == "POST":
#             logout(request)
#             return JsonResponse({"redirect": "login"}, status=200)
#         else:
#             return JsonResponse({"error": "Method not allowed."}, status=405)
#     except Exception as e:
#         print("This error is admin_logout --->: ",e)
#         return JsonResponse({"error": "Internal Server error."}, status=500)

