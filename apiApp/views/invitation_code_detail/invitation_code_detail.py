from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import invitation_code_detail_serializer
from apiApp.models import invitation_code_detail
from django.contrib.auth.models import User
from django.db.models import Q

from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show invitation code details
@api_view(['GET'])
def list_invitation_code_detail(request):
    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        # status = request.GET.get('status', None)
        used = request.GET.get('used', None)
        email = request.GET.get('email', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()
        
        if used:
            filters &= Q(used=used)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(email__icontains=search) 

        if email:
            try:
                email_obj = User.objects.get(email=email)
                
                filters &= Q(email=email_obj)
                
            except User.DoesNotExist:
                return JsonResponse({
                    "error": "email not found ",
                    "success": False,
                }, status=404)

        try:
            obj = invitation_code_detail.objects.filter(filters).order_by(order_by)
        except invitation_code_detail.DoesNotExist:
            return JsonResponse({
                "error": "invitation code detail not found.",
                "success": False,
            }, status=404)   


        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        # Serialize the data
        serialized_data = invitation_code_detail_serializer(obj, many=True)
        
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
        print("This error is list_invitation_code_detail --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add invitation code details
@api_view(['POST'])
def add_invitation_code_detail(request):
    try:
        request_user = request.user

        email = request.data.get("email")  

        if email:
            try:
                email_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({
                    "error": "email not found ",
                    "success": False,
                }, status=404)

        # Include `color_detail_id` in the request data for the serializer
        data = request.data.copy()
        data['created_by'] = request_user.id
        if email:
            data['email'] = email_obj.id

        serialized_data = invitation_code_detail_serializer(data=data)

        if serialized_data.is_valid():
            try:
                serialized_data.save()
                
                return JsonResponse({
                    "message": "Data added successfully.",
                    "data": serialized_data.data,
                    "success": True,
                }, status=200)
            except:
                return JsonResponse({
                    "error": "invitation code already exists. Please use a unique code.",
                    "success": False,
                }, status=409)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is add_invitation_code_detail --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update invitation code details
@api_view(['PATCH'])
def update_invitation_code_detail(request, slug_id):
    try:

        try:
            obj = invitation_code_detail.objects.get(slug_id=slug_id)
        except invitation_code_detail.DoesNotExist:
            return JsonResponse({
                "error": "invitation code detail not found.",
                "success": False,
            }, status=404)   
                
        email = request.data.get("email")  

        if email:
            try:
                email_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({
                    "error": "email not found ",
                    "success": False,
                }, status=404)

        data = request.data.copy()
        data['created_by'] = obj.created_by.id
        if email:
            data['email'] = email_obj.id

        serialized_data = invitation_code_detail_serializer(instance=obj, data=data, partial=True)        
        
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
        print("This error is update_invitation_code_detail --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# delete invitation code details
@api_view(['DELETE'])
def delete_invitation_code_detail(request, slug_id):
    try:
        try:
            obj = invitation_code_detail.objects.get(slug_id=slug_id)
        except invitation_code_detail.DoesNotExist:
            return JsonResponse({
                "error": "invitation code detail not found.",
                "success": False,
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_invitation_code_detail --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


