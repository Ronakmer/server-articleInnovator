
from django.shortcuts import render,redirect

# Create your views here.


def list_activity_log_page(request):
    try:
        return render(request,'frontendApp/activity_log/list_activity_log.html')
    except Exception as e:
        print("This error is list_activity_log_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})
