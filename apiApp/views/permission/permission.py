from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import permission_serializer
from apiApp.models import permission
from django.db.models import Q



# show permission
@api_view(['GET'])
def list_permission(request):
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
            obj = permission.objects.filter(filters).order_by('-created_date')
        except permission.DoesNotExist:
            return JsonResponse({
                "error": "permission not found.",
            }, status=404) 

        # Apply pagination
        total_count = obj.count()
        obj = obj[offset:offset + limit]


        # obj = permission.objects.all()
        serialized_data = permission_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "permissions":serialized_data.data,
            "total_count": total_count,
        }, status=200)

    except Exception as e:
        print("This error is list_permission --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add permission
@api_view(['POST'])
def add_permission(request):
    try:
        serialized_data = permission_serializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "permission": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_permission --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update permission
@api_view(['PUT'])
def update_permission(request, slug_id):
    try:

        try:
            obj = permission.objects.get(slug_id=slug_id)
        except permission.DoesNotExist:
            return JsonResponse({
                "error": "permission not found.",
            }, status=404)   

        serialized_data = permission_serializer(instance=obj, data=request.data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "permission": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_permission --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


# delete permission
@api_view(['DELETE'])
def delete_permission(request, slug_id):
    try:
        try:
            obj = permission.objects.get(slug_id=slug_id)
        except permission.DoesNotExist:
            return JsonResponse({
                "error": "permission not found.",
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_permission --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


