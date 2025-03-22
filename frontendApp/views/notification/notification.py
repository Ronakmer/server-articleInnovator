
from django.shortcuts import render,redirect

# Create your views here.


def list_notification_page(request):
    try:
        return render(request,'frontendApp/notification/list_notification.html')
    except Exception as e:
        print("This error is list_notification_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})
