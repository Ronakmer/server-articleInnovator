
from django.shortcuts import render,redirect
from apiApp.models import domain, wp_category, workspace, domain_install_log, domain_install_log_percentage
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
import requests
from django.core.serializers import serialize
import base64
from rest_framework.decorators import api_view




def process_category(obj_data):
    
    domain_obj = obj_data.get("domain_obj")
    workspace_obj = obj_data.get("workspace_obj")
    print(f"domain_obj: {domain_obj}")
    print(f"workspace_obj: {workspace_obj}")


    categories_progress = 0
    return_category = []  
        
    domain_name = domain_obj.name
    username = domain_obj.wordpress_username
    password = domain_obj.wordpress_application_password

    #  add category
    category_url = f'https://{domain_name}/wp-json/wp/v2/categories'
    
    credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials}',

    }
    
    # All tags
    all_categories = []
    category_details = []
    per_page = 100


    # Fetch total pages to calculate start and end pages
    initial_response = requests.get(f'{category_url}?per_page={per_page}&page=1', headers=headers)
    if initial_response.status_code != 200:
        # return JsonResponse({'error': 'Failed to fetch data from WordPress API'}, status=500)
        return 'Failed to fetch category from the API.'

    total_pages = int(initial_response.headers.get('X-WP-TotalPages', 1))
    start_page = 1
    end_page = total_pages

    # Loop through pages
    for page in range(start_page, end_page + 1):
        paginated_url = f'{category_url}?per_page={per_page}&page={page}'
        response = requests.get(paginated_url, headers=headers)

        if response.status_code != 200:
            # return JsonResponse({'error': 'Failed to fetch data from WordPress API'}, status=500)
            return 'Failed to fetch category from the API.'

        response_data = response.json()
        if not response_data:
            break

        all_categories.extend(response_data)
        category_details = [{'id': category['id'], 'name': category['name'], 'slug': category['slug'], 'description': category['description']} for category in response_data]

        
    
        # Find data in database
        existing_categories = []
        non_existing_categories = []
        
        for category in category_details:
            find_category = wp_category.objects.filter(wp_cat_id=category['id'], name=category['name']).exists()
            category_info = {
                'id': category['id'],
                'name': category['name'],
                'slug': category['slug'],
                'description': category['description'],
                'exists': find_category
            }
            
            return_category.append(category['name'])
        
            if find_category:
                existing_categories.append(category_info)
            else:
                non_existing_categories.append(category_info)
        
        # Add non-existing categories to the database
        for category in non_existing_categories:
            category_obj = wp_category()
            category_obj.name = category.get('name')
            category_obj.slug = category.get('slug')
            category_obj.description = category.get('description')

            category_obj.domain_id = domain_obj
            category_obj.workspace_id = workspace_obj
            category_obj.wp_cat_id = category.get('id')
            category_obj.save() 
            
            install_log_obj = domain_install_log()
            install_log_obj.log_type = 'category'
            install_log_obj.log_text = f"category: {category['name']}"
            install_log_obj.domain_id = domain_obj
            install_log_obj.save()      
            
            categories_progress = 3 / len(non_existing_categories)
            
            percentage_log_obj = domain_install_log_percentage()
            percentage_log_obj.domain_install_log_id = install_log_obj
            percentage_log_obj.log_percentage = categories_progress
            percentage_log_obj.domain_id = domain_obj
            percentage_log_obj.save()      


        page += 1

    return "category add successfully."





@api_view(['POST'])
def fetch_category_data(request):
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
              
        result = process_category(obj_data)
        if "Failed" in result:
            return JsonResponse({"error": result}, status=500)
        
        return JsonResponse({'message': result}, status=200)

    except Exception as e:
        print("This error is fetch_category_data --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

