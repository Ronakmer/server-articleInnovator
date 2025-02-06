
from django.shortcuts import render,redirect

# Create your views here.


def add_image_template_category_page(request):
    try:
        return render(request,'frontendApp/image_template_category/add_image_template_category.html')
    except Exception as e:
        print("This error is add_image_template_category_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_image_template_category_page(request):
    try:
        return render(request,'frontendApp/image_template_category/list_image_template_category.html')
    except Exception as e:
        print("This error is list_image_template_category_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_image_template_category_page(request, slug_id):
    try:
        return render(request,'frontendApp/image_template_category/add_image_template_category.html')
    except Exception as e:
        print("This error is update_image_template_category_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

