
from django.shortcuts import render,redirect

# Create your views here.


def add_color_detail_page(request):
    try:
        return render(request,'frontendApp/color_detail/add_color_detail.html')
    except Exception as e:
        print("This error is add_color_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_color_detail_page(request):
    try:
        return render(request,'frontendApp/color_detail/list_color_detail.html')
    except Exception as e:
        print("This error is list_color_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

def update_color_detail_page(request, slug_id):
    try:
        return render(request,'frontendApp/color_detail/add_color_detail.html')
    except Exception as e:
        print("This error is update_color_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

