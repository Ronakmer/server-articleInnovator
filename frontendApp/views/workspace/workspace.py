
from django.shortcuts import render,redirect

# Create your views here.


def add_workspace_page(request):
    try:
        return render(request,'frontendApp/workspace/add_workspace.html')
    except Exception as e:
        print("This error is add_workspace_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_workspace_page(request):
    try:
        return render(request,'frontendApp/workspace/list_workspace.html')
    except Exception as e:
        print("This error is list_workspace_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_workspace_page(request, slug_id):
    try:
        return render(request,'frontendApp/workspace/add_workspace.html')
    except Exception as e:
        print("This error is update_workspace_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

