
from apiApp.models import domain, article, article_info, workspace, domain_install_log, domain_install_log_percentage, internal_links, external_links
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
import requests
from django.core.serializers import serialize
import base64
from rest_framework.decorators import api_view
from datetime import datetime, timedelta




def process_article(obj_data):
         
    domain_obj = obj_data.get("domain_obj")
    workspace_obj = obj_data.get("workspace_obj")
    request_user = obj_data.get("request_user")
    
    # Replace with actual credentials

    domain_name = domain_obj.name
    username = domain_obj.wordpress_username
    password = domain_obj.wordpress_application_password


    # Prepare API URL and credentials
    api_url = f'https://{domain_name}/wp-json/botxbyte/v1/article-info-list/'
    credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials}',
    }

    page = 1
    per_page = 100
    article_progress = 0
    total_articles = 0
    return_article = []

    # Initialize loop with a maximum number of pages (you can modify this as needed)
    data = {
        'limit': per_page,
        'offset': (page - 1) * per_page,
    }
    # payload={}
    
    # Initial request to get total pages
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code != 200:
        return "Failed to fetch article data from API."

    response_data = response.json()
    total_pages = response_data.get('max_pages', 1)
    total_articles = 0  # Initialize total_articles at the start

    # Loop through all pages
    for page in range(1, total_pages + 1):
        data['offset'] = (page - 1) * per_page
        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code != 200:
            # return "Failed to fetch article data from API."
            break
        
        response_data = response.json()

        if not response_data or 'articles' not in response_data:
            break

        article_datas = response_data['articles']
        total_articles += len(article_datas)

        for data in article_datas:
            return_article.append(data['title'])

            print(data)
            
            # Date formatting
            date_string = data['date']
            naive_datetime = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            aware_datetime = naive_datetime.date()

            # Article save in database
            article_obj = article(
                wp_title=data.get('title'),
                wp_slug=data.get('slug'),
                wp_content=data.get('content'),
                wp_status=data.get('status'),
                wp_featured_image=data.get('featured_image_url'),
                wp_post_id=data.get('id'),
                wp_excerpt=data.get('excerpt'),
                wp_modified_date=data.get('modified_date'),
                wp_schedule_time=aware_datetime,  # Store aware datetime
                created_by=request_user,
                workspace_id=workspace_obj
            )
            article_obj.save()


            # Save article info
            article_info_obj = article_info(
                custom_fields=data['meta_data'],
                word_count=data['content_analysis']['word_count'],
                image_count=data['content_analysis']['image_count'],
                heading_count=data['content_analysis']['heading_count'],
                total_paragraphs=data['content_analysis']['total_paragraphs'],
                long_paragraphs=data['content_analysis']['long_paragraphs'],
                medium_paragraphs=data['content_analysis']['medium_paragraphs'],
                short_paragraphs=data['content_analysis']['short_paragraphs'],
                total_sentences=data['content_analysis']['total_sentences'],
                long_sentences=data['content_analysis']['long_sentences'],
                medium_sentences=data['content_analysis']['medium_sentences'],
                short_sentences=data['content_analysis']['short_sentences'],
                passive_sentences=data['content_analysis']['passive_sentences'],
                article_id=article_obj
            )
            article_info_obj.save()


            # Handle internal links
            for link_data in ['inbound', 'outbound']:
                for link in data['content_analysis']['internal_links'][link_data]['list']:
                    internal_links_obj = internal_links(
                        link_type=link_data,
                        post_title=link['post_title'],
                        anchor_text=link['anchor_text'],
                        url=link['url'],
                        article_id=article_obj,
                        derived_by='wordpress'
                    )
                    internal_links_obj.save()

            # Handle external links
            external_links_data = data['content_analysis']['external_links']
            for links in external_links_data['list']:
                external_links_obj = external_links(
                    anchor_text=links['anchor_text'],
                    url=links['url'],
                    article_id=article_obj,
                    derived_by='wordpress'
                )
                external_links_obj.save()


            # Log progress for each article
            install_log_obj = domain_install_log(
                log_type='article',
                log_text=f"Article: {data['title']}",
                domain_id=domain_obj
            )
            install_log_obj.save()
            
            # Update progress
            article_progress = 30 / total_articles
            
            # Save progress to percentage log
            percentage_log_obj = domain_install_log_percentage(
                domain_install_log_id=install_log_obj,
                log_percentage=article_progress,
                domain_id=domain_obj
            )
            percentage_log_obj.save()
            
    return "article  add successfully."




@api_view(['POST'])
def fetch_article_data(request):
    try:
        
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not domain_slug_id:
            return JsonResponse({"error": "Domain slug ID is required.","success": False}, status=400)
    
        if not workspace_slug_id:
            return JsonResponse({"error": "workspace slug ID is required.","success": False}, status=400)


        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "Invalid domain.","success": False}, status=404) 

        try:
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Invalid workspace.","success": False}, status=404)

        obj_data={
            "domain_obj":domain_obj,
            "workspace_obj":workspace_obj,
            "request_user":request.user,
        }

        result = process_article(obj_data)
        if "Failed" in result:
            return JsonResponse({"error": result,"success": False}, status=500)
        
        return JsonResponse({'message': result,"success": True}, status=200)


    except Exception as e:
        print("This error is fetch_article_data --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

