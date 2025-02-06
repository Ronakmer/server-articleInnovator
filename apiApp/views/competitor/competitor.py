from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import competitor_serializer
from apiApp.models import competitor
from django.db.models import Q


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

        # Initialize filters
        filters = Q()

        # # Apply filters based on provided parameters
        # if status:
        #     filters &= Q(status=status)
        if competitor_domain_name:
            filters &= Q(competitor_domain_name=competitor_domain_name)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        try:
            obj = competitor.objects.filter(filters).order_by('-created_date')
        except competitor.DoesNotExist:
            return JsonResponse({
                "error": "competitor not found.",
            }, status=404) 
            
        # Apply pagination
        obj = obj[offset:offset + limit]

        serialized_data = competitor_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "competitors":serialized_data.data,
        }, status=200)

    except Exception as e:
        print("This error is list_competitor --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add competitor
@api_view(['POST'])
def add_competitor(request):
    try:
        serialized_data = competitor_serializer(data=request.data)
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "competitor": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_competitor --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update competitor
@api_view(['PUT'])
def update_competitor(request, slug_id):
    try:

        try:
            obj = competitor.objects.get(slug_id=slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({
                "error": "competitor not found.",
            }, status=404)   

        serialized_data = competitor_serializer(instance=obj, data=request.data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "competitor": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_competitor --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


# delete competitor
@api_view(['DELETE'])
def delete_competitor(request, slug_id):
    try:
        try:
            obj = competitor.objects.get(slug_id=slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({
                "error": "competitor not found.",
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_competitor --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


