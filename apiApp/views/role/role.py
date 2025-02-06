from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import role_serializer
from apiApp.models import role
from django.db.models import Q



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

        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(name__icontains=search) 
            # filters &= Q(name__icontains=search) | Q(status__icontains=search)


        try:
            obj = role.objects.filter(filters).order_by('-created_date')
        except role.DoesNotExist:
            return JsonResponse({
                "error": "role not found.",
            }, status=404) 

        # Apply pagination
        total_count = obj.count()
        obj = obj[offset:offset + limit]


        # obj = role.objects.all()
        serialized_data = role_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "roles":serialized_data.data,
            "total_count": total_count,
        }, status=200)

    except Exception as e:
        print("This error is list_role --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add role
@api_view(['POST'])
def add_role(request):
    try:
        serialized_data = role_serializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "role": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_role --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update role
@api_view(['PUT'])
def update_role(request, slug_id):
    try:

        try:
            obj = role.objects.get(slug_id=slug_id)
        except role.DoesNotExist:
            return JsonResponse({
                "error": "role not found.",
            }, status=404)   

        serialized_data = role_serializer(instance=obj, data=request.data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "role": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_role --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


# delete role
@api_view(['DELETE'])
def delete_role(request, slug_id):
    try:
        try:
            obj = role.objects.get(slug_id=slug_id)
        except role.DoesNotExist:
            return JsonResponse({
                "error": "role not found.",
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_role --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


