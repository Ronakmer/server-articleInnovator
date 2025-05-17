
from django.shortcuts import render,redirect

# Create your views here.


def add_integration_page(request):
    try:
        return render(request,'frontendApp/integration/add_integration.html')
    except Exception as e:
        print("This error is add_integration_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_integration_page(request):
    try:
        return render(request,'frontendApp/integration/list_integration.html')
    except Exception as e:
        print("This error is list_integration_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


def update_integration_page(request, slug_id):
    try:
        return render(request,'frontendApp/integration/add_integration.html')
    except Exception as e:
        print("This error is update_integration_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

