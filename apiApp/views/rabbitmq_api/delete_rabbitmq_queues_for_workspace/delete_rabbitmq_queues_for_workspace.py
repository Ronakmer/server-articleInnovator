import requests
import json 
from django.conf import settings
from apiApp.models import workspace, rabbitmq_queue
import os

RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")

def delete_rabbitmq_queues_for_workspace(workspace_slug_id):
    try:
        # Get the workspace object
        workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)

        # Get all queues related to this workspace
        queues = rabbitmq_queue.objects.filter(workspace_id=workspace_obj)

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

    except workspace.DoesNotExist:
        print(f"Workspace with slug_id {workspace_slug_id} not found.")
        return None, "Workspace not found"

    except Exception as e:
        print("Error in delete_rabbitmq_queues_for_workspace:", e)
        return None, f"Exception: {str(e)}"
