import requests
import json 
from django.conf import settings
import os
from apiApp.models import article_type, workspace, rabbitmq_queue
from apiApp.views.rabbitmq_api.delete_rabbitmq_queues_for_article_type.delete_rabbitmq_queues_for_article_type import delete_rabbitmq_queues_for_article_type

RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")

def update_rabbitmq_queues_for_article_type(article_type_slug_id):
    try:
        # Delete existing queues first
        rabbitmq_delete_response, delete_error = delete_rabbitmq_queues_for_article_type(article_type_slug_id)
        if delete_error or not rabbitmq_delete_response:
            return f"Failed to delete queues for the article_type. {delete_error or rabbitmq_delete_response}", None

        # Get article type object
        article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)

        # Get all workspaces
        workspace_list = workspace.objects.all()

        # Create a queue for each workspace
        for data in workspace_list:
            queue_name = f'{data.slug_id}_{article_type_obj.title}'
            url = f'{RABBITMQ_BASE_URL}/queue/create'
            headers = {
                'Content-Type': 'application/json',
            }
            payload = {
                "queue_name": queue_name
            }

            # Send POST request to create the queue
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code in [200, 201]:
                print(f'Queue created: {queue_name}')
                
                # Save to DB
                rabbitmq_queue.objects.create(
                    workspace_id=data.id,
                    article_type_id=article_type_obj,
                    name=queue_name
                )
            else:
                print(f"Error creating queue {queue_name}: {response.status_code}, {response.text}")
                return None, f"API Error: {response.status_code}, {response.text}"

        return "Queue creation process completed successfully", None

    except article_type.DoesNotExist:
        print(f"article_type with slug_id {article_type_slug_id} not found.")
        return None, "article_type not found"

    except Exception as e:
        print("Error in update_rabbitmq_queues_for_article_type:", e)
        return None, f"Exception: {str(e)}"
