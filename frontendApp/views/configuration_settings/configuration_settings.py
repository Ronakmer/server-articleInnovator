
from django.shortcuts import render,redirect

# Create your views here.


def add_configuration_settings_page(request):
    try:
        return render(request,'frontendApp/configuration_settings/add_configuration_settings.html')
    except Exception as e:
        print("This error is add_configuration_settings_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_configuration_settings_page(request):
    try:
        return render(request,'frontendApp/configuration_settings/list_configuration_settings.html')
    except Exception as e:
        print("This error is list_configuration_settings_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


def update_configuration_settings_page(request, slug_id):
    try:
        return render(request,'frontendApp/configuration_settings/add_configuration_settings.html')
    except Exception as e:
        print("This error is update_configuration_settings_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

