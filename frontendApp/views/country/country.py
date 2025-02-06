
from django.shortcuts import render,redirect

# Create your views here.


def add_country_page(request):
    try:
        return render(request,'frontendApp/country/add_country.html')
    except Exception as e:
        print("This error is add_country_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_country_page(request):
    try:
        return render(request,'frontendApp/country/list_country.html')
    except Exception as e:
        print("This error is list_country_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


def update_country_page(request, slug_id):
    try:
        return render(request,'frontendApp/country/add_country.html')
    except Exception as e:
        print("This error is update_country_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

