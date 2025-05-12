

import requests
import json 
from django.conf import settings
import os
from apiApp.models import article_type, workspace, rabbitmq_queue
RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")


def create_rabbitmq_queues_for_workspace(workspace_slug_id):
    try:
        # Fetch all article_type titles from the database
        article_types = article_type.objects.all()

        # Get the workspace object where the queue names will be stored
        workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)

        # Initialize an empty list to hold the queue names
        queue_names = []

        # Create a queue for each article type
        for obj in article_types:
            # Use the article type title to create a dynamic queue name
            queue_name = f'{workspace_slug_id}_{obj.title}'
            queue_names.append(queue_name)

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
            print(response,'responsesx')
            # Handle the response
            if response.status_code in [200, 201]:
                print(response.json(),'sssssssssssssssssssssssssss')
                # Save the queue info to the rabbitmq_queue model
                rabbitmq_queue.objects.create(
                    workspace_id=workspace_obj,
                    article_type_id=obj,
                    name=queue_name
                )
                print(f'Queue created successfully for {obj.title} with status code: {response.status_code}')
            else:
                print(f"Error creating queue for {obj.title}: {response.status_code}, {response.text}")
                return None, f"API Error: {response.status_code}, {response.text}"

        return "Queue creation process completed successfully", None  # If all queues are created successfully

    except workspace.DoesNotExist:
        print(f"Workspace with slug_id {workspace_slug_id} not found.")
        return None, "Workspace not found"

    except Exception as e:
        print("Error in create_rabbitmq_queues_for_workspace:", e)
        return None, f"Exception: {str(e)}"
