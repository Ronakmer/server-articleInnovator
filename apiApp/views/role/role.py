from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import role_serializer
from apiApp.models import role
from django.db.models import Q
from loguru import logger
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show role
@api_view(['GET'])
def list_role(request):
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
            obj = role.objects.filter(filters).order_by(order_by)
        except role.DoesNotExist:
            return JsonResponse({
                "error": "role not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)


        serialized_data = role_serializer(obj, many=True)

        # logger.info("This is an info log message", extra={"notify": True, "status_code": 200, "workspace_slug_id": '77b4ad49-db8a-4434-aad5-c2351c953cc7', "url":request.path, "request_user": request.user, "domain_slug_id":'ec676a34-eb18-4610-b1b8-99ba7d26d87a', "user_status":True })

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
        print("This error is list_role --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add role
@api_view(['POST'])
def add_role(request):
    try:
        serialized_data = role_serializer(data=request.data)

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
        print("This error is add_role --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update role
@api_view(['PATCH'])
def update_role(request, slug_id):
    try:

        try:
            obj = role.objects.get(slug_id=slug_id)
        except role.DoesNotExist:
            return JsonResponse({
                "error": "role not found.",
                "success": False,
            }, status=404)   

        serialized_data = role_serializer(instance=obj, data=request.data, partial=True)        
        
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
        print("This error is update_role --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


# delete role
@api_view(['DELETE'])
def delete_role(request, slug_id):
    try:
        try:
            obj = role.objects.get(slug_id=slug_id)
        except role.DoesNotExist:
            return JsonResponse({
                "error": "role not found.",
                "success": False,
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_role --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


