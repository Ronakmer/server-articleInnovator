
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_api_key_serializer
from apiApp.models import user_api_key, user_detail
from django.db.models import Q
from django.contrib.auth.models import User
from apiApp.views.base.process_pagination.process_pagination import process_pagination


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
        order_by = request.GET.get('order_by', '-created_date')


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
            obj = user_api_key.objects.filter(filters).order_by(order_by)
        except user_api_key.DoesNotExist:
            return JsonResponse({
                "error": "user api key not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        serialized_data = user_api_key_serializer(obj, many=True)
        
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
        print("This error is list_user_api_key --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add user api key
@api_view(['POST'])
def add_user_api_key(request):
    try:
        user_detail_slug_id = request.data.get('user_detail_slug_id')

        if not user_detail_slug_id:
            return JsonResponse({
                "error": "user detail slug required fields.",
                "success": False,
            }, status=400)

        try:
            user_detail_obj = user_detail.objects.get(slug_id = user_detail_slug_id)                
        except user_detail.DoesNotExist:
            return JsonResponse({"error": "user not found.","success": False}, status=404)

        data = request.data.copy()
        data["user_detail_id"] = user_detail_obj.id  

        serialized_data = user_api_key_serializer(data=data)
        
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
        print("This error is add_user_api_key --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
    
# update user api key
@api_view(['PATCH'])
def update_user_api_key(request, slug_id):
    try:

        try:
            obj = user_api_key.objects.get(slug_id=slug_id)
        except user_api_key.DoesNotExist:
            return JsonResponse({
                "error": "user api key not found.",
                "success": False,
            }, status=404)   

        user_detail_slug_id = request.data.get('user_detail_slug_id')

        if not user_detail_slug_id:
            return JsonResponse({
                "error": "user detail slug required fields.",
                "success": False,
            }, status=400)

        try:
            user_detail_obj = user_detail.objects.get(slug_id = user_detail_slug_id)                
        except user_detail.DoesNotExist:
            return JsonResponse({"error": "user not found.","success": False}, status=404)

        data = request.data.copy()
        data["user_detail_id"] = user_detail_obj.id  

        serialized_data = user_api_key_serializer(instance=obj, data=data, partial=True)        
        
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
        print("This error is update_user_api_key --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# delete user api key
@api_view(['DELETE'])
def delete_user_api_key(request, slug_id):
    try:
        try:
            obj = user_api_key.objects.get(slug_id=slug_id)
        except user_api_key.DoesNotExist:
            return JsonResponse({
                "error": "user api key not found.",
                "success": False,
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_user_api_key --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


