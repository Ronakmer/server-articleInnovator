# from functools import wraps
# from django.http import JsonResponse
# from apiApp.models import user_detail, workspace

# def workspace_permission_required(func):
#     @wraps(func)
#     def wrap(request, *args, **kwargs):
#         user = request.user
        
#         print(f"User: {user}, Request Path: {request.path}, Method: {request.method}")
#         print(f"{request.data}")
#         print(f"{request.data['workspace_slug_id']}")
        
        
#         # Determine where to get workspace_slug_id based on the request method
#         if request.method == 'POST' or request.method == 'PUT':
#             if request.content_type == 'application/json':
#                 workspace_slug_id = request.data.get('workspace_slug_id') 
#             else:
#                 workspace_slug_id = request.POST.get('workspace_slug_id')  
#         elif request.method == 'GET':
#             workspace_slug_id = request.GET.get('workspace_slug_id')
#         elif request.method == 'DELETE':
#             workspace_slug_id = request.GET.get('workspace_slug_id')
#             if not workspace_slug_id:  
#                 workspace_slug_id = request.body.decode('utf-8')

#         print(workspace_slug_id, 'workspace_slug_id')
        
#         # is user (admin, user)
#         if workspace_slug_id:
#             # Check if the user has permission to work in the specified workspace by slug_id
#             user_workspaces = user_detail.objects.filter(user_id=user).values_list('workspace_id__slug_id', flat=True)

#             # If the user doesn't have permission to access the workspace, return an error
#             if workspace_slug_id not in user_workspaces:
#                 return JsonResponse({"error": "You do not have permission to perform this action in this workspace."}, status=403)
#         else:
#             # If no slug_id is provided, proceed with the original permission check
#             if not user_detail.objects.filter(user_id=user).exists():
#                 return JsonResponse({"error": "You do not have permission to perform this action."}, status=403)

#         # is super admin
#         if user.is_superuser:
#             return func(request, *args, **kwargs)
                
#         # If the user is in any workspace, proceed with the view function
#         return func(request, *args, **kwargs)
    
#     return wrap





from functools import wraps
from django.http import JsonResponse
from apiApp.models import user_detail, workspace

def workspace_permission_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        user = request.user
        
        # If the user is a superuser, skip the workspace check and proceed with the view
        if user.is_superuser:
            return func(request, *args, **kwargs)
        
        elif not user.is_superuser:
            # print(f"User: {user}, Request Path: {request.path}, Method: {request.method}")
            
            # Extract workspace_slug_id based on request method
            if request.method in ['POST', 'PUT']:
                if request.content_type == 'application/json':
                    workspace_slug_id = request.data.get('workspace_slug_id') 
                else:
                    workspace_slug_id = request.POST.get('workspace_slug_id')  
            elif request.method == 'GET':
                workspace_slug_id = request.GET.get('workspace_slug_id')
            elif request.method == 'DELETE':
                workspace_slug_id = request.GET.get('workspace_slug_id')
                # if not workspace_slug_id:  
                #     workspace_slug_id = request.body.decode('utf-8')

            # full_url = request.build_absolute_uri()
            # temp_workspace_slug_id = full_url.split('/')[-1]
            # print(temp_workspace_slug_id,'temp_workspace_slug_id')
            
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
            print(workspace_slug_id,'workspace_slug_id1')
            
            
            if current_url in permission_url:
                full_url = request.build_absolute_uri()
                print(full_url,'full_url')
                workspace_slug_id = full_url.split('/')[-1]
                print(workspace_slug_id,'workspace_slug_id1')

            print(workspace_slug_id,'workspace_slug_id2')
            # If workspace_slug_id is provided, check if the user is part of the workspace
            if workspace_slug_id:
                
                # Fetch the user's workspaces using the slug_id
                user_workspaces = user_detail.objects.filter(user_id=user).values_list('workspace_id__slug_id', flat=True)
                print(user_workspaces,'user_workspaces')
                # # If the user is not part of the workspace, return an error
                # if workspace_slug_id not in user_workspaces:
                #     return JsonResponse({"error": "You do not have permission to perform this action in this workspace."}, status=403)

                #  for workspace_slug pass list 
                if isinstance(workspace_slug_id, str):
                    workspace_slug_list = workspace_slug_id.split(",")
                else:
                    workspace_slug_list = workspace_slug_id  # If it's already a list, just use it

                print(workspace_slug_list,'workspace_slug_list00000')
                if not any(slug in user_workspaces for slug in workspace_slug_list):
                    return JsonResponse({"error": "You do not have permission to perform this action in this workspace."}, status=403)

            else:
                # If no workspace_slug_id is provided, return an error
                return JsonResponse({"error": "Workspace slug ID is required."}, status=400)
        
        # Continue with the view function if the user is part of the workspace
        return func(request, *args, **kwargs)
    
    return wrap
