
from django.shortcuts import render,redirect

# Create your views here.


def list_queues_page(request):
    try:
        return render(request,'frontendApp/queues/list_queues.html')
    except Exception as e:
        print("This error is list_queues_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})