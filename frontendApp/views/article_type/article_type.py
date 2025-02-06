
from django.shortcuts import render,redirect

# Create your views here.


def add_article_type_page(request):
    try:
        return render(request,'frontendApp/article_type/add_article_type.html')
    except Exception as e:
        print("This error is add_article_type_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_article_type_page(request):
    try:
        return render(request,'frontendApp/article_type/list_article_type.html')
    except Exception as e:
        print("This error is list_article_type_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


def update_article_type_page(request, slug_id):
    try:
        return render(request,'frontendApp/article_type/add_article_type.html')
    except Exception as e:
        print("This error is update_article_type_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

