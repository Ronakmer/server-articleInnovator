
from django.shortcuts import render,redirect

# Create your views here.


def add_motivation_page(request):
    try:
        return render(request,'frontendApp/motivation/add_motivation.html')
    except Exception as e:
        print("This error is add_motivation_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_motivation_page(request):
    try:
        return render(request,'frontendApp/motivation/list_motivation.html')
    except Exception as e:
        print("This error is list_motivation_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_motivation_page(request, slug_id):
    try:
        return render(request,'frontendApp/motivation/add_motivation.html')
    except Exception as e:
        print("This error is update_motivation_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

