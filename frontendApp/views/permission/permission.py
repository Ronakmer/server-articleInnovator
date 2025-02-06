
from django.shortcuts import render,redirect

# Create your views here.


def add_permission_page(request):
    try:
        return render(request,'frontendApp/permission/add_permission.html')
    except Exception as e:
        print("This error is add_permission_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_permission_page(request):
    try:
        return render(request,'frontendApp/permission/list_permission.html')
    except Exception as e:
        print("This error is list_permission_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_permission_page(request, slug_id):
    try:
        return render(request,'frontendApp/permission/add_permission.html')
    except Exception as e:
        print("This error is update_permission_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

