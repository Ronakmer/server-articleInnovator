import base64
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from apiApp.models import (domain, workspace, article_type, wp_author, wp_category, wp_tag, article, article_type_field,
supportive_prompt_type, supportive_prompt, prompt, variables)
from django.http import JsonResponse
from apiApp.views.base.s3.article_josn_method.create_article_folder_and_file_s3.create_article_folder_and_file_s3 import create_article_folder_and_file_s3
from apiApp.views.base.s3.article_josn_method.delete_file_from_s3.delete_file_from_s3 import delete_file_from_s3
from apiApp.views.base.s3.article_josn_method.show_file_from_s3.show_file_from_s3 import show_file_from_s3
from django.http import HttpResponse
import json
import uuid, os


def create_input_json(article_slug_id):
    try:
        print('create_input_json')
        article_obj = article.objects.filter(slug_id = article_slug_id)
        
        # Fetch related article_type_fields
        article_type_fields = article_type_field.objects.filter(article_type_id=article_obj.prompt_id.article_type_id)

        input_json = {
            "message": {
                "articl_slug_id": article_obj.slug_id,
                "url": article_obj.url,
                "wp_status": article_obj.wp_status,
                "article_status": article_obj.article_status,
                "wp_schedule_time": article_obj.wp_schedule_time,

                "prompt_id": {
                    "prompt_slug_id": article_obj.prompt_id.slug_id,
                    "prompt_name": article_obj.prompt_id.name,
                    "model": article_obj.prompt_id.ai_rate_model,
                    "prompt_data": article_obj.prompt_id.prompt_data,
                    "wordpress_prompt_json_data": article_obj.prompt_id.wordpress_prompt_json_data,
                    "article_type_id":{
                        "article_type_slug_id": article_obj.prompt_id.article_type_id.slug_id,
                        "category": article_obj.prompt_id.article_type_id.category,
                        "article_category": article_obj.prompt_id.article_type_id.article_category,
                        "article_type_title": article_obj.prompt_id.article_type_id.title,
                        "article_type_description": article_obj.prompt_id.article_type_id.description,
                        "article_type_field_id": [
                            {
                                "article_type_field_slug_id": field.slug_id,
                                "article_type_field_label": field.label,
                                "article_type_field_name": field.name,
                                "article_type_field_name": field.name,
                                "article_type_field_type": field.field_type,
                                "article_type_field_placeholder": field.placeholder,
                                "article_type_field_required": field.required,
                            } for field in article_type_fields
                        ]
                        
                    }
                },
                "domain_id": {
                    "domain_slug_id": article_obj.domain_id.slug_id,
                    "domain_name": article_obj.domain_id.name,
                    "permalinks": article_obj.domain_id.permalinks,
                },
                "workspace_id": {
                    "workspace_slug_id": article_obj.workspace_id.slug_id,
                    "workspace_name": article_obj.workspace_id.name,
                },
            }
        }
        
    
        # Define file path (you can change this)
        file_path = f"input_jsons/{article_slug_id}.json"

        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write JSON to file
        with open(file_path, 'w') as json_file:
            json.dump(input_json, json_file, indent=4)

        # return input_json

    except Exception as e:
        print("Unexpected error in create_input_json:", e)
        return {"error": "Internal server error.", "success": False}






