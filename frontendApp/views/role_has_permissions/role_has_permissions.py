
from django.shortcuts import render,redirect

# Create your views here.

def list_role_has_permissions_page(request):
    try:
        return render(request,'frontendApp/role_has_permissions/role_has_permissions.html')
    except Exception as e:
        print("This error is list_role_has_permissions_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

