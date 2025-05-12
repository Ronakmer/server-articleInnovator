



import requests
import json 
from django.conf import settings
import os
from apiApp.models import article_type, workspace, rabbitmq_queue
RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")


def create_rabbitmq_queues_for_article_type(article_type_slug_id):
    try:

        article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)


        # Get the workspace object where the queue names will be stored
        workspace_obj = workspace.objects.all()

        # Initialize an empty list to hold the queue names
        queue_names = []

        # Create a queue for each article type
        for data in workspace_obj:
            # Use the data type title to create a dynamic queue name
            queue_name = f'{data.slug_id}_{article_type_obj.title}'
            queue_names.append(queue_name)

            # URL for the RabbitMQ API
            url = f'{RABBITMQ_BASE_URL}/queue/create'

            # Headers for the request
            headers = {
                'Content-Type': 'application/json',
            }

            data = {
                "queue_name": queue_name  
            }

            # Send POST request to create the queue
            response = requests.post(url, headers=headers, json=data)

            # Handle the response
            if response.status_code in [200, 201]:
                
                # Save the queue info to the rabbitmq_queue model
                rabbitmq_queue.objects.create(
                    workspace_id=data.id,
                    article_type_id=article_type_obj,
                    name=queue_name
                )


                print(f'Queue created successfully for {data.title} with status code: {response.status_code}')
            else:
                print(f"Error creating queue for {data.title}: {response.status_code}, {response.text}")
                return None, f"API Error: {response.status_code}, {response.text}"


        return "Queue creation process completed successfully", None  # If all queues are created successfully

    except article_type.DoesNotExist:
        print(f"article_type with slug_id {article_type_slug_id} not found.")
        return None, "article_type not found"

    except Exception as e:
        print("Error in create_rabbitmq_queues_for_article_type:", e)
        return None, f"Exception: {str(e)}"
