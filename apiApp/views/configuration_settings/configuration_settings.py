from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import configuration_settings_serializer
from apiApp.models import configuration_settings
from django.db.models import Q
from loguru import logger
from apiApp.views.base.process_pagination.process_pagination import process_pagination
from django.views.decorators.http import require_GET


# show configuration_settings
@api_view(['GET'])
def list_configuration_settings(request):
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
            obj = configuration_settings.objects.filter(filters).order_by(order_by)
        except configuration_settings.DoesNotExist:
            return JsonResponse({
                "error": "configuration_settings not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)


        serialized_data = configuration_settings_serializer(obj, many=True)

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
        print("This error is list_configuration_settings --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)





@api_view(['POST'])
def add_configuration_settings(request):
    try:
        request_user = request.user
        
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

        # Add created_by field for tracking user who created the configuration
        data['created_by'] = request_user.id

        # Extract config_type and validate it exists
        config_type = data.get('name', '').lower()
        required_keys = configuration_settings.CONFIG_REQUIREMENTS.get(config_type)

        if required_keys is None:
            return JsonResponse({"error": "Invalid config name provided.", "success": False}, status=400)

        # Create a config dictionary from the flattened data
        # For example, convert 'config_count': '1' to {'config': {'count': 1}}
        config_data = {}
        for key in list(data.keys()):
            if key.startswith('config_'):
                # Extract the actual config key (e.g., 'count' from 'config_count')
                config_key = key.replace('config_', '')
                
                # Try to convert numeric values to integers
                value = data[key]
                try:
                    if str(value).isdigit():
                        value = int(value)
                except (ValueError, TypeError):
                    pass
                
                # Add to config dictionary
                config_data[config_key] = value
                
                # Remove the flattened key from data
                del data[key]
        
        # Add the constructed config dictionary to data
        data['config'] = config_data

        # Check for missing required keys in the configuration
        missing_keys = set(required_keys) - set(config_data.keys())
        if missing_keys:
            return JsonResponse({"error": f"Missing required keys: {', '.join(missing_keys)}", "success": False}, status=400)

        # Additional validation for retry configuration (if applicable)
        if config_type == 'retry':
            count = config_data.get('count')
            if not isinstance(count, int) or count < 0:
                return JsonResponse({"error": "RETRY count must be a non-negative integer.", "success": False}, status=400)

        # Serialize the data
        serializer = configuration_settings_serializer(data=data)

        # If serializer is valid, save it to the database
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                "message": "Configuration added successfully.",
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
        print(f"Error in add_configuration_settings: {e}")
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)
        


    
# update configuration_settings
@api_view(['PATCH'])
def update_configuration_settings(request, slug_id):
    try:

        try:
            obj = configuration_settings.objects.get(slug_id=slug_id)
        except configuration_settings.DoesNotExist:
            return JsonResponse({
                "error": "configuration_settings not found.",
                "success": False,
            }, status=404)   

        serialized_data = configuration_settings_serializer(instance=obj, data=request.data, partial=True)        
        
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
        print("This error is update_configuration_settings --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


# delete configuration_settings
@api_view(['DELETE'])
def delete_configuration_settings(request, slug_id):
    try:
        try:
            obj = configuration_settings.objects.get(slug_id=slug_id)
        except configuration_settings.DoesNotExist:
            return JsonResponse({
                "error": "configuration_settings not found.",
                "success": False,
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_configuration_settings --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)







#  get fields
@require_GET
def get_config_field(request):
    return JsonResponse(configuration_settings.CONFIG_REQUIREMENTS)
