
from django.shortcuts import render,redirect

# Create your views here.


def add_image_template_page(request):
    try:
        return render(request,'frontendApp/image_template/add_image_template.html')
    except Exception as e:
        print("This error is add_image_template_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_image_template_page(request):
    try:
        return render(request,'frontendApp/image_template/list_image_template.html')
    except Exception as e:
        print("This error is list_image_template_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_image_template_page(request, slug_id):
    try:
        return render(request,'frontendApp/image_template/add_image_template.html')
    except Exception as e:
        print("This error is update_image_template_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

