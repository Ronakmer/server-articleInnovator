
import os
# import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "articleInnovator.settings")
# django.setup()  # Initialize Django before importing models

from django.http import JsonResponse
import json
import random
import requests
import subprocess
from PIL import Image
from pebble import ProcessPool
from apiApp.models import image_tag, image_template, image_template_category, image_kit_configuration, workspace
from rest_framework.decorators import api_view
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import threading
from concurrent.futures import ThreadPoolExecutor
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from django.db.models import Q
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

GENERATE_IMAGE_LAMBDA_URL = os.getenv("GENERATE_IMAGE_LAMBDA_URL")
from django.conf import settings


    
def get_generated_images_json_data(templates, data):
    urls = json.loads(data["image_urls"])
    print(urls)
    no_of_images = int(data["no_of_images"])
    
    # Keep all templates
    valid_templates = templates.copy()
    
    # Generate the requested number of images
    result = []
    current_url_index = 0  # Starting URL index
    url_shift = 0  # Track URL shifts for each cycle through all templates
    
    for i in range(no_of_images):
        # Use templates in a circular fashion if needed
        template_index = i % len(valid_templates)
        template = json.loads(valid_templates[template_index])
        # If we've gone through all templates, increment the URL shift for the next cycle
        if template_index == 0 and i > 0:
            url_shift += 1
        # print(template)

        # Extract image objects and sort them by the numeric part of layerImageCategory
        image_objects = []
        non_image_objects = []
        
        for obj in template["objects"]:
            if "layerImageCategory" in obj and obj["layerImageCategory"].startswith("image_"):
                image_objects.append(obj)
            else:
                non_image_objects.append(obj)
        
        # Sort image objects by the numeric part of the category
        def get_image_number(obj):
            try:
                # Extract number from "image_X"
                return int(obj["layerImageCategory"].split("_")[1])
            except (IndexError, ValueError):
                return float('inf')  # Place objects with invalid numbers at the end
        
        image_objects.sort(key=get_image_number)
        
        # # Fill in src URLs for image objects with proper circular pattern
        for idx, obj in enumerate(image_objects):
            # Apply url_shift to create the circular pattern
            assigned_url_index = (idx + url_shift) % len(urls)
            template["objects"][idx]["src"] = urls[assigned_url_index]
        

        result.append(template)
    
    return result





@api_view(['POST'])
def generate_single_image(request):
    try:
        # DRF's request.data is already parsed from JSON
        json_data = request.data
        no_of_images = int(json_data.get('no_of_images', 1))  
        workspace_slug_id = json_data.get('workspace_slug_id')
        search_query = json_data.get('search_query')

        print(search_query,'search_query')
        
        file_name =  search_query.strip().replace(" ", "_")

        print(file_name,'file_name')
        
        # tag_names = json_data.get('tags')
        tag_names = json.loads(json_data.get('tags', '[]')) 
        category_names = json.loads(json_data.get('categories', '[]'))  

        # image_urls = json.loads(json_data['image_urls'])
        image_urls = json.loads(json_data.get('image_urls', '[]')) 
        
        if tag_names:
            tags = image_tag.objects.filter(name__in=tag_names)
        if category_names:
            categories = image_template_category.objects.filter(name__in=category_names)


        if tag_names and (not tags or not tags.exists()):
            return JsonResponse({"success": False, "message": "Didn't find matching tags"}, status=404)

        if category_names and (not categories or not categories.exists()):
            return JsonResponse({"success": False, "message": "Didn't find matching categories"}, status=404)
        
        
        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found ","success": False}, status=404)

        
        # Get templates related to these tags - use a more targeted approach
        template_sets = []
        if tag_names:
            for tag in tags:
                tag_templates = image_template.objects.filter(image_tag_id=tag, status='active')

                if tag_templates:
                    template_sets.append(list(tag_templates))
                    
        if category_names:
            for category in categories:
                category_templates = image_template.objects.filter(image_template_category_id=category, status='active')

                if category_templates:
                    template_sets.append(list(category_templates))
                    
        
        
        if not template_sets:
            return JsonResponse({"success": False, "message": "No templates found for the given tags"}, status=404)
        
        # Select templates, ensuring diversity if multiple tags
        templates_list = []
        for i in range(min(no_of_images, len(template_sets))):
            # Select a random template from each set to ensure diversity
            template = random.choice(template_sets[i % len(template_sets)])
            templates_list.append(template.template_json)
        
        # If we need more images than we have tag sets, add random templates
        if no_of_images > len(template_sets):
            all_templates = [t for template_set in template_sets for t in template_set]
            for _ in range(no_of_images - len(template_sets)):
                if all_templates:
                    template = random.choice(all_templates)
                    templates_list.append(template.template_json)
        
        
        generated_images_json_data = get_generated_images_json_data(templates_list, json_data)
        
        workspace_name = workspace_obj.name.strip().replace(" ", "_")


        # Process each image data in the list
        for image_data in generated_images_json_data:
            image_data["workspaceName"] = workspace_name
            image_data["fileName"] = file_name
            
            
            if "imageTags" in image_data:
                # Replace the UUIDs with actual tag names
                tag_slugs = image_data["imageTags"]
                image_data["imageTags"] = [t.name for t in image_tag.objects.filter(slug_id__in=tag_slugs)]
            
            if "imageKit" in image_data:
                # Get the imagekit configuration by slug_id
                imagekit_config = image_kit_configuration.objects.filter(workspace_id=workspace_obj.id, default_section=True).first()
                if imagekit_config:
                    # Replace with the actual configuration details
                    image_data["imageKit"] = {
                        "publicKey": imagekit_config.public_key,
                        "privateKey": imagekit_config.private_key,
                        "urlEndpoint": imagekit_config.url_endpoint
                    }
        
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(generate_image, image_data) for image_data in generated_images_json_data]
            results = [future.result() for future in futures]

        print(results,'results')

        return JsonResponse({
            "success": True, 
            "urls":results,
            "message": f"Image generation started in background for {len(generated_images_json_data)} images."
        }, status=202)
    except Exception as e:
        print("This error is generate_single_image --->: ", e)
        return JsonResponse({"success": False, "message": "Internal Server error."}, status=500)



def generate_image(data):
    try:
        payload = json.dumps({
            "imagekit":data['imageKit'],
            "generated_image_json_data": data,
            "workspace_name":data['workspaceName'],
            "file_name":data['fileName'],
        })
        # print(payload,'payload')
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(GENERATE_IMAGE_LAMBDA_URL, data=payload, headers=headers)

        if response.status_code == 200:
            print(response.json())
            return response.json()

    except Exception as e:
        print("This error is generate_image --->: ", e)


    
    
