
from django.shortcuts import render,redirect

# Create your views here.


def error_page(request):
    try:
        return render(request,'frontendApp/base/error_page.html')
    except Exception as e:
        print("This error is error_page --->: ",e)
        # return render(request, 'error.html' , {'error': 500})


