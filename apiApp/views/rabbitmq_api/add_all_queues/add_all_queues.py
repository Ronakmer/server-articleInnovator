# views.py or wherever you're adding server-side logic
import requests
import os
from django.http import JsonResponse
from apiApp.models import article_type, workspace, rabbitmq_queue
from rest_framework.decorators import api_view


RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")  


@api_view(['POST'])
def add_all_queues(request):
    try:

        rabbitmq_queue_obj = rabbitmq_queue.objects.all()

        # Now create queues via RabbitMQ API
        for data in rabbitmq_queue_obj:
            response = requests.post(
                f'{RABBITMQ_BASE_URL}/queue/create',
                headers={'Content-Type': 'application/json'},
                json={"data": data.name}
            )

            if response.status_code in [200, 201]:
                print(f'Queue created successfully ')
            else:
                print(f"Failed to create queue {data.name}: {response.status_code} - {response.text}")

        return JsonResponse({
            "message": f"queues created successfully.",
            # "queues": created_queues,
            "success": True
        })

    except Exception as e:
        print("This error is add_all_queues --->: ",e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)


