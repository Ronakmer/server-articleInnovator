import requests
import json 
from django.conf import settings
from apiApp.models import article_type, workspace, rabbitmq_queue
import os

RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")



def delete_rabbitmq_queues_for_article_type(article_type_slug_id):
    try:
        # Get the article_type object
        article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)

        # Get all queues related to this article_type
        queues = rabbitmq_queue.objects.filter(article_type_id=article_type_obj)

        # URL for RabbitMQ API to delete queues
        url = f'{RABBITMQ_BASE_URL}/queue/delete'
        headers = {
            "Accept": "application/json"
        }

        # Loop through each queue and delete it from RabbitMQ
        for queue in queues:
            print(f"Deleting queue: {queue.name}")
            response = requests.delete(f'{url}/{queue.name}', headers=headers)

            if response.status_code in [200, 201]:
                print(f"Successfully deleted queue: {queue.name}")
                # Delete queue record from database
                queue.delete()
            else:
                print(f"Error deleting queue {queue.name}: {response.status_code}, {response.text}")
                return None, f"API Error: {response.status_code}, {response.text}"

        return "All queues deleted successfully", None  # Success

    except article_type.DoesNotExist:
        print(f"article_type with slug_id {article_type_slug_id} not found.")
        return None, "article_type not found"

    except Exception as e:
        print("Error in delete_rabbitmq_queues_for_article_type:", e)
        return None, f"Exception: {str(e)}"

