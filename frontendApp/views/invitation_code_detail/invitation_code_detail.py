
from django.shortcuts import render,redirect

# Create your views here.


def add_invitation_code_detail_page(request):
    try:
        return render(request,'frontendApp/invitation_code_detail/add_invitation_code_detail.html')
    except Exception as e:
        print("This error is add_invitation_code_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_invitation_code_detail_page(request):
    try:
        return render(request,'frontendApp/invitation_code_detail/list_invitation_code_detail.html')
    except Exception as e:
        print("This error is list_invitation_code_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_invitation_code_detail_page(request, slug_id):
    try:
        return render(request,'frontendApp/invitation_code_detail/add_invitation_code_detail.html')
    except Exception as e:
        print("This error is update_invitation_code_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

