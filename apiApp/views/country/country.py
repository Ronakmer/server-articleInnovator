from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import country_serializer
from apiApp.models import country

# from .serializers import ImageUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show country
@api_view(['GET'])
def list_country(request):
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
            obj = country.objects.filter(filters).order_by(order_by)
        except country.DoesNotExist:
            return JsonResponse({
                "error": "country not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)


        serialized_data = country_serializer(obj, many=True)
        
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
        print("This error is list_country --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add country
@api_view(['POST'])
def add_country(request):
    try:
        serialized_data = country_serializer(data=request.data)

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
        print("This error is add_country --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update country
@api_view(['PATCH'])
def update_country(request, slug_id):
    try:

        try:
            obj = country.objects.get(slug_id=slug_id)
        except country.DoesNotExist:
            return JsonResponse({
                "error": "country not found.",
                "success": False,
            }, status=404)   

        serialized_data = country_serializer(instance=obj, data=request.data, partial=True)        
        
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
        print("This error is update_country --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


# delete country
@api_view(['DELETE'])
def delete_country(request, slug_id):
    try:
        try:
            obj = country.objects.get(slug_id=slug_id)
        except country.DoesNotExist:
            return JsonResponse({
                "error": "country not found.",
                "success": False,
            }, status=404) 

        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_country --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



