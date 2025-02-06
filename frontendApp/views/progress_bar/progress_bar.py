
from django.shortcuts import render,redirect

# Create your views here.


def progress_bar_page(request):
    try:
        return render(request,'frontendApp/progress_bar/progress_bar.html')
    except Exception as e:
        print("This error is progress_bar_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})


