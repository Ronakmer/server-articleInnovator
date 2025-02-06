from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import ai_configuration_serializer
from apiApp.models import ai_configuration, workspace
from django.db.models import Q
from apiApp.views.decorator.workspace_decorator import workspace_permission_required



# show ai configuration
@api_view(['GET'])
@workspace_permission_required
def list_ai_configuration(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        api_provider = request.GET.get('api_provider', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')

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
                    "error": "workspace not found"
                }, status=404)

        request_user = request.user
        
        if request_user.is_superuser:       
            obj = ai_configuration.objects.filter(filters).order_by('-created_date')
        else:
            obj = ai_configuration.objects.filter(filters, created_by=request_user).order_by('-created_date')
        
        # Apply pagination
        total_count = obj.count()
        
        obj = obj[offset:offset + limit]


        serialized_data = ai_configuration_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "ai_configurations":serialized_data.data,
            "total_count":total_count,
            
        }, status=200)

    except Exception as e:
        print("This error is list_ai_configuration --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)




# add ai configuration
@api_view(['POST'])
@workspace_permission_required
def add_ai_configuration(request):
    try:
        request_user = request.user

        # Retrieve workspace using slug ID
        workspace_slug_id = request.data.get("workspace_slug_id")  
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace slug id is required."
            }, status=400)
        # print(workspace_slug_id,'workspace_slug_id') 
        
        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found "
            }, status=404)

        # Prepare the data for the serializer, replacing slug with the workspace instance's PK
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id
        data["created_by"] = request_user.id  

        serialized_data = ai_configuration_serializer(data=data)
        
        if serialized_data.is_valid():

            serialized_data.save()

            return JsonResponse({
                "message": "Data added successfully.",
                "ai_configuration": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors,
            }, status=400)

    except Exception as e:
        print("This error is add_ai_configuration --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update ai configuration
@api_view(['PUT'])
@workspace_permission_required
def update_ai_configuration(request, slug_id):
    try:

        try:
            obj = ai_configuration.objects.get(slug_id=slug_id)
        except ai_configuration.DoesNotExist:
            return JsonResponse({
                "error": "ai configuration not found.",
            }, status=404)   

        # Retrieve workspace using slug ID
        workspace_slug_id = request.data.get("workspace_slug_id")  
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace slug id is required."
            }, status=400)

        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found "
            }, status=404)

        # Prepare the data for the serializer, replacing slug with the workspace instance's PK
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id 
        data['created_by'] = obj.created_by.id
        # if 'created_by' in data:
        #     del data['created_by']

        serialized_data = ai_configuration_serializer(instance=obj, data=data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "ai_configuration": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_ai_configuration --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


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
            }, status=404) 
                
        workspace_slug_id = request.GET.get("workspace_slug_id")  
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace slug id is required."
            }, status=400)
            
        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)
            
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_ai_configuration --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

