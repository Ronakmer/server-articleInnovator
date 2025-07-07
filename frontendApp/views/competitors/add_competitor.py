from django.shortcuts import render,redirect



def add_competitor_page(request):
    try:
        return render(request,'frontendApp/competitors/add_competitor.html')
    except Exception as e:
        print("This error is add_competitor_page --->: ",e)
        return render(request, 'error.html' , {'error': 500})



