
from django.shortcuts import render,redirect
from apiApp.models import domain, wp_tag, workspace, domain_install_log, domain_install_log_percentage
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
import requests
from django.core.serializers import serialize
import base64
from rest_framework.decorators import api_view
import time




def process_tags(obj_data):
    print(obj_data,'obj_data')
    # time.sleep(30)
    
    domain_obj = obj_data.get("domain_obj")
    workspace_obj = obj_data.get("workspace_obj")
    print(f"domain_obj: {domain_obj}")
    print(f"workspace_obj: {workspace_obj}")
    

    tag_progress = 0
    return_tags = []

    domain_name = domain_obj.name
    username = domain_obj.wordpress_username
    password = domain_obj.wordpress_application_password


    #  add tag
    tag_url = f'https://{domain_name}/wp-json/wp/v2/tags'
    
    credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials}',
    }

    # All tags
    all_tags = []
    per_page = 100
    tag_details = []
    
    # Fetch total pages to calculate start and end pages
    initial_response = requests.get(f'{tag_url}?per_page={per_page}&page=1', headers=headers)
    if initial_response.status_code != 200:
        # return JsonResponse({'error': 'Failed to fetch data from API'}, status=500)
        return 'Failed to fetch tags from the API.' 
    
    total_pages = int(initial_response.headers.get('X-WP-TotalPages', 1))
    start_page = 1
    end_page = total_pages

    for page in range(start_page, end_page + 1):
        paginated_url = f'{tag_url}?per_page={per_page}&page={page}'
        response = requests.get(paginated_url, headers=headers)

        if response.status_code != 200:
            # return JsonResponse({'error': 'Failed to fetch data from API'}, status=500)
            return 'Failed to fetch tags from the API.'

        response_data = response.json()
        if not response_data:
            break


        all_tags.extend(response_data)
        # tag_names = [tag['name'] for tag in response_data]
        tag_details = [{'id': tag['id'], 'name': tag['name'], 'slug':tag['slug'], 'description':tag['description']} for tag in response_data]
    
        #  Find data in database
        existing_tags = []
        non_existing_tags = []
        
        for tag in tag_details:
            find_domain = wp_tag.objects.filter(wp_tag_id=tag['id'], name=tag['name']).exists()
            tag_info={
                'id': tag['id'],
                'name': tag['name'],
                'slug': tag['slug'],
                'description': tag['description'],
                'exists': find_domain
            }
            return_tags.append(tag['name'])
        
            if find_domain:
                existing_tags.append(tag_info)
            else:
                non_existing_tags.append(tag_info)
                                    
        for tag in non_existing_tags:
            tag_obj = wp_tag()
            tag_obj.name = tag['name']
            tag_obj.slug = tag['slug']
            tag_obj.description = tag['description']
            tag_obj.domain_id = domain_obj 
            tag_obj.workspace_id = workspace_obj 
            tag_obj.wp_tag_id = tag['id']
            tag_obj.save()
            
            install_log_obj = domain_install_log()
            install_log_obj.log_type = 'tag'
            install_log_obj.log_text = f"Tag: {tag['name']}"
            install_log_obj.domain_id = domain_obj
            install_log_obj.save()      
            
            tag_progress = 3 / len(non_existing_tags)
                        
            percentage_log_obj = domain_install_log_percentage()
            percentage_log_obj.domain_install_log_id = install_log_obj
            percentage_log_obj.log_percentage = tag_progress
            percentage_log_obj.domain_id = domain_obj
            percentage_log_obj.save()     
        
        page += 1


    return "tag add successfully."





@api_view(['POST'])
def fetch_tag_data(request):
    try:
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
        print(domain_slug_id,'domain_slug_id')

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
        
        result = process_tags(obj_data)
        if "Failed" in result:
            return JsonResponse({"error": result}, status=500)
        
        return JsonResponse({'message': result}, status=200)
    
    except Exception as e:
        print("This error is fetch_tag_data --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)












# @api_view(['POST'])
# def fetch_tag_data(request):
#     try:
#         domain_slug_id = request.data.get('domain_slug_id')
#         workspace_slug_id = request.data.get('workspace_slug_id')
#         print(domain_slug_id,'domain_slug_id')

#         if not domain_slug_id:
#             return JsonResponse({"error": "Domain slug ID is required."}, status=400)
    
#         if not workspace_slug_id:
#             return JsonResponse({"error": "workspace slug ID is required."}, status=400)


#         try:
#             domain_obj = domain.objects.get(slug_id = domain_slug_id)
#         except domain.DoesNotExist:
#             return JsonResponse({
#                 "error": "Invalid domain.",
#             }, status=404) 

#         try:
#             workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
#         except workspace.DoesNotExist:
#             return JsonResponse({
#                 "error": "Invalid workspace.",
#             }, status=404)
        
#         slug_id_data={
#             "domain_obj":domain_obj,
#             "workspace_obj":workspace_obj,
#         }
        
#         result = process_tags(slug_id_data)
#         if "Failed" in result:
#             return JsonResponse({"error": result}, status=500)

#         print(result,'result')
        
#         # tag_progress = 0
#         # return_tags = []

#         # domain_name = domain_obj.name
#         # username = domain_obj.wordpress_username
#         # password = domain_obj.wordpress_application_password


#         # #  add tag
#         # tag_url = f'https://{domain_name}/wp-json/wp/v2/tags'
        
#         # credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

#         # headers = {
#         #     'Content-Type': 'application/json',
#         #     'Authorization': f'Basic {credentials}',

#         # }

#         # # All tags
#         # all_tags = []
#         # per_page = 100
#         # tag_details = []
        
#         # # Fetch total pages to calculate start and end pages
#         # initial_response = requests.get(f'{tag_url}?per_page={per_page}&page=1', headers=headers)
#         # if initial_response.status_code != 200:
#         #     return JsonResponse({'error': 'Failed to fetch data from API'}, status=500)

#         # total_pages = int(initial_response.headers.get('X-WP-TotalPages', 1))
#         # start_page = 1
#         # end_page = total_pages

#         # for page in range(start_page, end_page + 1):
#         #     paginated_url = f'{tag_url}?per_page={per_page}&page={page}'
#         #     response = requests.get(paginated_url, headers=headers)

#         #     if response.status_code != 200:
#         #         return JsonResponse({'error': 'Failed to fetch data from API'}, status=500)

#         #     response_data = response.json()
#         #     if not response_data:
#         #         break


#         #     all_tags.extend(response_data)
#         #     # tag_names = [tag['name'] for tag in response_data]
#         #     tag_details = [{'id': tag['id'], 'name': tag['name'], 'slug':tag['slug'], 'description':tag['description']} for tag in response_data]


#         #     page += 1


        
#         # #  Find data in database
#         # existing_tags = []
#         # non_existing_tags = []
        
#         # for tag in tag_details:
#         #     find_domain = wp_tag.objects.filter(wp_tag_id=tag['id'], name=tag['name']).exists()
#         #     tag_info={
#         #         'id': tag['id'],
#         #         'name': tag['name'],
#         #         'slug': tag['slug'],
#         #         'description': tag['description'],
#         #         'exists': find_domain
#         #     }
#         #     return_tags.append(tag['name'])
        
#         #     if find_domain:
#         #         existing_tags.append(tag_info)
#         #     else:
#         #         non_existing_tags.append(tag_info)
                                    
#         # for tag in non_existing_tags:
#         #     tag_obj = wp_tag()
#         #     tag_obj.name = tag['name']
#         #     tag_obj.slug = tag['slug']
#         #     tag_obj.description = tag['description']
#         #     tag_obj.domain_id = domain_obj 
#         #     tag_obj.workspace_id = workspace_obj 
#         #     tag_obj.wp_tag_id = tag['id']
#         #     tag_obj.save()
            
#         #     install_log_obj = domain_install_log()
#         #     install_log_obj.log_type = 'tag'
#         #     install_log_obj.log_text = f"Tag: {tag['name']}"
#         #     install_log_obj.domain_id = domain_obj
#         #     install_log_obj.save()      
            
#         #     tag_progress = 3 / len(non_existing_tags)
                        
#         #     percentage_log_obj = domain_install_log_percentage()
#         #     percentage_log_obj.domain_install_log_id = install_log_obj
#         #     percentage_log_obj.log_percentage = tag_progress
#         #     percentage_log_obj.domain_id = domain_obj
#         #     percentage_log_obj.save()      

        
#         return JsonResponse({'status': 200, 'message': result})
    
#     except Exception as e:
#         print("This error is fetch_tag_data --->: ", e)
#         return JsonResponse({"error": "Internal server error."}, status=500)







