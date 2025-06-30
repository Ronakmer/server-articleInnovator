

from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
from django.db.models import Q
from AIMessageService.models import ai_message
from AIMessageService.serializers import ai_message_serializer
from AIMessageService.views.base.process_pagination.process_pagination import process_pagination
import json
# import redis



@api_view(['GET'])
def list_ai_message(request):
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
        if message_field_type:
            filters &= Q(message_field_type=message_field_type)
        if search:
            filters &= (
                Q(message_id__icontains=search) |
                Q(article_id__icontains=search) |
                Q(message_field_type__icontains=search)
            )


        print(message_field_type,'message_field_type')
        print(article_id,'article_slug_id')

        try:
            obj = ai_message.objects.filter(filters).order_by(order_by)
        except ai_message.DoesNotExist:
            return JsonResponse({
                "error": "ai_message not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        serialized_data = ai_message_serializer(obj, many=True)

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
        print("Error in list_ai_message:", e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)

    

# Add AI Message
@api_view(['POST'])
def add_ai_message(request):
    try:
        serialized_data = ai_message_serializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "data": serialized_data.data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors,
                "success": False, 
            }, status=400)


    except Exception as e:
        print("Error in add_ai_message:", e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)



# Update AI Message
@api_view(['PATCH'])
def update_ai_message(request, article_id, message_id):
    try:
        print(request.data,'sss222')
        try:
            obj = ai_message.objects.get(article_id=article_id, message_id=message_id)
        except ai_message.DoesNotExist:
            return JsonResponse({
                "error": "AI message not found.",
                "success": False,
            }, status=404)

        serialized_data = ai_message_serializer(instance=obj, data=request.data, partial=True)

        if serialized_data.is_valid():
            serialized_data.save()

            return JsonResponse({
                "message": "Data updated successfully.",
                "data": serialized_data.data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors,
                "success": False,
            }, status=400)

    except Exception as e:
        print("Error in update_ai_message:", e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)




# Delete AI Message
@api_view(['DELETE'])
def delete_ai_message(request, article_id):
    try:
        try:
            obj = ai_message.objects.filter(article_id=article_id)
        except ai_message.DoesNotExist:
            return JsonResponse({
                "error": "AI message not found.",
                "success": False,
            }, status=404) 

        obj.delete()

        return JsonResponse({
            "message": "Data deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("Error in delete_ai_message:", e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)





