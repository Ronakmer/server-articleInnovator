from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import role_serializer, permission_serializer
from apiApp.models import role, permission, role_has_permissions


@api_view(['GET'])
def list_role_has_permissions(request):
    try:
        # Fetch all permissions and roles
        permissions = permission.objects.all()
        roles = role.objects.all()

        role_permissions_map = {}

        # Map each role to its associated permission objects
        for role_instance in roles:
            # Get permission IDs associated with the role
            permission_ids = role_has_permissions.objects.filter(role_id=role_instance.id).values_list('permission_id', flat=True)
            # Fetch permission objects for the IDs
            permission_objects = permission.objects.filter(id__in=permission_ids)
            role_permissions_map[role_instance.name] = permission_objects

        # Group permissions by 'group' field if it exists
        grouped_permissions = {}
        for perm in permissions:
            group_key = perm.group if hasattr(perm, 'group') and perm.group else 'ungrouped'
            if group_key not in grouped_permissions:
                grouped_permissions[group_key] = []
            grouped_permissions[group_key].append({
                'slug_id': perm.slug_id,
                'name': perm.name
            })

        # Build the response data
        response_data = {
            'roles': [
                {
                    'name': role_instance.name,
                    'slug_id': role_instance.slug_id,  # Use slug_id for roles
                    'permissions': [
                        {
                            'name': perm.name,
                            'slug_id': perm.slug_id,  # Use slug_id for permissions
                            'status': True
                        }
                        for perm in role_permissions_map.get(role_instance.name, [])
                    ]
                }
                for role_instance in roles
            ],
            'grouped_permissions': grouped_permissions
        }

        return JsonResponse({'status': 'success', 'data': response_data}, status=200)

    except Exception as e:
        print(f"Error in list_role_has_permissions: {e}")
        return JsonResponse({'status': 'error'}, status=500)





@api_view(['POST'])
def add_role_has_permissions(request):
    try:
        # Extract role and permissions data from the request
        role_name = request.data.get('role')
        permissions_data = request.data.get('permissions')

        # Ensure permissions_data is not empty
        if not permissions_data:
            return JsonResponse({"status": "error", "message": "Permissions data is required."}, status=400)

        # Split permissions string and clean up any empty or invalid data
        permissions_ids = permissions_data.split(',')
        permissions_ids = [perm_id.strip() for perm_id in permissions_ids if perm_id.strip()]

        if not permissions_ids:
            return JsonResponse({"status": "error", "message": "No valid permission IDs provided."}, status=400)

        # Fetch the role instance
        role_instance = role.objects.filter(name=role_name).first()

        if not role_instance:
            return JsonResponse({"status": "error", "message": f"Role not found."}, status=404)

        # Fetch the permissions based on the slug IDs
        permission_objects = permission.objects.filter(slug_id__in=permissions_ids)


        # Now, add the new associations
        for perm in permission_objects:
            role_has_permissions.objects.create(role_id=role_instance, permission_id=perm)

        return JsonResponse({"status": "success", "message": "Role and permissions added successfully."}, status=200)

    except Exception as e:
        print(f"Error in add_role_has_permissions: {e}")
        return JsonResponse({"status": "error", "message": "Internal server error."}, status=500)



@api_view(['PUT'])
def update_role_has_permissions(request):
    try:
        # Extract role and permissions data from the request
        role_name = request.data.get('role')
        permissions_data = request.data.get('permissions')

        # Ensure permissions_data is not empty
        if not permissions_data:
            return JsonResponse({"status": "error", "message": "Permissions data is required."}, status=400)

        # Split permissions string and clean up any empty or invalid data
        permissions_ids = permissions_data.split(',')
        permissions_ids = [perm_id.strip() for perm_id in permissions_ids if perm_id.strip()]

        if not permissions_ids:
            return JsonResponse({"status": "error", "message": "No valid permission IDs provided."}, status=400)

        # Fetch the role instance
        role_instance = role.objects.filter(name=role_name).first()

        if not role_instance:
            return JsonResponse({"status": "error", "message": f"Role not found."}, status=404)

        # Fetch the permissions based on the slug IDs
        permission_objects = permission.objects.filter(slug_id__in=permissions_ids)

        # Remove existing permissions for the role before adding new ones
        role_has_permissions.objects.filter(role_id=role_instance).delete()

        # Now, add the new associations
        for perm in permission_objects:
            role_has_permissions.objects.create(role_id=role_instance, permission_id=perm)

        return JsonResponse({"status": "success", "message": "Role and permissions added successfully."}, status=200)

    except Exception as e:
        print(f"Error in update_role_has_permissions: {e}")
        return JsonResponse({"status": "error", "message": "Internal server error."}, status=500)

