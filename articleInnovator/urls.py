"""
URL configuration for articleInnovator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("dev-admin/", admin.site.urls),
    path('', include('frontendApp.urls')),
    path('api/', include('apiApp.urls')),
    path('message-service-api/', include('AIMessageService.urls')),
    path('competitor-api/', include('competitorApp.urls')),
    
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)