from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import article_type_field_serializer
from apiApp.models import article_type_field
from django.db.models import Q



# show article type field
@api_view(['GET'])
def list_article_type_field(request):
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
            obj = article_type_field.objects.filter(filters).order_by('-created_date')
        except article_type_field.DoesNotExist:
            return JsonResponse({
                "error": "article type field not found"
            }, status=404)

        # Apply pagination
        total_count = obj.count()
        obj = obj[offset:offset + limit]

        serialized_data = article_type_field_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "article_type_fields":serialized_data.data,
            "total_count":total_count,
        }, status=200)

    except Exception as e:
        print("This error is list_article_type_field --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add article type field
@api_view(['POST'])
def add_article_type_field(request):
    try:
        serialized_data = article_type_field_serializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "article_type_field": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_article_type_field --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update article type field
@api_view(['PUT'])
def update_article_type_field(request, slug_id):
    try:

        try:
            obj = article_type_field.objects.get(slug_id=slug_id)
        except article_type_field.DoesNotExist:
            return JsonResponse({
                "error": "article type field not found.",
            }, status=404)   

        serialized_data = article_type_field_serializer(instance=obj, data=request.data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "article_type_field": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_article_type_field --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


# delete article type field
@api_view(['DELETE'])
def delete_article_type_field(request, slug_id):
    try:
        try:
            obj = article_type_field.objects.get(slug_id=slug_id)
        except article_type_field.DoesNotExist:
            return JsonResponse({
                "error": "article type field not found.",
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_article_type_field --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)
