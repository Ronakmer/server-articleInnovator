
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_api_key_serializer
from apiApp.models import user_api_key, user_detail
from django.db.models import Q
from django.contrib.auth.models import User


# show user api key
@api_view(['GET'])
def list_user_api_key(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        # status = request.GET.get('status', None)
        email = request.GET.get('email', None)
        slug_id = request.GET.get('slug_id', None)

        filters = Q()
        if slug_id:
            filters &= Q(slug_id=slug_id)

        if email:
            try:
                email_obj = User.objects.get(email=email)
                
                filters &= Q(email=email_obj)
                
            except User.DoesNotExist:
                return JsonResponse({
                    "error": "email not found "
                }, status=404)

        try:
            obj = user_api_key.objects.filter(filters).order_by('-created_date')
        except user_api_key.DoesNotExist:
            return JsonResponse({
                "error": "user api key not found.",
            }, status=404) 

        # Apply pagination
        obj = obj[offset:offset + limit]

        serialized_data = user_api_key_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "user_api_keys":serialized_data.data,
        }, status=200)

    except Exception as e:
        print("This error is list_user_api_key --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add user api key
@api_view(['POST'])
def add_user_api_key(request):
    try:
        user_detail_slug_id = request.data.get('user_detail_slug_id')

        if not user_detail_slug_id:
            return JsonResponse({
                "error": "user detail slug required fields."
            }, status=400)

        try:
            user_detail_obj = user_detail.objects.get(slug_id = user_detail_slug_id)                
        except user_detail.DoesNotExist:
            return JsonResponse({"error": "user not found."}, status=404)

        data = request.data.copy()
        data["user_detail_id"] = user_detail_obj.id  

        serialized_data = user_api_key_serializer(data=data)
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "user_api_key": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_user_api_key --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
    
# update user api key
@api_view(['PUT'])
def update_user_api_key(request, slug_id):
    try:

        try:
            obj = user_api_key.objects.get(slug_id=slug_id)
        except user_api_key.DoesNotExist:
            return JsonResponse({
                "error": "user api key not found.",
            }, status=404)   

        user_detail_slug_id = request.data.get('user_detail_slug_id')

        if not user_detail_slug_id:
            return JsonResponse({
                "error": "user detail slug required fields."
            }, status=400)

        try:
            user_detail_obj = user_detail.objects.get(slug_id = user_detail_slug_id)                
        except user_detail.DoesNotExist:
            return JsonResponse({"error": "user not found."}, status=404)

        data = request.data.copy()
        data["user_detail_id"] = user_detail_obj.id  

        serialized_data = user_api_key_serializer(instance=obj, data=data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "user_api_key": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_user_api_key --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)



# delete user api key
@api_view(['DELETE'])
def delete_user_api_key(request, slug_id):
    try:
        try:
            obj = user_api_key.objects.get(slug_id=slug_id)
        except user_api_key.DoesNotExist:
            return JsonResponse({
                "error": "user api key not found.",
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_user_api_key --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


