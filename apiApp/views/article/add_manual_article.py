import base64
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from apiApp.models import domain, workspace, article_type, wp_author, wp_category, wp_tag, article, image_kit_configuration
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

from datetime import datetime, timezone
import base64
import io
import requests
from PIL import Image
from imagekitio import ImageKit
from imagekitio.models import UploadFileRequestOptions
from PIL import Image
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from apiApp.views.base.image_kit_method.image_kit_method import upload_to_imagekit


def add_manual_article(request_user, request_data):
    try:
        data = {
            "article_type_slug_id": request_data.get('article_type_slug_id'),
            "author_slug_id": request_data.get('author_slug_id'),
            "domain_slug_id": request_data.get('domain_slug_id'),
            "category_slug_id": request_data.get('category_slug_id'),
            "tag_slug_id": request_data.get('tag_slug_id'),
            "workspace_slug_id": request_data.get('workspace_slug_id'),
            "wp_title": request_data.get('wp_title'),
            "wp_content": request_data.get('wp_content'),
            "article_status": request_data.get('article_status'),
            "wp_featured_image": request_data.get('wp_featured_image'),
            "wp_excerpt": request_data.get('wp_excerpt'),
            "wp_status": request_data.get('wp_status'),
            "wp_slug": request_data.get('wp_slug'),
        }
        
        # Handle wp_schedule_time separately
        wp_schedule_time = request_data.get("wp_schedule_time")
        
        
        # Validate wp_schedule_time only if wp_status is "future"
        # if data["wp_status"] == "future":
        scheduled_statuses = ['future', 'scheduled']
        if data["wp_status"] in scheduled_statuses:

            if not wp_schedule_time:
                return {"error": "wp_schedule_time is required when wp_status is future", "success": False}
            data["wp_schedule_time"] = wp_schedule_time
        else:
            wp_schedule_time = None


        # wp_featured_image
        # wp_featured_image = request_data.get("wp_featured_image")





        # Validate required fields
        missing_fields = [key for key, value in data.items() if value is None or value == ""]

        if missing_fields:
            return {"error": f"Missing required fields: {', '.join(missing_fields)}", "success": False}

        # Fetch related objects
        try:
            domain_obj = domain.objects.get(slug_id=data["domain_slug_id"])
            workspace_obj = workspace.objects.get(slug_id=data["workspace_slug_id"])
            article_type_obj = article_type.objects.get(slug_id=data["article_type_slug_id"])
            wp_author_obj = wp_author.objects.get(slug_id=data["author_slug_id"])
        except domain.DoesNotExist:
            return {"error": "Domain not found.", "success": False}
        except workspace.DoesNotExist:
            return {"error": "Workspace not found.", "success": False}
        except article_type.DoesNotExist:
            return {"error": "Article type not found.", "success": False}
        except wp_author.DoesNotExist:
            return {"error": "Author not found.", "success": False}

        # Construct slug
        wp_slug = f"{domain_obj.name}/{data['wp_slug']}"

        # Fetch category and tag objects
        # category_ids = wp_category.objects.filter(slug_id__in=data["category_slug_id"].split(",")) if data["category_slug_id"] else []
        # tag_ids = wp_tag.objects.filter(slug_id__in=data["tag_slug_id"].split(",")) if data["tag_slug_id"] else []

        category_ids = []
        tag_ids = []
        
        category_names = []
        tag_names = []

        if data["category_slug_id"]:
            category_objs_list = data["category_slug_id"].split(",")
            category_objs_list = [data for data in category_objs_list]
            
            # Fetch category objects
            category_objs = wp_category.objects.filter(slug_id__in=category_objs_list)
            
            # Get category names instead of IDs
            category_names = [category.name for category in category_objs]
            category_ids = list(category_objs)  # Convert queryset to list

        if data["tag_slug_id"]:
            tag_objs_list = data["tag_slug_id"].split(",")
            tag_objs_list = [data for data in tag_objs_list]

            # Fetch tag objects
            tag_objs = wp_tag.objects.filter(slug_id__in=tag_objs_list)
            
            # Get tag names instead of IDs
            tag_names = [tag.name for tag in tag_objs]
            tag_ids = list(tag_objs)  # Convert queryset to list



            if data["wp_featured_image"] and not data["wp_featured_image"].startswith(("http://", "https://")):
                # workspace_id = data["workspace_slug_id"]  # Directly from data
                # data["wp_featured_image"] = upload_to_imagekit(workspace_id, data["wp_featured_image"]) or None
                
                image_url = upload_to_imagekit(data["wp_featured_image"], workspace_obj)
                data["wp_featured_image"] = image_url if image_url else None


        # API call setup
        domain_name = domain_obj.name
        user_login = domain_obj.wordpress_username
        password = domain_obj.wordpress_application_password

        api_url = f'https://{domain_name}/wp-json/botxbyte/v1/dynamic-article-publish/'
        credentials = base64.b64encode(f'{user_login}:{password}'.encode('utf-8')).decode('utf-8')

        print(category_names,'category_names')
        print(wp_schedule_time,'wp_schedule_time')
        print(data["wp_status"],'data["wp_status"]')



        api_data = {
            "post_title": data["wp_title"],
            "content": data["wp_content"],
            "categories": category_names,
            "wp_slug": wp_slug,
            "status": data["wp_status"],
            "wp_featured_image": data["wp_featured_image"],
            # "date_gmt": wp_schedule_time or "",
            # "date_gmt": f"{wp_schedule_time}+00:00" if wp_schedule_time else "",
            "date": f"{wp_schedule_time}+00:00" if wp_schedule_time else "",
            "wp_excerpt": data["wp_excerpt"],
            "tags": tag_names,
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}',
        }

        response = requests.post(api_url, headers=headers, json=api_data)
        response_data = response.json()
        print(response_data,'responsex')

        if response.status_code not in (200, 201):
            return {"error": f"WordPress API error: {response.status_code} - {response.text}", "success": False}

        wp_post_id = response_data.get('post_id')

        # Save article
        article_obj = article.objects.create(
            wp_title=data["wp_title"],
            wp_slug=wp_slug,
            article_status=data["article_status"],
            created_by=request_user,
            wp_featured_image=data["wp_featured_image"],
            wp_post_id=wp_post_id,
            wp_status=data["wp_status"] if data["wp_status"] in dict(article.WP_STATUS_CHOICES) else None,
            # wp_schedule_time=wp_schedule_time if data["wp_status"] == 'scheduled' else None,
            wp_schedule_time=wp_schedule_time if data["wp_status"] in ['future', 'scheduled'] else None,

            article_type_id=article_type_obj,
            domain_id=domain_obj,
            workspace_id=workspace_obj,
            wp_author_id=wp_author_obj,
        )

        # Assign categories and tags
        if category_ids:
            article_obj.wp_category_id.set(category_ids)
        if tag_ids:
            article_obj.wp_tag_id.set(tag_ids)

        temp_article_id = article_obj.id

        # Save content to S3
        try:
            s3_data = {
                "domain_slug_id": domain_obj.name,
                "article_slug_id": article_obj.slug_id,
                "wp_content": data["wp_content"],
                "wp_excerpt": data["wp_excerpt"]
            }
            s3_file_path = create_article_folder_and_file_s3(s3_data)

            article_obj.wp_content = s3_file_path
            article_obj.wp_excerpt = s3_file_path
            article_obj.save()

        except Exception as e:
            print("Error in create_article_folder_and_file_s3:", e)
            return {"error": "Internal server error.", "success": False}

        return {"message": "Data added successfully.", "success": True}

    except Exception as e:
        print("Unexpected error in add_manual_article:", e)
        return {"error": "Internal server error.", "success": False}








def upload_to_imagekit(base64_strings, workspace_id, file_name="uploaded_image.jpg"):
    # imagekit = ImageKit(
    #     private_key='private_QsF9D6YRrbJdWLn8hnZROA4HCMk=',
    #     public_key='public_tIF7GbY5ixVQhO3149pUgym/4IA=',
    #     url_endpoint='https://ik.imagekit.io/botxbyte'
    # )

    now = datetime.now()  # Gets the current local date and time
    current_year = now.year
    current_month = now.month
    current_date = now.day

    folder_path = f"articleInnovator/image/{workspace_id.name}/{current_year}/{current_month}/{current_date}"

    # Get ImageKit configuration
    image_kit_configuration_obj = image_kit_configuration.objects.filter(workspace_id=workspace_id.id, default_section=True).first()
    if not image_kit_configuration_obj:
        print("ImageKit configuration not found")
        return None

    # Initialize ImageKit
    imagekit = ImageKit(
        private_key=image_kit_configuration_obj.private_key,
        public_key=image_kit_configuration_obj.public_key,
        url_endpoint=image_kit_configuration_obj.url_endpoint
    )

    # Create upload options with folder path
    options = UploadFileRequestOptions(
        folder=folder_path,
        use_unique_file_name=True,  # Ensures unique filenames to prevent overwriting
        tags=["articleInnovator", "imageGen"]  # Tags for organization
    )

    # Base64 encoded image string
    base64_string = base64_strings  # Replace with your actual base64 string

    # Upload the image
    upload_response = imagekit.upload_file(
        file=base64_string,  # Base64 string
        file_name=workspace_id.name,  # File name to store in ImageKit
        options=options
        
    )

    print(upload_response,'upload_response')
    # Print the response URL
    print("Uploaded Image URL:", upload_response.url)
    return  upload_response.url


