from django.shortcuts import render,redirect



def list_competitor_page(request):
    try:
        return render(request,'frontendApp/competitors/list_competitor.html')
    except Exception as e:
        print("This error is list_competitor_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



