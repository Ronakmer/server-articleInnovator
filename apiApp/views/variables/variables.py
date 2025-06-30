from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import variables_serializer
from apiApp.models import variables, supportive_prompt_type, article_type
from django.db.models import Q
from loguru import logger
from apiApp.views.base.process_pagination.process_pagination import process_pagination
import json
import uuid  # Required for generating new slug_id

# show variables
@api_view(['GET'])
def list_variables(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        supportive_prompt_type_slug_id = request.GET.get('supportive_prompt_type_slug_id', None)
        article_type_slug_id = request.GET.get('article_type_slug_id', None)
        
        print(supportive_prompt_type_slug_id,'supportive_prompt_type_slug_idx')
        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(name__icontains=search) 
        if supportive_prompt_type_slug_id:
            filters &= Q(supportive_prompt_type_id__slug_id=supportive_prompt_type_slug_id) 
        if article_type_slug_id:
            filters &= Q(article_type_id__slug_id=article_type_slug_id) 

        print(supportive_prompt_type_slug_id,'supportive_prompt_type_slug_id')

        try:
            obj = variables.objects.filter(filters).order_by(order_by)
        except variables.DoesNotExist:
            return JsonResponse({
                "error": "wp prompt type not found.",
                "success": False,
            }, status=404) 
            
            

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)


        serialized_data = variables_serializer(obj, many=True)

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
        print("This error is list_variables --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)




# add variables
def add_variables(request_data, slug_id):
    try:
        if isinstance(request_data, str):
            request_data = json.loads(request_data)

        supportive_variables_list = request_data

        if not isinstance(supportive_variables_list, list):
            return None, "Invalid data format. Expected a list of variables."

        # Try to get supportive_prompt_type object
        try:
            prompt_type_obj = supportive_prompt_type.objects.get(slug_id=slug_id)
        except supportive_prompt_type.DoesNotExist:
            prompt_type_obj = None

        # Try to get article_type object
        try:
            article_type_obj = article_type.objects.get(slug_id=slug_id)
        except article_type.DoesNotExist:
            article_type_obj = None

        if not prompt_type_obj and not article_type_obj:
            return None, "No matching supportive_prompt_type or article_type with the given slug_id."


        for item in supportive_variables_list:
            if prompt_type_obj:
                item['supportive_prompt_type_id'] = prompt_type_obj.id
            elif article_type_obj:
                item['article_type_id'] = article_type_obj.id
                
            serialized_data = variables_serializer(data=item)

            if serialized_data.is_valid():
                serialized_data.save()
            else:
                return None, f"Invalid supportive variable data: {serialized_data.errors}"

        return True, None
    except Exception as e:
        print("This error is add_variables --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
    

def update_variables(request_data, slug_id):
    try:
        print(request_data,'request_datasdfsdfsdf')
        if isinstance(request_data, str):
            request_data = json.loads(request_data)

        supportive_variables_list = request_data
        print("Request Data:", supportive_variables_list)

        if not isinstance(supportive_variables_list, list):
            return None, "Invalid data format. Expected a list of variables."

        # Try to get supportive_prompt_type object
        try:
            prompt_type_obj = supportive_prompt_type.objects.get(slug_id=slug_id)
        except supportive_prompt_type.DoesNotExist:
            prompt_type_obj = None

        # Try to get article_type object
        try:
            article_type_obj = article_type.objects.get(slug_id=slug_id)
        except article_type.DoesNotExist:
            article_type_obj = None

        if not prompt_type_obj and not article_type_obj:
            return None, "No matching supportive_prompt_type or article_type with the given slug_id."

        all_updated_data = []

        for item in supportive_variables_list:
            if prompt_type_obj:
                item['supportive_prompt_type_id'] = prompt_type_obj.id
            elif article_type_obj:
                item['article_type_id'] = article_type_obj.id

            slug_id = item.get('slug_id')

            if slug_id:
                # Updating existing record
                try:
                    obj = variables.objects.get(slug_id=slug_id)
                    print(f"Updating existing supportive variable with slug_id: {slug_id}")
                    serialized_data = variables_serializer(instance=obj, data=item, partial=True)
                    if serialized_data.is_valid():
                        serialized_data.save()
                        all_updated_data.append(serialized_data.data)
                    else:
                        return None, f"Invalid supportive variable data: {serialized_data.errors}"
                except variables.DoesNotExist:
                    return None, f"variables with slug_id {slug_id} does not exist."
            else:
                # Creating new record
                # item['slug_id'] = str(uuid.uuid4())
                # print(f"Creating new supportive variable with slug_id: {item['slug_id']}")
                serialized_data = variables_serializer(data=item)
                if serialized_data.is_valid():
                    serialized_data.save()
                    all_updated_data.append(serialized_data.data)
                else:
                    return None, f"Invalid supportive variable data: {serialized_data.errors}"

        return all_updated_data, None

    except Exception as e:
        print("This error is update_variables --->: ", e)
        return None, "Internal server error."







# # delete variables
# @api_view(['DELETE'])
# def delete_variables(request, slug_id):
#     try:
#         try:
#             obj = variables.objects.get(slug_id=slug_id)
#         except variables.DoesNotExist:
#             return JsonResponse({
#                 "error": "wp prompt type not found.",
#                 "success": False,
#             }, status=404) 
                
#         obj.delete()
        
#         return JsonResponse({
#             "message": "Data Deleted successfully.",
#             "success": True,
#         }, status=200)

#     except Exception as e:
#         print("This error is delete_variables --->: ", e)
#         return JsonResponse({"error": "Internal server error.","success": False}, status=500)


