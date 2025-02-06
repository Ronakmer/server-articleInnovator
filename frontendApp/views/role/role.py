
from django.shortcuts import render,redirect

# Create your views here.


def add_role_page(request):
    try:
        return render(request,'frontendApp/role/add_role.html')
    except Exception as e:
        print("This error is add_role_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_role_page(request):
    try:
        return render(request,'frontendApp/role/list_role.html')
    except Exception as e:
        print("This error is list_role_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_role_page(request, slug_id):
    try:
        return render(request,'frontendApp/role/add_role.html')
    except Exception as e:
        print("This error is update_role_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

