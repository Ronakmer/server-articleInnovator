
from functools import wraps
from django.http import JsonResponse
from apiApp.models import user_detail, workspace

def workspace_permission_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        request_user = request.user
        
        # If the user is a superuser, skip the workspace check and proceed with the view
        if request_user.is_superuser:
            return func(request, *args, **kwargs)
        
        elif not request_user.is_superuser:
            # print(f"User: {user}, Request Path: {request.path}, Method: {request.method}")
            
            # Extract workspace_slug_id based on request method
            if request.method in ['POST', 'PATCH']:
                if request.content_type == 'application/json':
                    workspace_slug_id = request.data.get('workspace_slug_id') 
                else:
                    workspace_slug_id = request.POST.get('workspace_slug_id')  
            elif request.method == 'GET':
                workspace_slug_id = request.GET.get('workspace_slug_id')
            elif request.method == 'DELETE':
                workspace_slug_id = request.GET.get('workspace_slug_id')

            
            # Get the function name
            try:
                current_url = request.resolver_match.view_name
            except AttributeError:
                current_url = None
                print("Function name could not be resolved.")
                return JsonResponse({"error": "url resolved."}, status=404)

            permission_url = [
                'update_workspace', 'delete_workspace'
            ]            
            
            if current_url in permission_url:
                full_url = request.build_absolute_uri()
                workspace_slug_id = full_url.split('/')[-1]

            # If workspace_slug_id is provided, check if the user is part of the workspace
            if workspace_slug_id:
                
                #  for workspace_slug pass list 
                if isinstance(workspace_slug_id, str):
                    workspace_slug_list = workspace_slug_id.split(",")
                else:
                    workspace_slug_list = workspace_slug_id  # If it's already a list, just use it

                # Fetch the user's workspaces using the slug_id
                user_workspaces = user_detail.objects.filter(user_id=request_user).values_list('workspace_id__slug_id', flat=True)
                print(user_workspaces,'user_workspaces')

                if not any(slug in user_workspaces for slug in workspace_slug_list):
                    return JsonResponse({"error": "You do not have permission to perform this action in this workspace.","success": False}, status=403)

            else:
                # If no workspace_slug_id is provided, return an error
                return JsonResponse({"error": "Workspace slug ID is required.","success": False}, status=400)
        
        # Continue with the view function if the user is part of the workspace
        return func(request, *args, **kwargs)
    
    return wrap
