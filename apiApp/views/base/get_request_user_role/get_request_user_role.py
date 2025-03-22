from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.models import user_detail, domain
from django.db.models import Q
from loguru import logger
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show role
@api_view(['GET'])
def get_request_user_role(request):
    try:
        request_user = request.user

        domain_slug_id = request.GET.get('domain_slug_id')

        role_name = "superuser" if request_user.is_superuser else ""    

        user_details = user_detail.objects.get(user_id=request_user)
        if user_details.role_id.name == 'admin':
            role_name = 'admin'

        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({
                "error": "domain not found.",
                "success": False,
            }, status=404)
            
        
        if domain_obj.manager_id.filter(user_id=request_user).exists():
            role_name = "manager"
        elif domain_obj.writer_id.filter(user_id=request_user).exists():
            role_name = "writer"

            
        return JsonResponse({
            "role_data":role_name,
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is get_request_user_role --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)

