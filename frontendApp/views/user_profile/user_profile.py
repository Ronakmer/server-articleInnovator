
from django.shortcuts import render,redirect

# Create your views here.


def user_profile_page(request):
    try:
        return render(request,'frontendApp/user_profile/user_profile.html')
    except Exception as e:
        print("This error is user_profileail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})
