
from django.shortcuts import render,redirect

# Create your views here.


def add_dynamic_avatar_image_page(request):
    try:
        return render(request,'frontendApp/dynamic_avatar_image/add_dynamic_avatar_image.html')
    except Exception as e:
        print("This error is add_dynamic_avatar_image_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_dynamic_avatar_image_page(request):
    try:
        return render(request,'frontendApp/dynamic_avatar_image/list_dynamic_avatar_image.html')
    except Exception as e:
        print("This error is list_dynamic_avatar_image_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


def update_dynamic_avatar_image_page(request, slug_id):
    try:
        return render(request,'frontendApp/dynamic_avatar_image/add_dynamic_avatar_image.html')
    except Exception as e:
        print("This error is update_dynamic_avatar_image_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

