from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_detail_serializer
from apiApp.models import user_detail, role, workspace
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from django.db.models import Q




# revoke workspace from user
@api_view(['POST'])
@workspace_permission_required
def revoke_workspace_from_user(request, slug_id):
    try:
        request_user = request.user 
        workspace_slug_id = request.POST.get('workspace_slug_id')
        
        try:
            user_detail_obj = user_detail.objects.get(slug_id = slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "user detail not found.",
            }, status=404) 

        if not (workspace_slug_id):
            return JsonResponse({"error": "workspace slug required fields."}, status=400)

        if not user_detail_obj.workspace_id.filter(slug_id=workspace_slug_id).exists():
            return JsonResponse({
                "error": "You don't have permission."
            }, status=403)

        try:
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            user_detail_obj.workspace_id.remove(workspace_obj)
        except workspace.DoesNotExist:
            # print("Workspace not found")
            return JsonResponse({
                "error": "workspace detail not found.",
            }, status=404)

        return JsonResponse({
            "message": "Data revoke successfully.",
            # "user_detail": serialized_user_data,
        }, status=200)

    except Exception as e:
        print("This error is revoke_workspace_from_user --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)
    
    
    
    
# add workspace to user
@api_view(['POST'])
@workspace_permission_required
def add_workspace_to_user(request, slug_id):
    try:
        request_user = request.user 
        workspace_slug_id = request.POST.get('workspace_slug_id')
        
        try:
            user_detail_obj = user_detail.objects.get(slug_id = slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "user detail not found.",
            }, status=404) 
            
        if not (workspace_slug_id):
            return JsonResponse({"error": "workspace slug required fields."}, status=400)

        try:
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            user_detail_obj.workspace_id.add(workspace_obj)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace detail not found.",
            }, status=404) 

        return JsonResponse({
            "message": "Data add successfully.",
            # "user_detail": serialized_user_data,
        }, status=200)

    except Exception as e:
        print("This error is add_workspace_to_user --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)
    