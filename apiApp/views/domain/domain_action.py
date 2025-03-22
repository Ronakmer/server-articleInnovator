from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_detail_serializer, domain_serializer
from apiApp.models import user_detail, role, workspace, domain
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from django.db.models import Q





# revoke domain from user
@api_view(['GET'])
@workspace_permission_required
def list_revoke_domain_from_user(request, slug_id):
    try:
        request_user = request.user 
        workspace_slug_id = request.GET.get('workspace_slug_id')
        # domain_slug_id = request.POST.get('domain_slug_id')
        
        try:
            user_detail_obj = user_detail.objects.get(slug_id = slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "user detail not found.",
                "success": False,
            }, status=404) 

        if not (workspace_slug_id):
            return JsonResponse({"error": "workspace slug required fields.","success": False}, status=400)
        
        if not user_detail_obj.workspace_id.filter(slug_id=workspace_slug_id).exists():
            return JsonResponse({
                "error": "You don't have permission."
            }, status=403)

        try:
            obj = domain.objects.filter(Q(manager_id=user_detail_obj) | Q(writer_id=user_detail_obj)).distinct()
        except domain.DoesNotExist:
            return JsonResponse({
                "error": "domain detail not found.",
                "success": False,
            }, status=404) 

        serialized_data = domain_serializer(obj, many=True)

        return JsonResponse({
            "message": "Data revoke successfully.",
            "success": True,
            "data": serialized_data.data,
        }, status=200)

    except Exception as e:
        print("This error is list_revoke_domain_from_user --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)
    

    

# revoke domain from user
@api_view(['POST'])
@workspace_permission_required
def revoke_domain_from_user(request, slug_id):
    try:
        request_user = request.user 
        workspace_slug_id = request.data.get('workspace_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        role_type = request.data.get('role_type')
        
        try:
            user_detail_obj = user_detail.objects.get(slug_id = slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "user detail not found.",
                "success": False,
            }, status=404) 

        if not (workspace_slug_id):
            return JsonResponse({"error": "workspace slug required fields.","success": False}, status=400)
        
        if not (domain_slug_id):
            return JsonResponse({"error": "domain slug required fields.","success": False}, status=400)

        if not user_detail_obj.workspace_id.filter(slug_id=workspace_slug_id).exists():
            return JsonResponse({
                "error": "You don't have permission.",
                "success": False,
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
                "success": False,
            }, status=404) 

        return JsonResponse({
            "message": "Data revoke successfully.",
            # "user_detail": serialized_user_data,
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is revoke_domain_from_user --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)
    

    
    
    
# add domain to user
@api_view(['POST'])
@workspace_permission_required
def add_domain_to_user(request):
    try:
        workspace_slug_id = request.data.get('workspace_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        role_type = request.data.get('role_type')
        slug_id = request.data.get('slug_id')

        try:
            user_detail_obj = user_detail.objects.get(slug_id = slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "user detail not found.",
                "success": False,
            }, status=404) 
            
        if not (workspace_slug_id):
            return JsonResponse({"error": "workspace slug required fields.","success": False}, status=400)
        if not (domain_slug_id):
            return JsonResponse({"error": "domain slug required fields.","success": False}, status=400)
        if not (role_type):
            return JsonResponse({"error": "role type required fields.","success": False}, status=400)

        try:
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
        except user_detail.DoesNotExist:
            return JsonResponse({
                "error": "workspce detail not found.",
                "success": False,
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
                "success": False,
            }, status=404) 

        return JsonResponse({
            "message": "Data add successfully.",
            "success": True,
            # "user_detail": serialized_user_data,
        }, status=200)

    except Exception as e:
        print("This error is add_domain_to_user --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)
    