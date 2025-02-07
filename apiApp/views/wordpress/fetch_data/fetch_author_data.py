
from django.shortcuts import render,redirect
from apiApp.models import domain, wp_author, workspace, domain_install_log, domain_install_log_percentage
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
import requests
from django.core.serializers import serialize
import base64
from rest_framework.decorators import api_view





def process_author(obj_data):
    
    domain_obj = obj_data.get("domain_obj")
    workspace_obj = obj_data.get("workspace_obj")

    
    author_progress = 0        
    return_author = []

    domain_name = domain_obj.name
    username = domain_obj.wordpress_username
    password = domain_obj.wordpress_application_password

    author_url = f'https://{domain_name}/wp-json/wp/v2/users'
    
    credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials}',

    }

    all_authors = []
    per_page = 100
    author_details = []
    
    # Fetch total pages to calculate start and end pages
    initial_response = requests.get(f'{author_url}?per_page={per_page}&page=1', headers=headers)
    if initial_response.status_code != 200:
        # return JsonResponse({'error': 'Failed to fetch data from API'}, status=500)
        return 'Failed to fetch author from the API.' 
    
    total_pages = int(initial_response.headers.get('X-WP-TotalPages', 1))
    start_page = 1
    end_page = total_pages


    
    for page in range(start_page, end_page + 1):
        paginated_url = f'{author_url}?per_page={per_page}&page={page}'
        response = requests.get(paginated_url, headers=headers)

        if response.status_code != 200:
            # return JsonResponse({'error': 'Failed to fetch data from API'}, status=500)
            return 'Failed to fetch author from the API.'

        response_data = response.json()
        if not response_data:
            break

        all_authors.extend(response_data)
        author_details = [{'id': author['id'], 'username': author['slug'], 'name': author['name'],'bio': author['description']} for author in response_data]

        # Find data in database
        existing_authors = []
        non_existing_authors = []

        for author in author_details:
            find_author = wp_author.objects.filter(wp_author_id=author['id'], username=author['username']).exists()
            author_info = {
                'id': author['id'],
                'username': author['username'],
                'name': author['name'],
                'bio': author['bio'],
                'exists': find_author
            }
            return_author.append(author['name']) 
        
            if find_author:
                existing_authors.append(author_info)
            else:
                non_existing_authors.append(author_info)
                
        # Add non-existing authors to the database
        for author in non_existing_authors:
            
            # Split the name into first and last name
            name_parts = author['name'].split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''


            author_obj = wp_author()
            author_obj.username = author['username']
            author_obj.domain_id = domain_obj
            author_obj.wp_author_id = author['id']
            author_obj.bio = author['bio']
            author_obj.first_name = first_name
            author_obj.last_name = last_name
            author_obj.workspace_id = workspace_obj
            # author_obj.email = author['email']
            author_obj.save()
            
            install_log_obj = domain_install_log()
            install_log_obj.log_type = 'author'
            install_log_obj.log_text = f"Author: {author['username']}"
            install_log_obj.domain_id = domain_obj
            install_log_obj.save()      
            
            author_progress = 4 / len(non_existing_authors)

            percentage_log_obj = domain_install_log_percentage()
            percentage_log_obj.domain_install_log_id = install_log_obj
            percentage_log_obj.log_percentage = author_progress
            percentage_log_obj.domain_id = domain_obj
            percentage_log_obj.save()      

        page += 1

    return "tag add successfully."





@api_view(['POST'])
def fetch_author_data(request):
    try:
        
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not domain_slug_id:
            return JsonResponse({"error": "Domain slug ID is required."}, status=400)
    
        if not workspace_slug_id:
            return JsonResponse({"error": "workspace slug ID is required."}, status=400)


        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({
                "error": "Invalid domain.",
            }, status=404) 

        try:
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "Invalid workspace.",
            }, status=404) 
        
       
        obj_data={
            "domain_obj":domain_obj,
            "workspace_obj":workspace_obj,
        }
        
        result = process_author(obj_data)
        if "Failed" in result:
            return JsonResponse({"error": result}, status=500)
        
        return JsonResponse({'message': result}, status=200)

    
    except Exception as e:
        print("This error is fetch_author_data --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

