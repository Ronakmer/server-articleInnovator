import requests
import os
from django.http import JsonResponse
from apiApp.models import article_type, workspace, rabbitmq_queue
from rest_framework.decorators import api_view


RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")  


@api_view(['POST'])
def add_queue_api(request):
    try:

        queue_name = request.data.get('queue_name')
        
        # URL for the RabbitMQ API
        url = f'{RABBITMQ_BASE_URL}/queue/create'
        print(url, "url")
        # Headers for the request
        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            "queue_name": queue_name  
        }

        # Send POST request to create the queue
        response = requests.post(url, headers=headers, json=data)
        
        print(response,'responsexxx0')
        if response.status_code in [200, 201]:
            return JsonResponse({
                "message": f"Worker '{queue_name}' add successfully.",
                "success": True
            })
        else:
            return JsonResponse({
                "error": f"Failed to scale worker '{queue_name}': {response.status_code} - {response.text}",
                "success": False
            }, status=response.status_code)

    except Exception as e:
        print("This error is add_queue_api --->: ",e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)





