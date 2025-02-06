
from django.shortcuts import render,redirect

# Create your views here.


def add_image_tag_page(request):
    try:
        return render(request,'frontendApp/image_tag/add_image_tag.html')
    except Exception as e:
        print("This error is add_image_tag_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_image_tag_page(request):
    try:
        return render(request,'frontendApp/image_tag/list_image_tag.html')
    except Exception as e:
        print("This error is list_image_tag_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_image_tag_page(request, slug_id):
    try:
        return render(request,'frontendApp/image_tag/add_image_tag.html')
    except Exception as e:
        print("This error is update_image_tag_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

