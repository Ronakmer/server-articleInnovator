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
        article_obj = article.objects.filter(slug_id=article_slug_id).first()
        print(article_obj, 'article_objxxxx')
        print(article_obj.prompt_id.article_type_id, 'article_objxxxx')

        # Get the article_type instance directly
        article_type_instance = article_obj.prompt_id.article_type_id
        article_type_id = article_type_instance.id

        # Get all related article_type_fields (ManyToMany relationship)
        article_type_fields = article_type_instance.article_type_field_id.all()

        # Fetch variables using the article_type_id
        variables_data = variables.objects.filter(article_type_id=article_type_id)

        input_json = {
            "message": {
                "article_slug_id": article_obj.slug_id,
                "url": article_obj.url,
                "wp_status": article_obj.wp_status,
                "article_status": article_obj.article_status,
                "wp_schedule_time": article_obj.wp_schedule_time.isoformat() if article_obj.wp_schedule_time else None,

                # "is_category_selected_by_ai": article_obj.is_category_selected_by_ai,
                # "is_category_generated_by_ai": article_obj.is_category_generated_by_ai,
                # "is_tag_selected_by_ai": article_obj.is_tag_selected_by_ai,
                # "is_tag_generated_by_ai": article_obj.is_tag_generated_by_ai,
                # "is_author_selected_by_ai": article_obj.is_author_selected_by_ai,
                # "is_meta_description_generated_by_ai": article_obj.is_meta_description_generated_by_ai,
                # "is_meta_keyword_generated_by_ai": article_obj.is_meta_keyword_generated_by_ai,
                # "is_meta_title_generated_by_ai": article_obj.is_meta_title_generated_by_ai,
                # "is_internal_links_generated_by_ai": article_obj.is_internal_links_generated_by_ai,
                # "is_external_links_generated_by_ai": article_obj.is_external_links_generated_by_ai,

                "wp_author": article_obj.wp_author_id.slug_id if article_obj.wp_author_id else None,
                "wp_category": [cat.slug_id for cat in article_obj.wp_category_id.all()],
                "wp_tag": [tag.slug_id for tag in article_obj.wp_tag_id.all()],

                "prompt": {
                    "slug_id": article_obj.prompt_id.slug_id,
                    "name": article_obj.prompt_id.name,
                    "ai_rate_model": article_obj.prompt_id.ai_rate_model,
                    "prompt_data": article_obj.prompt_id.prompt_data,
                    "supportive_prompt_json_data": article_obj.prompt_id.supportive_prompt_json_data,
                    "article_type": {
                        "slug_id": article_type_instance.slug_id,
                        "category": article_type_instance.category,
                        "article_category": article_type_instance.article_category,
                        "title": article_type_instance.title,
                        "description": article_type_instance.description,
                        "article_type_field": [
                            {
                                "slug_id": field.slug_id,
                                "label": field.label,
                                "name": field.name,
                                "type": field.field_type,
                                "placeholder": field.placeholder,
                                "required": field.required,
                            } for field in article_type_fields
                        ]
                    }
                },
                "variables": [
                    {
                        "slug_id": var.slug_id,
                        "name": var.name,
                        "value": var.value,
                        "required": var.required,
                    } for var in variables_data
                ],
                "domain": {
                    "slug_id": article_obj.domain_id.slug_id,
                    "name": article_obj.domain_id.name,
                    "permalinks": article_obj.domain_id.permalinks,
                },
                "workspace": {
                    "slug_id": article_obj.workspace_id.slug_id,
                    "name": article_obj.workspace_id.name,
                },
            }
        }

        # Define file path (you can change this)
        file_path = f"ai_article_input_jsons/{article_slug_id}.json"
        abs_path = os.path.abspath(file_path)

        print("Saving file to:", abs_path)

        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write JSON to file
        with open(file_path, 'w') as json_file:
            json.dump(input_json, json_file, indent=4, default=str)

        return input_json

    except Exception as e:
        print("Unexpected error in create_input_json:", e)
        return {"error": "Internal server error.", "success": False}
    
    