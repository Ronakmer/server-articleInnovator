


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import user_detail_serializer
from apiApp.models import domain, domain_install_log, domain_install_log_percentage
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from django.db.models import Q
import json 



# progres_data
@api_view(['GET'])
def progres_data(request):
    try:
        request = json.loads(request.body)
        domain_id = request['domain_id']
        print(domain_id,'9898')
        domain_obj = domain.objects.get(id=domain_id)
        last_log_id = request.get('last_log_id')

        if last_log_id:
            progres_data = domain_install_log_percentage.objects.filter(domain_id = domain_obj,id__gt=last_log_id).values_list('log_percentage', 'domain_install_log_id__log_text','id').first()
        else:
            progres_data = domain_install_log_percentage.objects.filter(domain_id = domain_obj).values_list('log_percentage', 'domain_install_log_id__log_text','id').first()
            
            
        # Prepare the serialized data
        if progres_data:
            serialized_data = {
                'log_percentage': progres_data[0],
                'log_text': progres_data[1],
                'last_log_id':progres_data[2],
            }
        else:
            serialized_data = {}


        return JsonResponse({'status': 200, 'message': 'success', 'progress_data': serialized_data})

    except Exception as ex:
        # Return error response
        return JsonResponse({'status': 500, 'message': str(ex)})


