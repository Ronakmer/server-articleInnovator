
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs
import json
import base64
import requests
from rest_framework.decorators import api_view


@api_view(['POST'])
def add_test_article(request):
    try:
        wp_username = request.data.get('wp_username')
        wp_password = request.data.get('wp_password')
        domain_name = request.data.get('domain_name')  

        api_url = f'https://{domain_name}/wp-json/botxbyte/v1/dynamic-article-publish/'
        
        credentials = base64.b64encode(f'{wp_username}:{wp_password}'.encode('utf-8')).decode('utf-8')
        data = {
            "post_title": "Your Article Title",
            "content": "Your article content here.",
            "networth": "$1 M",
            "category": "Finance",
            "price": "2001",
            "status": "draft"
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}',
        }

        response = requests.post(api_url, headers=headers, json=data, verify=False)
        
        return JsonResponse({'status_code': response.status_code, 'domain_name' : domain_name ,'response_text': response.json()})

    except Exception as e:
        print("This error is add_test_article --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



@api_view(['POST'])
def delete_test_article(request):
    try:
        
        wp_username = request.data.get('wp_username')
        wp_password = request.data.get('wp_password')
        domain_name = request.data.get('domain_name')  
        test_post_id = request.data.get('test_post_id')  
        
        print(wp_username, wp_username, domain_name, test_post_id)
        
        api_url = f'https://{domain_name}/wp-json/wp/v2/posts/{test_post_id}'

        credentials = base64.b64encode(f'{wp_username}:{wp_password}'.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {credentials}',
        }

        response = requests.delete(api_url, headers=headers, verify=False)

        return JsonResponse({'status_code': response.status_code,'response_text': response.json()})

    except Exception as e:
        print("This error is delete_test_article --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)
