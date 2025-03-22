from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import dynamic_avatar_image_serializer
from apiApp.models import dynamic_avatar_image
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination



# show dynamic avatar image
@api_view(['GET'])
def list_dynamic_avatar_image(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        avatar_type = request.GET.get('avatar_type', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')  

        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        
        if avatar_type:
            filters &= Q(avatar_type=avatar_type)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(avatar_type__icontains=search) 

        try:
            obj = dynamic_avatar_image.objects.filter(filters).order_by(order_by)
        except dynamic_avatar_image.DoesNotExist:
            return JsonResponse({
                "error": "dynamic avatar image not found.",
                "success": False,
            }, status=404)   

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        serialized_data = dynamic_avatar_image_serializer(obj, many=True)
        
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
        print("This error is list_dynamic_avatar_image --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add dynamic avatar image
@api_view(['POST'])
def add_dynamic_avatar_image(request):
    try:
        serialized_data = dynamic_avatar_image_serializer(data=request.data)

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
        print("This error is add_dynamic_avatar_image --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update dynamic avatar image
@api_view(['PATCH'])
def update_dynamic_avatar_image(request, slug_id):
    try:

        try:
            obj = dynamic_avatar_image.objects.get(slug_id=slug_id)
        except dynamic_avatar_image.DoesNotExist:
            return JsonResponse({
                "error": "dynamic avatar image not found.",
                "success": False,
            }, status=404)   

        serialized_data = dynamic_avatar_image_serializer(instance=obj, data=request.data, partial=True)        
        
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
        print("This error is update_dynamic_avatar_image --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


# delete dynamic avatar image
@api_view(['DELETE'])
def delete_dynamic_avatar_image(request, slug_id):
    try:
        try:
            obj = dynamic_avatar_image.objects.get(slug_id=slug_id)
        except dynamic_avatar_image.DoesNotExist:
            return JsonResponse({
                "error": "dynamic avatar image not found.",
                "success": False,
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_dynamic_avatar_image --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


