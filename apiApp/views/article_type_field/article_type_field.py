from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import article_type_field_serializer
from apiApp.models import article_type_field
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination



# show article type field
@api_view(['GET'])
def list_article_type_field(request):
    try:

        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')

        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(name__icontains=search) 
            
        try:
            obj = article_type_field.objects.filter(filters).order_by(order_by)
        except article_type_field.DoesNotExist:
            return JsonResponse({
                "error": "article type field not found",
                "success": False,
            }, status=404)

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        serialized_data = article_type_field_serializer(obj, many=True)
        
        return JsonResponse({
            "data":serialized_data.data,
            "success": True,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },
        }, status=200)

    except Exception as e:
        print("This error is list_article_type_field --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add article type field
@api_view(['POST'])
def add_article_type_field(request):
    try:
        serialized_data = article_type_field_serializer(data=request.data)

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
        print("This error is add_article_type_field --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update article type field
@api_view(['PATCH'])
def update_article_type_field(request, slug_id):
    try:

        try:
            obj = article_type_field.objects.get(slug_id=slug_id)
        except article_type_field.DoesNotExist:
            return JsonResponse({
                "error": "article type field not found.",
                "success": False,
            }, status=404)   

        serialized_data = article_type_field_serializer(instance=obj, data=request.data, partial=True)        
        
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
        print("This error is update_article_type_field --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


# delete article type field
@api_view(['DELETE'])
def delete_article_type_field(request, slug_id):
    try:
        try:
            obj = article_type_field.objects.get(slug_id=slug_id)
        except article_type_field.DoesNotExist:
            return JsonResponse({
                "error": "article type field not found.",
                "success": False,
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_article_type_field --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)
