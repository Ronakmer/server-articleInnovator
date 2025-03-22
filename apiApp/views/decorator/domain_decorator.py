from functools import wraps
from django.http import JsonResponse
from apiApp.models import user_detail, domain, role, role_has_permissions, permission

def domain_permission_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        request_user = request.user
        
        print('---------- Checking domain permission -----------------')
        print(f"User: {request_user}, Request Path: {request.path}, Method: {request.method}")
        
        # If the user is a superuser, skip the domain check and proceed with the view
        if request_user.is_superuser:
            return func(request, *args, **kwargs)
        
        elif not request_user.is_superuser:

            current_page = request.path.strip('/').rsplit('/', 1)[0] 
            print(current_page,'current_page')
                
            # Get the function name
            try:
                current_url = request.resolver_match.view_name
                print(current_url, 'current_url')
            except AttributeError:
                current_url = None
                print("Function name could not be resolved.")


            # Extract domain_slug_id based on request method
            if request.method in ['POST', 'PATCH']:
                if request.content_type == 'application/json':
                    domain_slug_id = request.data.get('domain_slug_id') 
                else:
                    domain_slug_id = request.POST.get('domain_slug_id')  
            elif request.method == 'GET':
                domain_slug_id = request.GET.get('domain_slug_id')
            elif request.method == 'DELETE':
                domain_slug_id = request.GET.get('domain_slug_id')

            # Check if the user is associated with any domain
            user_details = user_detail.objects.get(user_id=request_user)
            if user_details.role_id.name == 'admin':
                print(f"Granted: User {request_user} is an admin. Skipping domain check.")
                return func(request, *args, **kwargs)


            try:
                domain_obj = domain.objects.get(slug_id = domain_slug_id)
            except domain.DoesNotExist:
                return JsonResponse({
                    "error": "domain not found.",
                    "success": False,
                }, status=404)
                
            # Check if user has access to workspace
            workspace_obj = domain_obj.workspace_id
            if not workspace_obj:
                return JsonResponse({"error": "Workspace not associated with domain","success": False}, status=400)

            if not user_details.workspace_id.filter(id=workspace_obj.id).exists():
                return JsonResponse({"error": "User does not have access to this workspace","success": False}, status=403)

                   
            request.is_manager = False
            request.is_writer = False
            role_name = None

            # Check if the request_user is a manager or writer of the domain
            if domain_obj.manager_id.filter(user_id=request_user).exists():
                _ = domain_obj.manager_id.get(user_id=request_user)
                role_name = 'manager'
                request.is_manager = True
  
            elif domain_obj.writer_id.filter(user_id=request_user).exists():
                _ = domain_obj.writer_id.get(user_id=request_user)
                role_name = 'writer'
                request.is_writer = True
            
           
            # print(role_name)
            if role_name == 'manager':
                print(current_url,'current_url')
              
                role_obj = role.objects.get(name='manager')
            
                # Get all permissions assigned to the role
                role_permissions = role_has_permissions.objects.filter(role_id=role_obj)
                permission_url = role_permissions.values_list('permission_id__name', flat=True)

                if current_url in permission_url:
                    print("Permission granted for this URL.")
                    return func(request, *args, **kwargs)


            if role_name == 'writer':
               
                print(current_url,'current_url')
                role_obj = role.objects.get(name='writer')
            
                # Get all permissions assigned to the role
                role_permissions = role_has_permissions.objects.filter(role_id=role_obj)
                permission_url = role_permissions.values_list('permission_id__name', flat=True)

                if current_url in permission_url:
                    print("Permission granted for this URL.")
                    return func(request, *args, **kwargs)
                
        # Default response if no conditions are met
        return JsonResponse({"error": "Permission denied or invalid request.","success": False}, status=403)
                

    return wrap
