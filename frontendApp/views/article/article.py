
from django.shortcuts import render,redirect

# Create your views here.


def add_article_page(request):
    try:
        return render(request,'frontendApp/article/add_article/add_article.html')
    except Exception as e:
        print("This error is add_article_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_article_page(request):
    try:
        return render(request,'frontendApp/article/list_article/list_article.html')
    except Exception as e:
        print("This error is list_article_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


def update_article_page(request, slug_id):
    try:
        return render(request,'frontendApp/article/update_article/update_article.html')
    except Exception as e:
        print("This error is update_article_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

