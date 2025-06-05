
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import workspace_serializer
from apiApp.models import workspace, user_detail
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from django.db.models import Q



def process_pagination(obj, offset=0, limit=100):

    total_count = obj.count()
    obj = obj[offset:offset + limit]
    page = (offset // limit) + 1 if limit > 0 else 1
    total_pages = (total_count // limit) + (1 if total_count % limit > 0 else 0)

    return obj, total_count, page, total_pages



# def process_pagination(obj, offset=0, limit=100):
#     total_count = len(obj)
#     obj = obj[offset:offset + limit]
#     page = (offset // limit) + 1 if limit > 0 else 1
#     total_pages = (total_count // limit) + (1 if total_count % limit > 0 else 0)
#     return obj, total_count, page, total_pages

