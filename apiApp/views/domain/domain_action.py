from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_detail_serializer
from apiApp.models import user_detail, role, workspace, domain
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from django.db.models import Q




# revoke domain from user
@api_view(['POST'])
@workspace_permission_required
def revoke_domain_from_user(request, slug_id):
    try:
        request_user = request.user 
        workspace_slug_id = request.POST.get('workspace_slug_id')
        domain_slug_id = request.POST.get('domain_slug_id')
        role_type = request.POST.get('role_type')
        
        try:
            user_detail_obj = user_detail.objects.get(slug_id = slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "user detail not found.",
            }, status=404) 

        if not (workspace_slug_id):
            return JsonResponse({"error": "workspace slug required fields."}, status=400)
        
        if not (domain_slug_id):
            return JsonResponse({"error": "domain slug required fields."}, status=400)

        if not user_detail_obj.workspace_id.filter(slug_id=workspace_slug_id).exists():
            return JsonResponse({
                "error": "You don't have permission."
            }, status=403)

        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            if role_type == 'manager':
                domain_obj.manager_id.remove(user_detail_obj)
            elif role_type == 'writer':
                domain_obj.writer_id.remove(user_detail_obj)

        except domain.DoesNotExist:
            return JsonResponse({
                "error": "domain detail not found.",
            }, status=404) 

        return JsonResponse({
            "message": "Data revoke successfully.",
            # "user_detail": serialized_user_data,
        }, status=200)

    except Exception as e:
        print("This error is revoke_domain_from_user --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)
    

    
    
    
# add domain to user
@api_view(['POST'])
@workspace_permission_required
def add_domain_to_user(request, slug_id):
    try:
 
        workspace_slug_id = request.POST.get('workspace_slug_id')
        domain_slug_id = request.POST.get('domain_slug_id')
        role_type = request.POST.get('role_type')

        try:
            user_detail_obj = user_detail.objects.get(slug_id = slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "user detail not found.",
            }, status=404) 
            
        if not (workspace_slug_id):
            return JsonResponse({"error": "workspace slug required fields."}, status=400)
        if not (domain_slug_id):
            return JsonResponse({"error": "domain slug required fields."}, status=400)
        if not (role_type):
            return JsonResponse({"error": "role type required fields."}, status=400)

        try:
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "workspce detail not found.",
            }, status=404) 

        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            if role_type == 'manager':
                domain_obj.manager_id.add(user_detail_obj)
            elif role_type == 'writer':
                domain_obj.writer_id.add(user_detail_obj)
            domain_obj.workspace_id = workspace_obj
            domain_obj.save()
    
        except domain.DoesNotExist:
            return JsonResponse({
                "error": "domain detail not found.",
            }, status=404) 

        return JsonResponse({
            "message": "Data add successfully.",
            # "user_detail": serialized_user_data,
        }, status=200)

    except Exception as e:
        print("This error is add_domain_to_user --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)
    