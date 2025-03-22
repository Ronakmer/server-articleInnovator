
from django.shortcuts import render,redirect

# Create your views here.


def add_admin_detail_page(request):
    try:
        return render(request,'frontendApp/admin_detail/add_admin_detail.html')
    except Exception as e:
        print("This error is add_admin_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def list_admin_detail_page(request):
    try:
        return render(request,'frontendApp/admin_detail/list_admin_detail.html')
    except Exception as e:
        print("This error is list_admin_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



def update_admin_detail_page(request, slug_id):
    try:
        return render(request,'frontendApp/admin_detail/add_admin_detail.html')
    except Exception as e:
        print("This error is update_admin_detail_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



# def detail_admin_page(request, slug_id):
#     try:
#         return render(request,'frontendApp/admin_detail/detail_admin.html')
#     except Exception as e:
#         print("This error is update_admin_detail_page --->: ",e)
#         return render(request, 'error.html' , {'error': 500})

