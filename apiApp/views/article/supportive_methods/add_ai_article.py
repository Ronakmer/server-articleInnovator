import base64
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from apiApp.models import domain, workspace, article_type, wp_author, wp_category, wp_tag, article, prompt
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
import json


def add_ai_article(request_user, request_data):
    try:
        print('ai')
        print(request_data)

        # Step 1: Collect basic data from request
        data = {
            "article_type_slug_id": request_data.get('article_type_slug_id'),
            "domain_slug_id": request_data.get('domain_slug_id'),
            "workspace_slug_id": request_data.get('workspace_slug_id'),
            "wp_status": request_data.get('wp_status'),
            "prompt_slug_id": request_data.get('prompt_slug_id'),
            "url": request_data.get('url'),
            "keyword": request_data.get('keyword'),
            "ai_content_flags": request_data.get('ai_content_flags'),
            "article_priority": request_data.get('article_priority'),
            # "is_category_selected_by_ai": request_data.get('is_category_selected_by_ai'),
            # "is_category_generated_by_ai": request_data.get('is_category_generated_by_ai'),
            # "is_tag_selected_by_ai": request_data.get('is_tag_selected_by_ai'),
            # "is_tag_generated_by_ai": request_data.get('is_tag_generated_by_ai'),
            # "is_author_selected_by_ai": request_data.get('is_author_selected_by_ai'),
            # "is_meta_description_generated_by_ai": request_data.get('is_meta_description_generated_by_ai'),
            # "is_meta_keyword_generated_by_ai": request_data.get('is_meta_keyword_generated_by_ai'),
            # "is_meta_title_generated_by_ai": request_data.get('is_meta_title_generated_by_ai'),
            # "is_internal_links_generated_by_ai": request_data.get('is_internal_links_generated_by_ai'),
            # "is_external_links_generated_by_ai": request_data.get('is_external_links_generated_by_ai'),
        }

        # Step 2: Handle wp_schedule_time separately
        wp_schedule_time = request_data.get("wp_schedule_time")
        if data["wp_status"] == "future":
            if not wp_schedule_time:
                return {"error": "wp_schedule_time is required when wp_status is future", "success": False}
            data["wp_schedule_time"] = wp_schedule_time
        else:
            wp_schedule_time = None

        print(data, 'data')

        # Step 3: Validate required fields (excluding keyword and url which will be validated separately)
        required_fields = ["article_type_slug_id", "domain_slug_id", "workspace_slug_id", "wp_status", "prompt_slug_id"]
        missing_fields = [field for field in required_fields if data.get(field) is None or data.get(field) == ""]
        if missing_fields:
            return {"error": f"Missing required fields: {', '.join(missing_fields)}", "success": False}

        # Step 4: Fetch article type to determine validation rules
        try:
            article_type_obj = article_type.objects.get(slug_id=data["article_type_slug_id"])
        except article_type.DoesNotExist:
            return {"error": "Article type not found.", "success": False}

        # Step 5: Validate keyword and url based on article type category
        if article_type_obj.category == 'keyword':
            if not data.get("keyword"):
                return {"error": "Keyword is required for this article type.", "success": False}
            # URL is not required for keyword type, so set it to empty if not provided
            data["url"] = ""
        elif article_type_obj.category == 'url':
            if not data.get("url"):
                return {"error": "URL is required for this article type.", "success": False}
            # Keyword is not required for url type, so set it to empty if not provided
            data["keyword"] = ""
        else:
            return {"error": "Invalid article type category.", "success": False}

        # Check if both keyword and url are passed
        if data.get("keyword") and data.get("url"):
            return {"error": "Please pass only one value: either a keyword or a URL.", "success": False}

        # Step 6: Fetch related model objects
        try:
            domain_obj = domain.objects.get(slug_id=data["domain_slug_id"])
            workspace_obj = workspace.objects.get(slug_id=data["workspace_slug_id"])
            prompt_obj = prompt.objects.get(slug_id=data["prompt_slug_id"])
        except domain.DoesNotExist:
            return {"error": "Domain not found.", "success": False}
        except workspace.DoesNotExist:
            return {"error": "Workspace not found.", "success": False}
        except prompt.DoesNotExist:
            return {"error": "Prompt not found.", "success": False}

        category_ids = []
        tag_ids = []
        
        category_names = []
        tag_names = []
        
        wp_author_obj=None
        print(prompt_obj.supportive_prompt_json_data,'xdsd2341')
        
        supportive_prompt_data = prompt_obj.supportive_prompt_json_data
        print(supportive_prompt_data.get('supportive_prompt_category_selected_by_ai_id'),'23211111111111')
        
        ai_content_flags = request_data.get('ai_content_flags')
        ai_content_flags = json.loads(ai_content_flags)
        
        if not ai_content_flags.get("is_wp_categories_selected_by_ai", False):
            print(request_data.get("category_slug_id"),'000000000000000000')
            category_slugs = request_data.get("category_slug_id")
            if category_slugs:
                category_slug_list = category_slugs.split(",")
                category_objs = wp_category.objects.filter(slug_id__in=category_slug_list)

                # Get category names and list of objects
                category_names = [cat.name for cat in category_objs]
                category_ids = list(category_objs)
            else:
                return {"error": "Missing required category", "success": False}

        print(category_ids,'category_idsxxx')

        # Handle tag selection
        if not ai_content_flags.get("is_wp_tags_selected_by_ai", False):
            print(request_data.get("tag_slug_id"),'000000000000000000')
            
            tag_slugs = request_data.get("tag_slug_id")
            if tag_slugs:
                tag_slug_list = tag_slugs.split(",")
                tag_objs = wp_tag.objects.filter(slug_id__in=tag_slug_list)

                tag_names = [tag.name for tag in tag_objs]
                tag_ids = list(tag_objs)
            else:
                return {"error": "Missing required tag", "success": False}

        # Handle author selection
        if not ai_content_flags.get("is_wp_authors_selected_by_ai", False):
            print(request_data.get("author_slug_id"),'000000000000000000')
            
            author_slug = request_data.get("author_slug_id")
            if author_slug:
                try:
                    wp_author_obj = wp_author.objects.get(slug_id=author_slug)
                except wp_author.DoesNotExist:
                    return {"error": "Author not found.", "success": False}
            else:
                return {"error": "Missing required author", "success": False}




        print(data["wp_status"] ,'data["wp_status"] ')
        
        ai_content_flags_raw = data.get("ai_content_flags", "{}")

        # Step 7: Save the article object
        article_obj = article.objects.create(
            article_status=data.get("article_status", "initiate"), 
            article_priority=data.get("article_priority"), 
            ai_content_flags=json.loads(ai_content_flags_raw),
            wp_status=data["wp_status"] if data["wp_status"] in dict(article.WP_STATUS_CHOICES) else None,
            wp_schedule_time=wp_schedule_time if data["wp_status"] == 'future' else None,
            article_type_id=article_type_obj,
            domain_id=domain_obj,
            workspace_id=workspace_obj,
            prompt_id=prompt_obj,
            url=data["url"],
            keyword=data["keyword"],
            wp_author_id = wp_author_obj if wp_author_obj else None,
            # is_category_selected_by_ai = str_to_bool(data.get("is_category_selected_by_ai", True)),
            # is_category_generated_by_ai = str_to_bool(data.get("is_category_generated_by_ai", True)),
            # is_tag_selected_by_ai = str_to_bool(data.get("is_tag_selected_by_ai", True)),
            # is_tag_generated_by_ai = str_to_bool(data.get("is_tag_generated_by_ai", True)),
            # is_author_selected_by_ai = str_to_bool(data.get("is_author_selected_by_ai", True)),
            # is_meta_description_generated_by_ai = str_to_bool(data.get("is_meta_description_generated_by_ai", True)),
            # is_meta_keyword_generated_by_ai = str_to_bool(data.get("is_meta_keyword_generated_by_ai", True)),
            # is_meta_title_generated_by_ai = str_to_bool(data.get("is_meta_title_generated_by_ai", True)),
            # is_internal_links_generated_by_ai = str_to_bool(data.get("is_internal_links_generated_by_ai", True)),
            # is_external_links_generated_by_ai = str_to_bool(data.get("is_external_links_generated_by_ai", True)),
            created_by=request_user
        )
        
        # ✅ Assign ManyToMany fields AFTER saving
        if category_ids:
            article_obj.wp_category_id.set([cat.pk for cat in category_ids])  # .set() expects a list of IDs or objects

        if tag_ids:
            article_obj.wp_tag_id.set([tag.pk for tag in tag_ids])

        return {"message": "Data added successfully.", "success": True, "article_slug_id": article_obj.slug_id}

    except Exception as e:
        print("Unexpected error in add_ai_article:", e)
        return {"error": f"Internal server error: {str(e)}", "success": False}
    
    
    
    
    
    
# def str_to_bool(val):
#     return str(val).lower() == 'true'
