# from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required

######### file import  #########
from AIMessageService.views.ai_message_api.ai_message_api import list_ai_message, add_ai_message, update_ai_message, delete_ai_message
from AIMessageService.views.article_input_json.article_input_json import list_article_input_json



permissions_list = [
    
    # # input json
    {"name": "list_article_input_json", "route": "article-input-json/", "description": "article-input-json", "status": "True", "group": "article-input-json"},

    # # ai_message_api
    {"name": "list_ai_message", "route": "ai-messages/", "description": "get all ai-message", "status": "True", "group": "ai-message"},
    {"name": "add_ai_message", "route": "ai-message/add/", "description": "add ai-message", "status": "True", "group": "ai-message"},
    {"name": "update_ai_message", "route": "ai-message/update/<str:article_id>/<str:message_id>/", "description": "update ai-message", "status": "True", "group": "ai-message"},
    {"name": "delete_ai_message", "route": "ai-message/delete/<str:article_id>/", "description": "delete ai-message", "status": "True", "group": "ai-message"},
    
]



urlpatterns = []
for perm in permissions_list:
    view_name = perm["name"]
    # Dynamically get the view class
    view_class = globals().get(view_name)
    
    if view_class:
        # If it's a class-based view, invoke .as_view() to get the callable view
        view = view_class.as_view() if hasattr(view_class, 'as_view') else view_class
        urlpatterns.append(path(route=perm["route"], view=view, name=view_name.replace(".as_view", "")))






urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

