from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import language_serializer
from apiApp.models import language
from django.db.models import Q


# show language
@api_view(['GET'])
def list_language(request):
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
            obj = language.objects.filter(filters).order_by('-created_date')
        except language.DoesNotExist:
            return JsonResponse({
                "error": "language not found.",
            }, status=404) 

        # Apply pagination
        total_count = obj.count()
        obj = obj[offset:offset + limit]

        
        serialized_data = language_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "languages":serialized_data.data,
            "total_count": total_count,
            
        }, status=200)

    except Exception as e:
        print("This error is list_language --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add language
@api_view(['POST'])
def add_language(request):
    try:
        serialized_data = language_serializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "language": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_language --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update language
@api_view(['PUT'])
def update_language(request, slug_id):
    try:
        try:
            obj = language.objects.get(slug_id=slug_id)
        except language.DoesNotExist:
            return JsonResponse({
                "error": "language not found.",
            }, status=404)   

        serialized_data = language_serializer(instance=obj, data=request.data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "language": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_language --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


# delete language
@api_view(['DELETE'])
def delete_language(request, slug_id):
    try:
        try:
            obj = language.objects.get(slug_id=slug_id)
        except language.DoesNotExist:
            return JsonResponse({
                "error": "language not found.",
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_language --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

