


from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
from django.db.models import Q
from AIMessageService.models import input_json
from AIMessageService.serializers import input_json_serializer
from AIMessageService.views.base.process_pagination.process_pagination import process_pagination
import json
# import redis




@api_view(['GET'])
def list_article_input_json(request):
    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        message_id = request.GET.get('message_id', None)
        article_id = request.GET.get('article_slug_id', None)
        search = request.GET.get('search', '')
        message_field_type = request.GET.get('message_field_type', '')
        order_by = request.GET.get('order_by', '-created_date')

        # Initialize filters
        filters = Q()
        
        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if message_id:
            filters &= Q(message_id=message_id)
        if article_id:
            filters &= Q(article_id=article_id)
       
        if search:
            filters &= (
                Q(message_id__icontains=search) |
                Q(article_id__icontains=search)
            )


        # print(message_field_type,'message_field_type')
        print(article_id,'article_slug_id')

        try:
            obj = input_json.objects.filter(filters).order_by(order_by)
        except input_json.DoesNotExist:
            return JsonResponse({
                "error": "input_json not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        serialized_data = input_json_serializer(obj, many=True)

        return JsonResponse({
            "data": serialized_data.data,
            "success": True,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },
        }, status=200)

    except Exception as e:
        print("Error in list_article_input_json:", e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)


    


def add_article_input_json(request_data):
    try:
        serializer = input_json_serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return {
                'success': True,
                'message': 'Data saved successfully',
                'data': serializer.data,
                'status': 200
            }

        return {
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors,
            'status': 400
        }

    except Exception as e:
        print("Error in save_article_input_json:", e)
        return {'success': False,'message': 'Internal server error','status': 500}
