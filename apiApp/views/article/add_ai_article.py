import base64
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from apiApp.models import domain, workspace, article_type, wp_author, wp_category, wp_tag, article
import base64
import requests
from django.http import JsonResponse
from apiApp.views.base.s3.article_josn_method.create_article_folder_and_file_s3.create_article_folder_and_file_s3 import create_article_folder_and_file_s3
from apiApp.views.base.s3.article_josn_method.delete_file_from_s3.delete_file_from_s3 import delete_file_from_s3
from apiApp.views.base.s3.article_josn_method.show_file_from_s3.show_file_from_s3 import show_file_from_s3
from django.http import HttpResponse
# from imagekitio import ImageKit
# from imagekitio.exceptions import ImageKitException
import uuid



def add_ai_article(request_user, request_data):
    try:
        print('ai')
        # data = {
        #     "article_type_slug_id": request_data.get('article_type_slug_id'),
        #     "author_slug_id": request_data.get('author_slug_id'),
        #     "domain_slug_id": request_data.get('domain_slug_id'),
        #     "category_slug_id": request_data.get('category_slug_id'),
        #     "tag_slug_id": request_data.get('tag_slug_id'),
        #     "workspace_slug_id": request_data.get('workspace_slug_id'),
        #     "wp_title": request_data.get('wp_title'),
        #     "wp_content": request_data.get('wp_content'),
        #     "article_status": request_data.get('article_status'),
        #     "wp_featured_image": request_data.get('wp_featured_image'),
        #     "wp_excerpt": request_data.get('wp_excerpt'),
        #     "wp_status": request_data.get('wp_status'),
        #     "wp_slug": request_data.get('wp_slug'),
        # }
        
        # # Handle wp_schedule_time separately
        # wp_schedule_time = request_data.get("wp_schedule_time")
        
        # # Validate wp_schedule_time only if wp_status is "future"
        # if data["wp_status"] == "future":
        #     if not wp_schedule_time:
        #         return {"error": "wp_schedule_time is required when wp_status is future", "success": False}
        #     data["wp_schedule_time"] = wp_schedule_time
        # else:
        #     wp_schedule_time = None

        # print(data, 'data')

        # # Validate required fields
        # missing_fields = [key for key, value in data.items() if value is None or value == ""]

        # if missing_fields:
        #     return {"error": f"Missing required fields: {', '.join(missing_fields)}", "success": False}

        # # Fetch related objects
        # try:
        #     domain_obj = domain.objects.get(slug_id=data["domain_slug_id"])
        #     workspace_obj = workspace.objects.get(slug_id=data["workspace_slug_id"])
        #     article_type_obj = article_type.objects.get(slug_id=data["article_type_slug_id"])
        #     wp_author_obj = wp_author.objects.get(slug_id=data["author_slug_id"])
        # except domain.DoesNotExist:
        #     return {"error": "Domain not found.", "success": False}
        # except workspace.DoesNotExist:
        #     return {"error": "Workspace not found.", "success": False}
        # except article_type.DoesNotExist:
        #     return {"error": "Article type not found.", "success": False}
        # except wp_author.DoesNotExist:
        #     return {"error": "Author not found.", "success": False}

        # # Construct slug
        # wp_slug = f"{domain_obj.name}/{data['wp_slug']}"

        # # Fetch category and tag objects
        # # category_ids = wp_category.objects.filter(slug_id__in=data["category_slug_id"].split(",")) if data["category_slug_id"] else []
        # # tag_ids = wp_tag.objects.filter(slug_id__in=data["tag_slug_id"].split(",")) if data["tag_slug_id"] else []

        # category_ids = []
        # tag_ids = []
        
        # category_names = []
        # tag_names = []

        # if data["category_slug_id"]:
        #     category_objs_list = data["category_slug_id"].split(",")
        #     category_objs_list = [data for data in category_objs_list]
            
        #     # Fetch category objects
        #     category_objs = wp_category.objects.filter(slug_id__in=category_objs_list)
            
        #     # Get category names instead of IDs
        #     category_names = [category.name for category in category_objs]
        #     category_ids = list(category_objs)  # Convert queryset to list

        # if data["tag_slug_id"]:
        #     tag_objs_list = data["tag_slug_id"].split(",")
        #     tag_objs_list = [data for data in tag_objs_list]

        #     # Fetch tag objects
        #     tag_objs = wp_tag.objects.filter(slug_id__in=tag_objs_list)
            
        #     # Get tag names instead of IDs
        #     tag_names = [tag.name for tag in tag_objs]
        #     tag_ids = list(tag_objs)  # Convert queryset to list



        # # # Handle Image Upload
        # # if isinstance(data["wp_featured_image"], str):  # If it's a URL
        # #     image_url = data["wp_featured_image"]
        # # else:  # If it's an uploaded image
        # #     try:
        # #         upload_response = imagekit.upload(file=data["wp_featured_image"], file_name=str(uuid.uuid4()))
        # #         image_url = upload_response.get('url')
        # #     except ImageKitException as e:
        # #         return JsonResponse({"error": "Image upload failed.", "details": str(e), "success": False}, status=500)





        # # API call setup
        # domain_name = domain_obj.name
        # user_login = domain_obj.wordpress_username
        # password = domain_obj.wordpress_application_password

        # api_url = f'https://{domain_name}/wp-json/botxbyte/v1/dynamic-article-publish/'
        # credentials = base64.b64encode(f'{user_login}:{password}'.encode('utf-8')).decode('utf-8')

        # api_data = {
        #     "post_title": data["wp_title"],
        #     "content": data["wp_content"],
        #     "categories": category_names,
        #     "wp_slug": wp_slug,
        #     "status": data["wp_status"],
        #     "wp_featured_image": data["wp_featured_image"],
        #     "wp_schedule_time": wp_schedule_time or "",
        #     "wp_excerpt": data["wp_excerpt"],
        # }

        # headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': f'Basic {credentials}',
        # }

        # response = requests.post(api_url, headers=headers, json=api_data)
        # response_data = response.json()

        # if response.status_code not in (200, 201):
        #     return {"error": f"WordPress API error: {response.status_code} - {response.text}", "success": False}

        # wp_post_id = response_data.get('post_id')

        # # Save article
        # article_obj = article.objects.create(
        #     wp_title=data["wp_title"],
        #     wp_slug=wp_slug,
        #     article_status=data["article_status"],
        #     created_by=request_user,
        #     wp_featured_image=data["wp_featured_image"],
        #     wp_post_id=wp_post_id,
        #     wp_status=data["wp_status"] if data["wp_status"] in dict(article.WP_STATUS_CHOICES) else None,
        #     wp_schedule_time=wp_schedule_time if data["wp_status"] == 'scheduled' else None,
        #     article_type_id=article_type_obj,
        #     domain_id=domain_obj,
        #     workspace_id=workspace_obj,
        #     wp_author_id=wp_author_obj,
        # )

        # # Assign categories and tags
        # if category_ids:
        #     article_obj.wp_category_id.set(category_ids)
        # if tag_ids:
        #     article_obj.wp_tag_id.set(tag_ids)

        # temp_article_id = article_obj.id

        # # Save content to S3
        # try:
        #     s3_data = {
        #         "domain_slug_id": domain_obj.name,
        #         "article_slug_id": article_obj.slug_id,
        #         "wp_content": data["wp_content"],
        #         "wp_excerpt": data["wp_excerpt"]
        #     }
        #     s3_file_path = create_article_folder_and_file_s3(s3_data)

        #     article_obj.wp_content = s3_file_path
        #     article_obj.wp_excerpt = s3_file_path
        #     article_obj.save()

        # except Exception as e:
        #     print("Error in create_article_folder_and_file_s3:", e)
        #     return {"error": "Internal server error.", "success": False}

        # return {"message": "Data added successfully.", "success": True}

    except Exception as e:
        print("Unexpected error in add_ai_article:", e)
        return {"error": "Internal server error.", "success": False}






