

from django.shortcuts import render,redirect


def list_ai_rate_limiter_page(request):
    try:
        return render(request,'frontendApp/ai_rate_limiter/list_ai_rate_limiter.html')
    except Exception as e:
        print("This error is list_ai_rate_limiter_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})
