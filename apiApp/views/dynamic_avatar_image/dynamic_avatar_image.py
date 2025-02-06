from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import dynamic_avatar_image_serializer
from apiApp.models import dynamic_avatar_image
from django.db.models import Q



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
            obj = dynamic_avatar_image.objects.filter(filters).order_by('-created_date')
        except dynamic_avatar_image.DoesNotExist:
            return JsonResponse({
                "error": "dynamic avatar image not found.",
            }, status=404)   

        # Apply pagination
        total_count = obj.count()
        obj = obj[offset:offset + limit]
        
        serialized_data = dynamic_avatar_image_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "dynamic_avatar_images":serialized_data.data,
            "total_count": total_count,
            
        }, status=200)

    except Exception as e:
        print("This error is list_dynamic_avatar_image --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add dynamic avatar image
@api_view(['POST'])
def add_dynamic_avatar_image(request):
    try:
        serialized_data = dynamic_avatar_image_serializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "dynamic_avatar_image": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_dynamic_avatar_image --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update dynamic avatar image
@api_view(['PUT'])
def update_dynamic_avatar_image(request, slug_id):
    try:

        try:
            obj = dynamic_avatar_image.objects.get(slug_id=slug_id)
        except dynamic_avatar_image.DoesNotExist:
            return JsonResponse({
                "error": "dynamic avatar image not found.",
            }, status=404)   

        serialized_data = dynamic_avatar_image_serializer(instance=obj, data=request.data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "dynamic_avatar_image": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_dynamic_avatar_image --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


# delete dynamic avatar image
@api_view(['DELETE'])
def delete_dynamic_avatar_image(request, slug_id):
    try:
        try:
            obj = dynamic_avatar_image.objects.get(slug_id=slug_id)
        except dynamic_avatar_image.DoesNotExist:
            return JsonResponse({
                "error": "dynamic avatar image not found.",
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_dynamic_avatar_image --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


