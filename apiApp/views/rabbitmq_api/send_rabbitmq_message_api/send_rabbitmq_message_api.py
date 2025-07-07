


# views.py or wherever you're adding server-side logic
import requests
import os
from django.http import JsonResponse
from apiApp.models import article_type, workspace, rabbitmq_queue
from rest_framework.decorators import api_view


RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")  


def send_rabbitmq_message_api(input_json):
    # Send result to output queue regardless of success/failure
    # Send result to output queue regardless of success/failure
    cleaned_input_json = input_json.get('input_json', {})
    message_json = cleaned_input_json.get('message')
    
    print(message_json,'sdfsdfsdfsd23')
  
    try:
        worker_name = 'url_rewriter_para_request_worker'
        # send_response_url = f"{article_queue_service_base_url}/queue/publish/article-response-queue"
        send_response_url = f"{RABBITMQ_BASE_URL}/queue/publish/article-request-queue"
        
        output_payload = {
            "message":message_json
        }
        
        
        response = requests.post(
            send_response_url,
            json=output_payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        # Log the actual response for debugging
        print(f"Raw response status: {response.status_code}")
        print(f"Raw response content: {response.text}")
        
        # Only try to parse JSON if we got a valid response
        if response.text:
            response_data = response.json()
        else:
            print("Received empty response from API")
            response_data = {}
        
        print(f"Response from output queue: {response_data}")

        if response.status_code != 200:
            error_data = response.json() if response.text else {}
            if isinstance(error_data, dict) and "No workers" in str(error_data.get("error", "")):
                print("No worker available, attempting to scale up...")
                # Try to scale up worker using the workspace ID
                if scale_worker(str(worker_name)):
                    print("Successfully initiated worker scale up")
                    # Retry the request after scaling
                    response = requests.post(
                        send_response_url,
                        json=output_payload,
                        headers={"Content-Type": "application/json"},
                        timeout=10
                    )
            
            if response.status_code != 200:
                print(f"Failed to send result to output queue. Status: {response.status_code}, Response: {response.text}")
        else:
            print(f"Successfully sent result to output queue for message")
            
    except Exception as api_error:
        print(f"Error sending result to output queue: {api_error}")




        
    


def scale_worker(worker_name, count=1):
        """Scale up worker instances"""
        scale_url = f"{RABBITMQ_BASE_URL}/worker/scale/article-request-queue"   
        print(f"scale_url: {scale_url}")
        scale_data = {"count": count,"worker_name":f"{worker_name}"}
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(scale_url, json=scale_data, headers=headers)
            if response.status_code in [200, 201]:
                print(f"Successfully scaled worker {worker_name} with count {count}")
                return True
            else:
                print(f"Failed to scale worker: {response.status_code} - {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Exception during scaling worker: {e}")
            return False
