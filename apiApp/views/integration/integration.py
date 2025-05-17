from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import integration_serializer
from apiApp.models import integration, integration_type
from django.db.models import Q
from loguru import logger
from apiApp.views.base.process_pagination.process_pagination import process_pagination
from django.views.decorators.http import require_GET


# show integration
@api_view(['GET'])
def list_integration(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        
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
            obj = integration.objects.filter(filters).order_by(order_by)
        except integration.DoesNotExist:
            return JsonResponse({
                "error": "integration not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)


        serialized_data = integration_serializer(obj, many=True)

        logger.info("This is an info log message", extra={"notify": True, "status_code": 200, "workspace_slug_id": '77b4ad49-db8a-4434-aad5-c2351c953cc7', "url":request.path, "request_user": request.user, "domain_slug_id":'ec676a34-eb18-4610-b1b8-99ba7d26d87a', "user_status":True })

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
        print("This error is list_integration --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)





@api_view(['POST'])
def add_integration(request):
    try:
        request_user = request.user
        print(request.data,'request.datasss')
        # Check if data is provided in the request
        if not request.data:
            return JsonResponse({"error": "No data provided in request.", "success": False}, status=400)

        # Extract data from the request as a dictionary
        # For QueryDict, we need to properly handle the list values
        data = {}
        for key, value_list in request.data.items():
            # Most likely we want the first value if it's a list
            if isinstance(value_list, list) and value_list:
                data[key] = value_list[0]
            else:
                data[key] = value_list

        # Extract config_type and validate it exists
        integration_type_name = data.get('integration_type', '').lower()
        # required_keys = integration.CONFIG_REQUIREMENTS.get(integration_type)

        try:
            integration_type_obj = integration_type.objects.get(name__iexact=integration_type_name)
        except integration_type.DoesNotExist:
            return JsonResponse({"error": "Invalid integration type name.", "success": False}, status=400)


        required_fields = integration_type_obj.integration_field or []
        integration_json_data = {}

        # Build integration_json_data from fields starting with 'integration_'
        for key in list(data.keys()):
            if key.startswith('integration_'):
                field_key = key.replace('integration_', '')
                integration_json_data[field_key] = data[key]

        print(integration_json_data,'integration_json_dataxx')

        # Validate required keys
        # missing_keys = set(required_fields) - set(integration_json_data.keys())
        # if missing_keys:
        #     return JsonResponse({"error": f"Missing required keys: {', '.join(missing_keys)}", "success": False}, status=400)
        
        
        # Add the constructed config dictionary to data
        data['integration_type_id'] = integration_type_obj.id
        data['integration_json_data'] = integration_json_data
        data['created_by'] = request_user.id


        # Serialize the data
        serializer = integration_serializer(data=data)

        # If serializer is valid, save it to the database
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                "message": "Integration added successfully.",
                "data": serializer.data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serializer.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        # Handle unexpected errors
        print(f"Error in add_integration: {e}")
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)
        


@api_view(['PATCH'])
def update_integration(request, slug_id):
    try:
        request_user = request.user
        print(request.data, 'request.data for update')

        # Try to get the integration object
        try:
            obj = integration.objects.get(slug_id=slug_id)
        except integration.DoesNotExist:
            return JsonResponse({"error": "Integration not found.", "success": False}, status=404)

        status = request.data.get("status")
        if status is not None and status != "":
            serialized_data = integration_serializer(instance=obj, data=request.data, partial=True)
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
                

        # Check if data is provided in the request
        if not request.data:
            return JsonResponse({"error": "No data provided in request.", "success": False}, status=400)


        # Extract data from the request
        data = {}
        for key, value_list in request.data.items():
            if isinstance(value_list, list) and value_list:
                data[key] = value_list[0]
            else:
                data[key] = value_list

        # Get the integration type
        integration_type_name = data.get('integration_type', '').lower()
        try:
            integration_type_obj = integration_type.objects.get(name__iexact=integration_type_name)
        except integration_type.DoesNotExist:
            return JsonResponse({"error": "Invalid integration type name.", "success": False}, status=400)

        required_fields = integration_type_obj.integration_field or []
        integration_json_data = {}

        # Build integration_json_data from fields starting with 'integration_'
        for key in list(data.keys()):
            if key.startswith('integration_'):
                field_key = key.replace('integration_', '')
                integration_json_data[field_key] = data[key]

        print(integration_json_data, 'integration_json_data for update')

        # Add necessary fields to data
        data['integration_type_id'] = integration_type_obj.id
        data['integration_json_data'] = integration_json_data
        # data['updated_by'] = request_user.id

        # Serialize and update the object
        serializer = integration_serializer(instance=obj, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "message": "Integration updated successfully.",
                "data": serializer.data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serializer.errors,
                "success": False,
            }, status=400)

    except Exception as e:
        print(f"Error in update_integration: {e}")
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)


# delete integration
@api_view(['DELETE'])
def delete_integration(request, slug_id):
    try:
        try:
            obj = integration.objects.get(slug_id=slug_id)
        except integration.DoesNotExist:
            return JsonResponse({
                "error": "integration not found.",
                "success": False,
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_integration --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)







#  get fields
@require_GET
def get_integration_field(request):
    request_user = request.user
    integration_fields = []

    if request_user.is_superuser:
        permission_filter = 'superadmin'
    elif request_user.is_admin:
        permission_filter = 'admin'

    print(permission_filter,'permission_filterx')
    # Filter integrations based on permission_choice
    integration_types_obj = integration_type.objects.filter(
        permission_choice=permission_filter
    )
    
    print(integration_types_obj,'integration_types_objx')

    if not integration_types_obj:
        return JsonResponse({'error': f'integrations not found'}, status=404)

    result = {}
    for type_obj in integration_types_obj:
        if type_obj.integration_field:
            result[type_obj.name] = type_obj.integration_field
    
    # If no fields found in any integration type
    if not result:
        return JsonResponse({}, safe=False)
        
    return JsonResponse(result, safe=False)









