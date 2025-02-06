
from django.shortcuts import render,redirect

# Create your views here.


def add_article_type_field_page(request):
    try:
        return render(request,'frontendApp/article_type_field/add_article_type_field.html')
    except Exception as e:
        print("This error is add_article_type_field_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_article_type_field_page(request):
    try:
        return render(request,'frontendApp/article_type_field/list_article_type_field.html')
    except Exception as e:
        print("This error is list_article_type_field_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


def update_article_type_field_page(request, slug_id):
    try:
        return render(request,'frontendApp/article_type_field/add_article_type_field.html')
    except Exception as e:
        print("This error is update_article_type_field_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

