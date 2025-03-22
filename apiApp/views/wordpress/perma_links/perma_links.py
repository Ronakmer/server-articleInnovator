from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination
import base64, json
import requests






def get_perma_links(data):

    username = data.get('wordpress_username')
    password = data.get('wordpress_application_password')
    domain_name = data.get('name')

    api_url = f'https://{domain_name}/wp-json/botxbyte/v1/permalinks-info'
    
    credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials}',

    }

    try:
        response = requests.post(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP failures (e.g., 404, 500)
       
        return response.json()  # Return JSON response data
       
    except requests.exceptions.RequestException as e:
        print("Error in get_perma_links:", e)
        return {"error": "Failed to fetch permalinks", "success": False}



# show perma_links
@api_view(['POST'])
def list_perma_links(request):
    try:
        
        wordpress_username = request.data.get('wordpress_username')        
        wordpress_application_password = request.data.get('wordpress_application_password')        
        domain_name = request.data.get('name')        

        data={
            "name":domain_name,
            "wordpress_username":wordpress_username,
            "wordpress_application_password":wordpress_application_password,
        }
        
        response_data = get_perma_links(data)

        if response_data and "error" not in response_data:
            return JsonResponse({"data": response_data, "success": True}, status=200)
        else:
            return JsonResponse(response_data, status=400)  # Return API error response if present

    except Exception as e:
        print("This error is list_perma_links --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# update perma_links
def update_perma_links(data):
    try:
                
        username = data.get('wordpress_username')
        password = data.get('wordpress_application_password')
        domain_name = data.get('name')
        new_perma_links = data.get('new_perma_links')

        api_url = f'https://{domain_name}/wp-json/botxbyte/v1/update-permalinks'

        credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}',

        }
        json_data = {
            'structure': new_perma_links,
        }

        try:
            response = requests.post(api_url, headers=headers, json=json_data)
            print(response.json(),'m-m')
            
            return response.json()  # Return JSON response data

        except requests.exceptions.RequestException as e:
            print("Error in update_perma_links:", e)
            return {"error": "Failed to update permalinks", "success": False}



    except Exception as e:
        print("This error is update_perma_links --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
   