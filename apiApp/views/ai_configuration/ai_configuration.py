from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import ai_configuration_serializer
from apiApp.models import ai_configuration, workspace
from django.db.models import Q
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from apiApp.views.base.process_pagination.process_pagination import process_pagination

from apiApp.views.ai_rate_limiter_api.add_provider_key_api.add_provider_key_api import add_provider_key_api
from apiApp.views.ai_rate_limiter_api.delete_provider_key_api.delete_provider_key_api import delete_provider_key_api



# show ai configuration
@api_view(['GET'])
@workspace_permission_required
def list_ai_configuration(request):
    try:
        request_user = request.user
        
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        api_provider = request.GET.get('api_provider', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')

        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if api_provider:
            filters &= Q(api_provider=api_provider)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(email__icontains=search) 

        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id=workspace_obj.id)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found",
                    "success": False,
                }, status=404)
                
                
        if request_user.is_superuser:       
            obj = ai_configuration.objects.filter(filters).order_by(order_by)
        if request.is_admin:
            obj = ai_configuration.objects.filter(filters).order_by(order_by)
        
        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        print(obj,'obj')

        serialized_data = ai_configuration_serializer(obj, many=True)
        
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
        print("This error is list_ai_configuration --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# # add ai configuration
# @api_view(['POST'])
# @workspace_permission_required
# def add_ai_configuration(request):
#     try:
#         request_user = request.user

#         # Retrieve workspace using slug ID
#         workspace_slug_id = request.data.get("workspace_slug_id")  
#         if not workspace_slug_id:
#             return JsonResponse({
#                 "error": "workspace slug id is required.",
#                 "success": False,
#             }, status=400)
#         print(workspace_slug_id,'workspace_slug_id') 
        
#         try:
#             workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
#         except workspace.DoesNotExist:
#             return JsonResponse({
#                 "error": "workspace not found ",
#                 "success": False,
#             }, status=404)

#         # Prepare the data for the serializer, replacing slug with the workspace instance's PK
#         data = request.data.copy()
#         data["workspace_id"] = workspace_obj.id
#         data["created_by"] = request_user.id  

#         serialized_data = ai_configuration_serializer(data=data)
        
#         if serialized_data.is_valid():

#             serialized_data.save()

#             return JsonResponse({
#                 "message": "Data added successfully.",
#                 "success": True,
#                 "data": serialized_data.data,
#             }, status=200)
#         else:
#             return JsonResponse({
#                 "error": "Invalid data.",
#                 "success": False,
#                 "errors": serialized_data.errors,
#             }, status=400)

#     except Exception as e:
#         print("This error is add_ai_configuration --->: ", e)
#         return JsonResponse({"error": "Internal server error.","success": False}, status=500)


    
    
@api_view(['POST'])
@workspace_permission_required
def add_ai_configuration(request):
    try:
        request_user = request.user

        # Retrieve workspace slugs (handle multiple)
        workspace_slugs = request.data.get("workspace_slug_id")
        if not workspace_slugs:
            return JsonResponse({
                "error": "Workspace slug ID(s) are required.",
                "success": False,
            }, status=400)

        ai_models = request.data.get("api_model")
        print(ai_models,'00000000000000000000')
        # Convert string to a list if not already a list
        if isinstance(workspace_slugs, str):
            workspace_slugs = workspace_slugs.split(",")

        # Get all workspace objects
        workspace_objs = workspace.objects.filter(slug_id__in=workspace_slugs)
        if workspace_objs.count() != len(workspace_slugs):
            return JsonResponse({
                "error": "One or more workspace(s) not found.",
                "success": False,
            }, status=404)

        created_data = []
        errors = []

        for workspace_obj in workspace_objs:
            if isinstance(ai_models, str):
                ai_models = ai_models.split(",")  # Convert "s,s" to ["s", "s"]
            print(ai_models,'111111111111111111111111')
            for ai_model in ai_models:
                print(ai_model,'22222222222222222222222222')
                
                data = request.data.copy()
                data["workspace_id"] = workspace_obj.id
                data["created_by"] = request_user.id
                data["api_model"] = ai_model  # Store a single model per entry

                # Add provider key
                provider_response = add_provider_key_api(workspace_obj.slug_id, data)

                # Extract key_id if available
                if isinstance(provider_response, tuple):
                    provider_response = provider_response[0]  # Assuming key_id is the first item

                key_id = provider_response.get("key_id") if isinstance(provider_response, dict) else None
                if key_id:
                    data["ai_rate_key_id"] = key_id  # Save key_id in the database


                # Serialize and save
                serialized_data = ai_configuration_serializer(data=data)
                if serialized_data.is_valid():
                    serialized_data.save()
                    created_data.append(serialized_data.data)
                else:
                    errors.append(serialized_data.errors)

        if errors:
            return JsonResponse({
                "error": "Some configurations failed to add.",
                "success": False,
                "errors": errors,
                "data": created_data,
            }, status=400)

        return JsonResponse({
            "message": "All AI configurations added successfully.",
            "success": True,
            "data": created_data,
        }, status=201)

    except Exception as e:
        print(f"Error in add_ai_configuration: {e}")
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)

    
    
    
    
# update ai configuration
@api_view(['PATCH'])
@workspace_permission_required
def update_ai_configuration(request, slug_id):
    try:

        try:
            obj = ai_configuration.objects.get(slug_id=slug_id)
        except ai_configuration.DoesNotExist:
            return JsonResponse({
                "error": "ai configuration not found.",
                "success": False,
            }, status=404)   

        # Retrieve workspace using slug ID
        workspace_slug_id = request.data.get("workspace_slug_id")  
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace slug id is required.",
                "success": False,
            }, status=400)

        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission.",
                "success": False,
            }, status=404)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found ",
                "success": False,
            }, status=404)

        # Prepare the data for the serializer, replacing slug with the workspace instance's PK
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id 
        data['created_by'] = obj.created_by.id

        serialized_data = ai_configuration_serializer(instance=obj, data=data, partial=True)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "success": True,
                "data": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is update_ai_configuration --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# @api_view(['PATCH'])
# @workspace_permission_required
# def update_ai_configuration(request, slug_id):
#     try:
#         # Retrieve AI Configuration instance
#         try:
#             obj = ai_configuration.objects.get(slug_id=slug_id)
#         except ai_configuration.DoesNotExist:
#             return JsonResponse({
#                 "error": "AI configuration not found.",
#                 "success": False,
#             }, status=404)

#         # Retrieve workspace slug(s)
#         workspace_slugs = request.data.get("workspace_slug_id")
#         if not workspace_slugs:
#             return JsonResponse({
#                 "error": "Workspace slug ID(s) are required.",
#                 "success": False,
#             }, status=400)

#         # Convert to list if single value
#         if isinstance(workspace_slugs, str):
#             workspace_slugs = workspace_slugs.split(",")

#         # Get workspace objects
#         workspace_objs = workspace.objects.filter(slug_id__in=workspace_slugs)
#         if workspace_objs.count() != len(workspace_slugs):
#             return JsonResponse({
#                 "error": "One or more workspace(s) not found.",
#                 "success": False,
#             }, status=404)

#         # Check if user has permission to modify this AI Configuration
#         if obj.workspace_id.slug_id not in workspace_slugs:
#             return JsonResponse({
#                 "error": "You don't have permission to update this AI configuration.",
#                 "success": False,
#             }, status=403)

#         # Prepare update data
#         data = request.data.copy()
#         data["workspace_id"] = obj.workspace_id.id  # Keep the same workspace
#         data["created_by"] = obj.created_by.id  # Maintain original creator

#         serialized_data = ai_configuration_serializer(instance=obj, data=data, partial=True)

#         if serialized_data.is_valid():
#             serialized_data.save()
#             return JsonResponse({
#                 "message": "AI configuration updated successfully.",
#                 "success": True,
#                 "data": serialized_data.data,
#             }, status=200)
#         else:
#             return JsonResponse({
#                 "error": "Invalid data.",
#                 "errors": serialized_data.errors,
#                 "success": False,
#             }, status=400)

#     except Exception as e:
#         print(f"Error in update_ai_configuration: {e}")
#         return JsonResponse({"error": "Internal server error.", "success": False}, status=500)



# delete ai configuration
@api_view(['DELETE'])
@workspace_permission_required
def delete_ai_configuration(request, slug_id):
    try:
        try:
            obj = ai_configuration.objects.get(slug_id=slug_id)
        except ai_configuration.DoesNotExist:
            return JsonResponse({
                "error": "ai configuration not found.",
                "success": False,
            }, status=404) 
                
        workspace_slug_id = request.GET.get("workspace_slug_id")  
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
        
        workspace_id = obj.workspace_id.slug_id
        key_id = obj.ai_rate_key_id
        
        delete_response, delete_error = delete_provider_key_api(workspace_id, key_id)

        if delete_error or not delete_response or delete_response.get('status') != 'success':
            return JsonResponse({
                "error": f"Failed to delete ai configuration via API. {delete_error or delete_response}",
                "success": False,
            }, status=400)
        
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_ai_configuration --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

