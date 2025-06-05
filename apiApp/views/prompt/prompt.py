

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import prompt_serializer
from apiApp.models import prompt, workspace, article_type, user_detail, domain
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from apiApp.views.decorator.domain_decorator import domain_permission_required
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination
import json


# show prompt
@api_view(['GET'])
# @workspace_permission_required
@domain_permission_required
def list_prompt(request):
    try:
        request_user = request.user
        
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        article_type_slug_id = request.GET.get('article_type_slug_id', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        article_category = request.GET.get('article_category', None)
        category = request.GET.get('category', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            # filters &= Q(name__icontains=search)
            filters &= (
                Q(name__icontains=search) |
                Q(article_type_id__slug_id__icontains=search)
            )
            
        print(search,'searchx')


        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id=workspace_obj)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found.",
                    "success": False,
                }, status=404)  
            
        if article_category:
            try:
                article_category = article_type.objects.get(article_category=article_category)
                filters &= Q(article_category=article_category)
            except article_type.DoesNotExist:
                return JsonResponse({"error": "article category not found.","success": False}, status=404)
        if category:
            try:
                category = article_type.objects.get(category=category)
                filters &= Q(category=category)
            except article_type.DoesNotExist:
                return JsonResponse({"error": "category not found.","success": False}, status=404)

        if article_type_slug_id:
            try:
                article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)
                filters &= Q(article_type_id=article_type_obj)
            except article_type.DoesNotExist:
                return JsonResponse({"error": "Article type not found.","success": False}, status=404)
        
        if request_user.is_superuser:
            try:
                obj = prompt.objects.filter(filters).order_by(order_by)
            except prompt.DoesNotExist:
                return JsonResponse({
                    "error": "prompt not found.",
                    "success": False,
                }, status=404) 
        
        if request.is_admin:
                try:
                    obj = prompt.objects.filter(filters).distinct().order_by(order_by)
                except prompt.DoesNotExist:
                    return JsonResponse({
                        "error": "prompt not found.",
                        "success": False,
                    }, status=404)   
            

        print(obj,'pppppppppppppppppppp')
        print(len(obj),'qqqqqqqqqqqqqqqqqqq')
        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        serialized_data = prompt_serializer(obj, many=True)
        
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
        print("This error is list_prompt --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# # add prompt
# @api_view(['POST'])
# # @workspace_permission_required
# @domain_permission_required
# def add_prompt(request):
#     try:
#         request_user = request.user
        
#         workspace_slug_id = request.data.get('workspace_slug_id')
#         article_type_slug_id = request.data.get('article_type_slug_id')
        
#         if not workspace_slug_id:
#             return JsonResponse({
#                 "error": "Workspace slug id are required .",
#                 "success": False,
#             }, status=404)
            
#         if not article_type_slug_id:
#             return JsonResponse({
#                 "error": "Article Type slug id are required.",
#                 "success": False,
#             }, status=404)

#         try:
#             workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
#             article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)
#         except workspace.DoesNotExist:
#             return JsonResponse({"error": "Workspace not found.","success": False}, status=404)
#         except article_type.DoesNotExist:
#             return JsonResponse({"error": "Article Type not found.","success": False}, status=404)

        
#         print(workspace_obj.id, article_type_obj.id)
#         # Include data in the request data for the serializer
#         data = request.data.copy()
#         data['workspace_id'] = workspace_obj.id
#         data['article_type_id'] = article_type_obj.id
#         data['created_by'] = request_user.id
        
#         print(data)
#         serialized_data = prompt_serializer(data=data)

#         if serialized_data.is_valid():
#             serialized_data.save()
            
#             return JsonResponse({
#                 "message": "Data added successfully.",
#                 "data": serialized_data.data,
#                 "success": True,
#             }, status=200)
#         else:
#             return JsonResponse({
#                 "error": "Invalid data.",
#                 "errors": serialized_data.errors, 
#                 "success": False,
#             }, status=400)

#     except Exception as e:
#         print("This error is add_prompt --->: ", e)
#         return JsonResponse({"error": "Internal server error.","success": False}, status=500)





@api_view(['POST'])
@domain_permission_required
def add_prompt(request):
    try:
        request_user = request.user
        
        print(request.data,'fffffffffffffffff')
        # Retrieve required fields
        # workspace_slugs = request.data.get("workspace_slug_id")
        # article_type_slug_id = request.data.get("article_type_slug_id")
        
        # if not workspace_slugs:
        #     return JsonResponse({
        #         "error": "Workspace slug ID(s) are required.",
        #         "success": False,
        #     }, status=400)
        
        # if not article_type_slug_id:
        #     return JsonResponse({
        #         "error": "Article Type slug ID is required.",
        #         "success": False,
        #     }, status=400)
        
        
        # Define required fields (static)
        required_fields = ["workspace_slug_id", "article_type_slug_id"]

        # Identify dynamic fields (keys starting with 'supportive_prompt_')
        # dynamic_fields = [key for key in request.data.keys() if key.startswith("supportive_prompt_")]

        # Combine all required fields
        # all_required_fields = required_fields + dynamic_fields
        all_required_fields = required_fields
        
        # Validate required fields
        missing_fields = [field for field in all_required_fields if not request.data.get(field)]
        if missing_fields:
            return JsonResponse({
                "error": f"Missing required fields: {', '.join(missing_fields)}",
                "success": False,
            }, status=400)
            
            
        workspace_slugs = request.data.get("workspace_slug_id")
        article_type_slug_id = request.data.get("article_type_slug_id")

        
        # Convert workspace_slug_id to a list if it's a string
        if isinstance(workspace_slugs, str):
            workspace_slugs = workspace_slugs.split(",")
        
        # Get all workspace objects
        workspace_objs = workspace.objects.filter(slug_id__in=workspace_slugs)
        if workspace_objs.count() != len(workspace_slugs):
            return JsonResponse({
                "error": "One or more workspace(s) not found.",
                "success": False,
            }, status=404)
        
        # Get the article type object
        try:
            article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)
        except article_type.DoesNotExist:
            return JsonResponse({
                "error": "Article Type not found.",
                "success": False,
            }, status=404)
        
        created_data = []
        errors = []
        
        for workspace_obj in workspace_objs:
            data = request.data.copy()
            data["workspace_id"] = workspace_obj.id
            data["article_type_id"] = article_type_obj.id
            data["created_by"] = request_user.id
            
            # Extracting `supportive_prompt_*` fields and converting them into JSON format
            supportive_prompt_json_data = {
                key: (value[0] if isinstance(value, list) and value else value)
                for key, value in request.data.items()
                if key.startswith("supportive_prompt_")
            }
            print(supportive_prompt_json_data,'supportive_prompt_json_dataxxxxx')

            # Convert the dictionary to a JSON string
            data["supportive_prompt_json_data"] = json.dumps(supportive_prompt_json_data)

            serialized_data = prompt_serializer(data=data)
            if serialized_data.is_valid():
                serialized_data.save()
                created_data.append(serialized_data.data)
            else:
                errors.append(serialized_data.errors)
        
        if errors:
            return JsonResponse({
                "error": "Some prompts failed to add.",
                "success": False,
                "errors": errors,
                "data": created_data,
            }, status=400)
        
        return JsonResponse({
            "message": "All data added successfully.",
            "success": True,
            "data": created_data,
        }, status=201)
    
    except Exception as e:
        print(f"Error in add_prompt: {e}")
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)


    
@api_view(['PATCH'])
@domain_permission_required
def update_prompt(request, slug_id):
    try:
        request_user = request.user

        try:
            obj = prompt.objects.get(slug_id=slug_id)
        except prompt.DoesNotExist:
            return JsonResponse({
                "error": "Prompt not found.",
                "success": False,
            }, status=404)


        status = request.data.get("status")
        if status is not None and status != "":
            serialized_data = prompt_serializer(instance=obj, data=request.data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return JsonResponse({
                    "message": "Status updated successfully.",
                    "success": True,
                    "data": serialized_data.data,
                }, status=200)
            else:
                return JsonResponse({
                    "error": "Invalid data.",
                    "errors": serialized_data.errors,
                    "success": False,
                }, status=400)
                
        # Define required static fields
        required_fields = ["workspace_slug_id", "article_type_slug_id"]

        # Identify dynamic fields (keys starting with 'supportive_prompt_')
        # dynamic_fields = [key for key in request.data.keys() if key.startswith("supportive_prompt_")]

        # Combine all required fields
        # all_required_fields = required_fields + dynamic_fields
        all_required_fields = required_fields

        # Validate missing fields
        missing_fields = [field for field in all_required_fields if not request.data.get(field)]
        if missing_fields:
            return JsonResponse({
                "error": f"Missing required fields: {', '.join(missing_fields)}",
                "success": False,
            }, status=400)

        # Fetch workspace
        workspace_slug = request.data.get("workspace_slug_id")
        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "Workspace not found.",
                "success": False,
            }, status=404)

        # Fetch article type
        article_type_slug_id = request.data.get("article_type_slug_id")
        try:
            article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)
        except article_type.DoesNotExist:
            return JsonResponse({
                "error": "Article Type not found.",
                "success": False,
            }, status=404)

        # Create a copy of the request data
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id
        data["article_type_id"] = article_type_obj.id
        data["created_by"] = request_user.id  # If you're using updated_by, replace accordingly

        # Handle supportive_prompt_* fields
        supportive_prompt_json_data = {
            key: (value[0] if isinstance(value, list) and value else value)
            for key, value in request.data.items()
            if key.startswith("supportive_prompt_")
        }
        data["supportive_prompt_json_data"] = json.dumps(supportive_prompt_json_data)

        # Serialize and update
        serialized_data = prompt_serializer(instance=obj, data=data, partial=True)
        if serialized_data.is_valid():
            serialized_data.save()
            return JsonResponse({
                "message": "Prompt updated successfully.",
                "success": True,
                "data": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Validation failed.",
                "success": False,
                "errors": serialized_data.errors,
            }, status=400)

    except Exception as e:
        print("This error is update_prompt --->: ", e)
        return JsonResponse({
            "error": "Internal server error.",
            "success": False
        }, status=500)



# delete prompt
@api_view(['DELETE'])
# @workspace_permission_required
@domain_permission_required
def delete_prompt(request, slug_id):
    try:
        request_user = request.user
        try:
            obj = prompt.objects.get(slug_id=slug_id)
        except prompt.DoesNotExist:
            return JsonResponse({
                "error": "prompt not found.",
                "success": False,
            }, status=404) 
   
        workspace_slug_id = request.GET.get("workspace_slug_id")
          
        if not request_user.is_superuser:
            if not workspace_slug_id:
                return JsonResponse({
                    "error": "workspace slug id is required.",
                    "success": False,
                }, status=400)
                
            if (obj.workspace_id.slug_id != workspace_slug_id):
                return JsonResponse({
                    "error": "You Don't have permission.",
                    "success": False,
                }, status=403)

        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_prompt --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)




