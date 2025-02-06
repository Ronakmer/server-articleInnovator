from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import country_serializer
from apiApp.models import country

# from .serializers import ImageUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


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
            obj = country.objects.filter(filters).order_by('-created_date')
        except country.DoesNotExist:
            return JsonResponse({
                "error": "country not found.",
            }, status=404) 

        # Apply pagination
        total_count = obj.count()
        obj = obj[offset:offset + limit]
        
        serialized_data = country_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "countries":serialized_data.data,
            "total_count": total_count,
            
        }, status=200)

    except Exception as e:
        print("This error is list_country --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add country
@api_view(['POST'])
def add_country(request):
    try:
        serialized_data = country_serializer(data=request.data)

        if serialized_data.is_valid():
            
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "country": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_country --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update country
@api_view(['PUT'])
def update_country(request, slug_id):
    try:

        try:
            obj = country.objects.get(slug_id=slug_id)
        except country.DoesNotExist:
            return JsonResponse({
                "error": "country not found.",
            }, status=404)   

        serialized_data = country_serializer(instance=obj, data=request.data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "country": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_country --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


# delete country
@api_view(['DELETE'])
def delete_country(request, slug_id):
    try:
        try:
            obj = country.objects.get(slug_id=slug_id)
        except country.DoesNotExist:
            return JsonResponse({
                "error": "country not found.",
            }, status=404) 

        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_country --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)



