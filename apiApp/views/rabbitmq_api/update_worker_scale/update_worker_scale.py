import requests
import os
from django.http import JsonResponse
from apiApp.models import article_type, workspace, rabbitmq_queue
from rest_framework.decorators import api_view


RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")  


@api_view(['POST'])
def update_worker_scale(request):
    try:

        queue_name = request.data.get('queue_name')
        worker_count = request.data.get('worker_count')
        rabbitmq_queue_obj = rabbitmq_queue.objects.filter(name=queue_name).first()
        if not rabbitmq_queue_obj:
            return JsonResponse({"error": "Queue not found.", "success": False}, status=404)
        
        
        article_type_obj = rabbitmq_queue_obj.article_type_id
        if not article_type_obj:
            return JsonResponse({"error": "Article type not associated with this queue.", "success": False}, status=404)

        worker_name = article_type_obj.rabbitmq_worker 

        if not worker_name:
            return JsonResponse({"error": "Worker name not found in article type.", "success": False}, status=404)

        
        url = f'{RABBITMQ_BASE_URL}/worker/scale/{rabbitmq_queue_obj.name}'
        
        payload = {
            "count": worker_count,
            "worker_name": worker_name 
        }
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload)
        print(response,'responsexxx0')
        if response.status_code in [200, 201]:
            return JsonResponse({
                "message": f"Worker '{rabbitmq_queue_obj.name}' scaled successfully.",
                "success": True
            })
        else:
            return JsonResponse({
                "error": f"Failed to scale worker '{rabbitmq_queue_obj.name}': {response.status_code} - {response.text}",
                "success": False
            }, status=response.status_code)

    except Exception as e:
        print("This error is update_worker_scale --->: ",e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)





