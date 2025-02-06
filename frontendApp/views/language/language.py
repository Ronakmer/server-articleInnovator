
from django.shortcuts import render,redirect

# Create your views here.


def add_language_page(request):
    try:
        return render(request,'frontendApp/language/add_language.html')
    except Exception as e:
        print("This error is add_language_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_language_page(request):
    try:
        return render(request,'frontendApp/language/list_language.html')
    except Exception as e:
        print("This error is list_language_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_language_page(request, slug_id):
    try:
        return render(request,'frontendApp/language/add_language.html')
    except Exception as e:
        print("This error is update_language_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

