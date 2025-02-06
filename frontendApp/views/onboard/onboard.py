



from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def onboard_page(request):
    try:
        return render(request,'frontendApp/onboard/onboard.html')
    except Exception as e:
        print("This error is onboard_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})

