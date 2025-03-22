
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "articleInnovator.settings")
django.setup()  # Initialize Django before importing models


from django.http import JsonResponse
import json
import random
import requests
import subprocess
from PIL import Image
from multiprocessing import Manager
from pebble import ProcessPool
import uuid
from django.conf import settings
from apiApp.models import image_tag, image_template, image_template_category, image_kit_configuration
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging
import io
import base64
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

logger = logging.getLogger(__name__)

class ImageGenerator:
    
    def get_all_templates_by_tags(json_data):
        try:
            # Get tags info
            tag_names = json_data['tags']
            tags = image_tag.objects.filter(name__in=tag_names)
            print(tags,'00000000000xxxxxxxxxxxxxxxxxxx')
            if not tags:
                logger.error("Didn't find tags")
                return {"success": False, "message": "Didn't find tags"}
            
            # Get templates related to these tags
            templates = image_template.objects.filter(image_tag_id__in=tags, status='active')
            print(templates,'11111111111111111111555555555555555')
            
            if not templates:
                logger.error("No templates found for the given tags")
                return {"success": False, "message": "No templates found for the given tags"}
            
            # Convert QuerySet to list of dictionaries for consistent processing
            templates_list = []
            for template in templates:
                templates_list.append({
                    'template_id': template.id,
                    'name': template.name,
                    'template_json': template.template_json,
                    'template_image_path': template.template_image_path,
                    'status': template.status,
                    'slug_id': template.slug_id
                })
                print('00000000000000000000000000000000')
            
            return {"success": True, "message": templates_list}
        except Exception as ex:
            logger.error(ex)
            return {"success": False, "message": str(ex)}
    
    
    def create_circular_templates_info(templates_info, number):
        # Convert number to integer to ensure proper comparison
        number = int(number) if isinstance(number, str) else number
        
        # If templates_info doesn't have enough elements, use circular array
        if len(templates_info) < number:
            templates_info = (templates_info * number)[:number]
        else:
            templates_info = templates_info[:number]
        # Shuffle templates_info
        random.shuffle(templates_info)
        print('1111111111111111111111111111111')
        
        return templates_info
    
    
    def create_circular_keywords(keyword_with_original_image_url, template_image_count):
        # Convert template_image_count to integer if it's a string
        template_image_count = int(template_image_count) if isinstance(template_image_count, str) else template_image_count
        
        # Create circular keyword list if needed
        keyword_count = len(keyword_with_original_image_url)
        if keyword_count < template_image_count:
            circular_kwoiu = (keyword_with_original_image_url * template_image_count)[:template_image_count]
        else:
            circular_kwoiu = keyword_with_original_image_url[:template_image_count]
        return circular_kwoiu

    
    def upload_image_to_imagekit(original_image_url, keyword, workspace_id=None):
        """
        Upload an image to ImageKit using the provided configuration
        """
        try:
            # Download the image from the URL
            response = requests.get(original_image_url, stream=True)
            if not response.ok:
                logger.error(f"Failed to download image from {original_image_url}")
                return None
            
            # Open the image using PIL
            image = Image.open(response.raw)
            
            # Get workspace name from workspace_id if provided
            workspace_name = "default"
            if workspace_id:
                try:
                    from apiApp.models import workspace
                    workspace_obj = workspace.objects.get(id=workspace_id)
                    workspace_name = workspace_obj.name
                except Exception as e:
                    logger.warning(f"Could not find workspace name for ID {workspace_id}: {str(e)}")
            
            # Generate a unique filename
            file_name = f"{keyword}_{random.randint(1000, 9999)}.png"
            
            # Get the first ImageKit configuration from the database
            config = image_kit_configuration.objects.first()
            if not config:
                logger.error("No ImageKit configuration found in database")
                return None
                
            # Upload the image to ImageKit
            image_url, error = upload_to_imagekit(image, file_name, config.slug_id, workspace_name)
            
            if error:
                logger.error(f"ImageKit upload error: {error}")
                return None
                
            return image_url
        except Exception as ex:
            logger.error(f"Error in upload_image_to_imagekit: {str(ex)}")
            return None

    
    def get_imagekit_urls(keyword, original_image_url, workspace_id=None):
        logger.debug("get_imagekit_urls")
        try: 
            imagekit_url = ImageGenerator.upload_image_to_imagekit(original_image_url, keyword, workspace_id)
            logger.info(f"ImageKit URL: {imagekit_url}")
            print('444444444444444444444444444444444444444444')
            return imagekit_url or original_image_url  # Fall back to original URL if ImageKit fails
        except Exception as ex: 
            logger.error(ex)
            return original_image_url  # Fall back to original URL on error

    
    def generate_image(template_file_name):
        """ Calls the Node.js script to generate an image and returns the output """
        
        print(f"Processing template: {template_file_name}")

        try:
            # Run Node.js script and capture output
            result = subprocess.run(
                ["node", "generate_image.js", template_file_name],
                capture_output=True,
                text=True,
                check=True
            )

            # Extract output and process
            output = result.stdout.strip().split()[0] if result.stdout.strip() else None

            print(f"Generated Image: {output}")
            print('555555555555555555555555555555')
            return output
        except subprocess.CalledProcessError as e:
            print(f"Error running Node.js script: {e}")
            return None



    
    def process_template(template, keyword_with_original_image_url, used_orignal_image_url, workspace_id=None):
        try:
            logger.debug("process_template")
            print('starttttttttttttttttttttttttttttttttttttttttttttttt')

            template_json = json.loads(template['template_json'])
            template_image_count = sum(1 for tj in template_json['objects'] if "layerImageCategory" in tj and tj['layerImageCategory'])
            template_text_count = sum(1 for tj in template_json['objects'] if "layerTextCategory" in tj and tj['layerTextCategory'])

            circular_keyword_with_original_image_url = ImageGenerator.create_circular_keywords(
                keyword_with_original_image_url, template_image_count
            )
            imagekit_urls = []
            
            for ckwoiu in circular_keyword_with_original_image_url:
                keyword = ckwoiu['keyword']
                original_image_urls = ckwoiu['original_image_urls']
                for original_image_url in original_image_urls:
                    if original_image_url not in used_orignal_image_url:
                        used_orignal_image_url.append(original_image_url)
                        imagekit_url = ImageGenerator.get_imagekit_urls(keyword, original_image_url, workspace_id)

                        # Check if the imagekit_url has a valid image using PIL
                        try:
                            response = requests.get(imagekit_url, stream=True)
                            response.raw.decode_content = True
                            image = Image.open(response.raw)
                            image_size_width = image.size[0]
                        except Exception as e:
                            logger.error(f"Failed to open image from url {imagekit_url}: {e}")
                            image = None

                        if image:
                            imagekit_urls.append(imagekit_url)
                            break

            # Update template objects with image URLs
            try:
                counter = 0
                for obj in template_json['objects']:
                    if "layerImageCategory" in obj and obj['layerImageCategory']:
                        if counter < len(imagekit_urls):  # Check if we have enough image URLs
                            imagekit_url = imagekit_urls[counter]
                            # Ensure width and height are integers
                            width = round(float(obj['width']) * float(obj['scaleX']))
                            height = round(float(obj['height']) * float(obj['scaleY']))
                            imagekit_url = imagekit_url.rsplit("/", 1)[0] + \
                                        f"/tr:w-{width},h-{height},fo-auto" + \
                                        "/" + imagekit_url.rsplit("/", 1)[1]
                            
                            obj['width'] = width
                            obj['height'] = height
                            obj['scaleX'] = 1
                            obj['scaleY'] = 1
                            obj['src'] = imagekit_url
                            counter += 1
                        else:
                            logger.warning("Not enough image URLs for template objects")
            except Exception as ex:
                logger.error(f"Error updating template objects: {str(ex)}")

            # Create static folder if it doesn't exist
            static_dir = os.path.join(settings.BASE_DIR, 'static', 'generated_json')
            os.makedirs(static_dir, exist_ok=True)
            
            # Generate templates.json file with random name
            file_name = os.path.join(static_dir, f"{str(random.randint(1000, 9999))}_templates.json")
            
            with open(file_name, 'w') as outfile:
                json.dump([template_json], outfile)
            
            print(file_name,'0000000xxxxxxxxxxxxx')
            generated_image = ImageGenerator.generate_image(file_name)
            print('3333333333333333333333333333333333333333333333333333')
            return generated_image
        except Exception as ex:
            logger.error(f"Error in process_template: {str(ex)}")
        return None
 
    
    def process_template_done(generated_images):
        def callback(future):
            try:
                generated_image = future.result()
                if generated_image:
                    generated_images.append(generated_image)
                    logger.info(f"Generated - {generated_image}")
            except TimeoutError as error:
                logger.error(f"Function took longer than {error.args[1]} seconds")
            except Exception as error:
                logger.error(f"Function raised {error}")
                logger.error(error)
            print('66666666666666666666666666666666666666')
        return callback


# Using your upload_to_imagekit function as provided
def upload_to_imagekit(image, file_name, slug_id, workspace_name):
    # Set the specific folder path
    folder_path = f"articleInnovator/imageGen/{workspace_name}"
    
    try:
        logger.info(f'Starting ImageKit upload process to folder: {folder_path}')

        # Fetch ImageKit configuration based on slug_id
        try:
            config = image_kit_configuration.objects.get(slug_id=slug_id)
        except image_kit_configuration.DoesNotExist:
            return None, "ImageKit configuration not found."

        logger.info(f"ImageKit config found: {config.url_endpoint}")

        # Initialize ImageKit
        imagekit = ImageKit(
            private_key=config.private_key,
            public_key=config.public_key,
            url_endpoint=config.url_endpoint
        )
        
        # Convert PIL Image to binary content using base64
        file_content = io.BytesIO()
        if not isinstance(image, Image.Image):
            return None, "Invalid image object. Please provide a PIL Image object."
            
        logger.debug(f"Image format: {image.format}")
        
        if image.format != 'PNG':
            image = image.convert('RGB')  # Convert to RGB format if it's not PNG
        
        image.save(file_content, format='PNG')
        file_content.seek(0)
        
        # Convert to base64 encoded string
        binary_file = base64.b64encode(file_content.read())
        
        # Create upload options with folder path
        options = UploadFileRequestOptions(
            folder=folder_path,
            use_unique_file_name=True,  # Ensures unique filenames to prevent overwriting
            tags=["articleInnovator", "imageGen"]  # Tags for organization
        )

        # Upload the base64 encoded image to ImageKit
        logger.info(f"Uploading {file_name} to ImageKit folder: {folder_path}")
        upload_result = imagekit.upload_file(
            file=binary_file,
            file_name=file_name,
            options=options
        )

        if not upload_result:
            return None, "ImageKit upload failed: No result returned."

        # Check if the upload result contains the URL
        if hasattr(upload_result, 'url'):
            image_url = upload_result.url
        else:
            return None, "ImageKit upload failed: URL not found in response."

        logger.info(f"Image uploaded successfully to {folder_path}: {image_url}")
        return image_url, None  # Return the image URL on success

    except Exception as e:
        error_message = f"Error during ImageKit upload to {folder_path}: {str(e)}"
        logger.error(error_message)
        return None, error_message



@api_view(['POST'])
def generate_single_image(request):
    try:
        # DRF's request.data is already parsed from JSON
        json_data = request.data
        no_of_images = int(json_data.get('no_of_images', 1))  # Convert to int to ensure proper comparison
        workspace_id = json_data.get('workspace_id')

        # Get all templates
        templates_info = ImageGenerator.get_all_templates_by_tags(json_data)
        if not templates_info['success']:
            return Response({"success": False, "message": templates_info['message']})
            
        templates_info = templates_info['message']
        # Create circular templates and keywords
        circular_templates_info = ImageGenerator.create_circular_templates_info(templates_info, no_of_images)

        with Manager() as manager:
            print(manager,'1111111111111111111111111110000')
            
            used_orignal_image_url = manager.list()

            # Make sure image_url is a list
            image_urls = json_data['image_url']
            if not isinstance(image_urls, list):
                image_urls = [image_urls]

            keyword_with_original_image_url = [
                {
                    "original_image_urls": image_urls,
                    "keyword": json_data.get('keyword', "image")
                }
            ]

            generated_images = manager.list()

            
            with ProcessPool(max_workers=5, max_tasks=10) as pool:
                for template in circular_templates_info:
                    try:
                        TIMEOUT_SECONDS = 100
                        future = pool.schedule(
                            ImageGenerator.process_template,
                            args=(template, keyword_with_original_image_url, used_orignal_image_url, workspace_id),
                            timeout=TIMEOUT_SECONDS
                        )
                        callback = ImageGenerator.process_template_done(generated_images)
                        future.add_done_callback(callback)
                    except Exception as ex:
                        logger.error(ex)
                        
            return Response({"success": True, "message": list(generated_images)})
    except Exception as error:
        logger.error(f"An error occurred: {str(error)}")
        return Response({"success": False, "message": str(error)})
        
    return Response({"success": False, "message": "Unexpected Errors."})

