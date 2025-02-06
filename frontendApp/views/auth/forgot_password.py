
from django.shortcuts import render,redirect

# Create your views here.


def email_page(request):
    try:
        return render(request,'frontendApp/auth/forgot.html')
    except Exception as e:
        print("This error is email_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def otp_page(request):
    try:
        return render(request,'frontendApp/auth/enter_otp.html')
    except Exception as e:
        print("This error is otp_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def new_password_page(request):
    try:
        return render(request,'frontendApp/auth/new_password.html')
    except Exception as e:
        print("This error is new_password_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})




