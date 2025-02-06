
from django.shortcuts import render,redirect

# Create your views here.


def add_domain_page(request):
    try:
        return render(request,'frontendApp/domain/add_domain.html')
    except Exception as e:
        print("This error is add_domain_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_domain_page(request):
    try:
        return render(request,'frontendApp/domain/list_domain.html')
    except Exception as e:
        print("This error is list_domain_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


def update_domain_page(request, slug_id):
    try:
        return render(request,'frontendApp/domain/add_domain.html')
    except Exception as e:
        print("This error is update_domain_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def detail_domain_page(request, slug_id):
    try:
        return render(request,'frontendApp/domain/detail_domain.html')
    except Exception as e:
        print("This error is detail_domain_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

