from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import competitor_serializer
from apiApp.models import competitor
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show competitor
@api_view(['GET'])
def list_competitor(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        # status = request.GET.get('status', None)
        competitor_domain_name = request.GET.get('competitor_domain_name', None)
        slug_id = request.GET.get('slug_id', None)
        order_by = request.GET.get('order_by', '-created_date')

        # Initialize filters
        filters = Q()

        # # Apply filters based on provided parameters
        if competitor_domain_name:
            filters &= Q(competitor_domain_name=competitor_domain_name)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        try:
            obj = competitor.objects.filter(filters).order_by(order_by)
        except competitor.DoesNotExist:
            return JsonResponse({
                "error": "competitor not found.",
                "success": False,
            }, status=404) 
            
        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)


        serialized_data = competitor_serializer(obj, many=True)
        
        return JsonResponse({
            "data":serialized_data.data,
            "success": False,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },
        }, status=200)

    except Exception as e:
        print("This error is list_competitor --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add competitor
@api_view(['POST'])
def add_competitor(request):
    try:
        serialized_data = competitor_serializer(data=request.data)
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "success": True,
                "data": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is add_competitor --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update competitor
@api_view(['PATCH'])
def update_competitor(request, slug_id):
    try:

        try:
            obj = competitor.objects.get(slug_id=slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({
                "error": "competitor not found.",
                "success": False,
            }, status=404)   

        serialized_data = competitor_serializer(instance=obj, data=request.data, partial=True)        
        
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
        print("This error is update_competitor --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


# delete competitor
@api_view(['DELETE'])
def delete_competitor(request, slug_id):
    try:
        try:
            obj = competitor.objects.get(slug_id=slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({
                "error": "competitor not found.",
                "success": False,
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_competitor --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


