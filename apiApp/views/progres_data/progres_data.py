


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_detail_serializer
from apiApp.models import domain, domain_install_log, domain_install_log_percentage, workspace
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from django.db.models import Q
import json 



# progres_data
@api_view(['GET'])
def progres_data(request):
    try:

        domain_slug_id = request.GET.get('domain_slug_id')
        workspace_slug_id = request.GET.get('workspace_slug_id')

        domain_obj = domain.objects.get(slug_id = domain_slug_id)

        progres_data_obj = domain_install_log_percentage.objects.filter(
            domain_id=domain_obj, 
            status=False,  
        ).first()
        serialized_data = {}

        if progres_data_obj:
            progres_data_obj.status = True
            progres_data_obj.save()
        
        print(progres_data_obj,'progres_data_obj')

    
        if progres_data_obj:
            progres_data_obj.status = True
            progres_data_obj.save()
            serialized_data = {
                'log_percentage': progres_data_obj.log_percentage,
                'log_text': progres_data_obj.domain_install_log_id.log_text if progres_data_obj.domain_install_log_id else '',
                'last_log_id': progres_data_obj.id
            }
        else:
            serialized_data = {
                'log_percentage': None,
                'log_text': None,
                'last_log_id': None
            }

        print(serialized_data,'serialized_data')

        return JsonResponse({'message': 'success', 'progress_data': serialized_data, "success": True},status=200)

    except Exception as ex:
        # Return error response
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


