

from django.shortcuts import render,redirect

# Create your views here.


def add_ai_configuration_page(request):
    try:
        return render(request,'frontendApp/ai_configuration/add_ai_configuration.html')
    except Exception as e:
        print("This error is add_ai_configuration_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_ai_configuration_page(request):
    try:
        return render(request,'frontendApp/ai_configuration/list_ai_configuration.html')
    except Exception as e:
        print("This error is list_ai_configuration_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


def update_ai_configuration_page(request, slug_id):
    try:
        return render(request,'frontendApp/ai_configuration/add_ai_configuration.html')
    except Exception as e:
        print("This error is update_ai_configuration_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

