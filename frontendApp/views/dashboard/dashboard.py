
from django.shortcuts import render,redirect

# Create your views here.


    
def dashboard_page(request):
    return render(request,'frontendApp/dashboard/show_dashboard.html')







