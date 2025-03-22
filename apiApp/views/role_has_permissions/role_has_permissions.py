from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import role_serializer, permission_serializer
from apiApp.models import role, permission, role_has_permissions
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import json



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

        return JsonResponse({'status': 'success', 'data': response_data,"success": True}, status=200)

    except Exception as e:
        print(f"Error in list_role_has_permissions: {e}")
        return JsonResponse({'status': 'error',"success": False}, status=500)





@api_view(['PATCH'])
def update_role_has_permissions(request):
    try:
        # Extract role and permissions data from the request
        role_name = request.data.get('role')
        permissions_data = request.data.get('permissions')

        # Ensure permissions_data is not empty
        if not permissions_data:
            return JsonResponse({"status": "error", "error": "Permissions data is required.","success": False}, status=400)

        # Split permissions string and clean up any empty or invalid data
        permissions_ids = permissions_data.split(',')
        permissions_ids = [perm_id.strip() for perm_id in permissions_ids if perm_id.strip()]

        if not permissions_ids:
            return JsonResponse({"status": "error", "error": "No valid permission IDs provided.","success": False}, status=400)

        # Fetch the role instance
        role_instance = role.objects.filter(name=role_name).first()

        if not role_instance:
            return JsonResponse({"status": "error", "error": f"Role not found.","success": False}, status=404)

        # Fetch the permissions based on the slug IDs
        permission_objects = permission.objects.filter(slug_id__in=permissions_ids)

        # Remove existing permissions for the role before adding new ones
        role_has_permissions.objects.filter(role_id=role_instance).delete()

        # Now, add the new associations
        for perm in permission_objects:
            role_has_permissions.objects.create(role_id=role_instance, permission_id=perm)

        return JsonResponse({"status": "success", "error": "Role and permissions added successfully.","success": True}, status=200)

    except Exception as e:
        print(f"Error in update_role_has_permissions: {e}")
        return JsonResponse({"status": "error", "error": "Internal server error.","success": False}, status=500)














@api_view(['POST'])
def add_role_has_permissions(request):
    try:
        # Get the data from request
        data = request.data
        print("Received data:", data)
        
        # Validate the data
        if not isinstance(data, list):
            return JsonResponse({"error": "Request data should be a list of role-permission mappings.","success": False}, status=400)
        
        if not data:
            return JsonResponse({"error": "Role-permission data is required.","success": False}, status=400)
        
        # Track changes for response
        created = 0
        updated = 0
        deleted = 0
        
        for item in data:
            print("Processing item:", item)
            
            # Validate each item in the list
            if not isinstance(item, dict):
                return JsonResponse({"error": "Each item should be a dictionary.","success": False}, status=400)
            
            role_name = item.get('role')
            permissions_str = item.get('permissions')
            
            print(f"Role: {role_name}")
            print(f"Permissions string: {permissions_str}")
            
            # Validate required fields
            if not role_name:
                return JsonResponse({"error": "Role name is missing in one of the items.","success": False}, status=400)
            if not permissions_str:
                return JsonResponse({"error": "Permissions are missing in one of the items.","success": False}, status=400)
            
            # Get the role instance
            role_instance = role.objects.filter(name=role_name.lower()).first()
            if not role_instance:
                return JsonResponse({"error": f"Role '{role_name}' not found.","success": False}, status=404)
            
            # Split the permissions string and clean up
            permission_ids = [p.strip() for p in permissions_str.split(',')]
            print(f"Permission IDs after splitting: {permission_ids}")
            
            # Get existing permissions for this role
            existing_mappings = role_has_permissions.objects.filter(role_id=role_instance)
            existing_permission_ids = [str(mapping.permission_id.slug_id) for mapping in existing_mappings]
            print(f"Existing permission IDs: {existing_permission_ids}")
            
            # Determine permissions to add and remove
            to_add = [pid for pid in permission_ids if pid and pid not in existing_permission_ids]
            to_remove = [pid for pid in existing_permission_ids if pid not in permission_ids]
            
            print(f"Permissions to add: {to_add}")
            print(f"Permissions to remove: {to_remove}")
            
            # Add new permissions
            for pid in to_add:
                permission_instance = permission.objects.filter(slug_id=pid).first()
                if permission_instance:
                    role_has_permissions.objects.create(
                        role_id=role_instance,
                        permission_id=permission_instance
                    )
                    created += 1
                    print(f"Added permission {pid} to role {role_name}")
                else:
                    print(f"Warning: Permission {pid} not found, skipping")
            
            # Remove old permissions
            for pid in to_remove:
                deleted_count = role_has_permissions.objects.filter(
                    role_id=role_instance,
                    permission_id__slug_id=pid
                ).delete()[0]
                deleted += deleted_count
                print(f"Removed {deleted_count} permission(s) with ID {pid} from role {role_name}")
        
        return JsonResponse({
            "message": "Role permissions processed successfully.",
            "created": created,
            "updated": updated,
            "deleted": deleted,
            "success": True,
        }, status=200)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in add_role_has_permissions: {str(e)}")
        return JsonResponse({"error": "Internal server error","success": False}, status=500)