
from django.shortcuts import render,redirect

# Create your views here.


def add_user_detail_page(request):
    try:
        return render(request,'frontendApp/user_detail/add_user_detail.html')
    except Exception as e:
        print("This error is add_user_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_user_detail_page(request):
    try:
        return render(request,'frontendApp/user_detail/list_user_detail.html')
    except Exception as e:
        print("This error is list_user_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def update_user_detail_page(request, slug_id):
    try:
        return render(request,'frontendApp/user_detail/add_user_detail.html')
    except Exception as e:
        print("This error is update_user_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

