
from django.shortcuts import render,redirect

# Create your views here.


def add_prompt_page(request):
    try:
        return render(request,'frontendApp/prompt/add_prompt.html')
    except Exception as e:
        print("This error is add_prompt_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_prompt_page(request):
    try:
        return render(request,'frontendApp/prompt/list_prompt.html')
    except Exception as e:
        print("This error is list_prompt_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_prompt_page(request, slug_id):
    try:
        return render(request,'frontendApp/prompt/add_prompt.html')
    except Exception as e:
        print("This error is update_prompt_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

