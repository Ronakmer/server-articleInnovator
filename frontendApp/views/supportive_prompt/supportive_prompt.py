
from django.shortcuts import render,redirect

# Create your views here.


def add_supportive_prompt_page(request):
    try:
        return render(request,'frontendApp/supportive_prompt/add_supportive_prompt.html')
    except Exception as e:
        print("This error is add_supportive_prompt_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_supportive_prompt_page(request):
    try:
        return render(request,'frontendApp/supportive_prompt/list_supportive_prompt.html')
    except Exception as e:
        print("This error is list_supportive_prompt_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_supportive_prompt_page(request, slug_id):
    try:
        return render(request,'frontendApp/supportive_prompt/add_supportive_prompt.html')
    except Exception as e:
        print("This error is update_supportive_prompt_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

