
from rest_framework import status
from imagekitio import ImageKit
from django.conf import settings
from django.http import JsonResponse
from apiApp.models import image_kit_configuration
import json, io, os, base64
from imagekitio.models import UploadFileRequestOptions
from PIL import Image
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

def upload_to_imagekit(image, file_name, slug_id, workspace_name):
    # Set the specific folder path
    folder_path = f"articleInnovator/template/{workspace_name}"
    
    try:
        print(f'Starting ImageKit upload process to folder: {folder_path}')

        # Fetch ImageKit configuration based on slug_id
        try:
            config = image_kit_configuration.objects.get(slug_id=slug_id)
        except image_kit_configuration.DoesNotExist:
            return None, "ImageKit configuration not found."

        print(f"ImageKit config found: {config.url_endpoint}")

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
            
        print(image, '909')
        
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
        print(f"Uploading {file_name} to ImageKit folder: {folder_path}")
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

        print(f"Image uploaded successfully to {folder_path}: {image_url}")
        return image_url, None  # Return the image URL on success

    except Exception as e:
        error_message = f"Error during ImageKit upload to {folder_path}: {str(e)}"
        print(error_message)
        return None, error_message