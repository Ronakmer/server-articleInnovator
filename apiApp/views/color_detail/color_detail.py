from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import color_detail_serializer
from apiApp.models import color_detail
from django.db.models import Q



# show color detail
@api_view(['GET'])
def list_color_detail(request):
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
            filters &= Q(bg_color__icontains=search) 

            
        try:
            obj = color_detail.objects.filter(filters).order_by('-created_date')
        except color_detail.DoesNotExist:
            return JsonResponse({
                "error": "color not found.",
            }, status=404)   


        # Apply pagination
        total_count = obj.count()
        obj = obj[offset:offset + limit]
        
        serialized_data = color_detail_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "colors":serialized_data.data,
            "total_count": total_count,
            
        }, status=200)

    except Exception as e:
        print("This error is list_color_detail --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add color detail
@api_view(['POST'])
def add_color_detail(request):
    try:
        serialized_data = color_detail_serializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "color": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_color_detail --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update color detail
@api_view(['PUT'])
def update_color_detail(request, slug_id):
    try:

        try:
            obj = color_detail.objects.get(slug_id=slug_id)
        except color_detail.DoesNotExist:
            return JsonResponse({
                "error": "color not found.",
            }, status=404)   

        serialized_data = color_detail_serializer(instance=obj, data=request.data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "color": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_color_detail --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


# delete color detail
@api_view(['DELETE'])
def delete_color_detail(request, slug_id):
    try:
        try:
            obj = color_detail.objects.get(slug_id=slug_id)
        except color_detail.DoesNotExist:
            return JsonResponse({
                "error": "color not found.",
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_color_detail --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


