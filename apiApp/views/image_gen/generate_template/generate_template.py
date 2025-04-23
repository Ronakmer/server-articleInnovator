
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import image_tag_serializer
from apiApp.models import image_tag, workspace
from django.db.models import Q
import base64
import io
from PIL import Image
from django.core.files.base import ContentFile
from imagekitio import ImageKit
from apiApp.views.base.image_kit_method.image_kit_method import upload_to_imagekit

from io import BytesIO
import os


@api_view(['POST'])
def generate_template(request):
    try:
        url_data = request.data.get('img_data')
        template_name = request.data.get('template_name')
        imagekit_slug_id = request.data.get('imagekit_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
        
        print(request.data)


        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found.",
                "success": False,
            }, status=404)
            
        workspace_name = workspace_obj.name      
        # Validate incoming data
        if not url_data or not template_name:
            return JsonResponse({
                "error": "Image URL and template name are required fields.",
                "success": False,
            }, status=400)

        # Decode image data
        try:
            header, encoded = url_data.split(",", 1)
            image_data = base64.b64decode(encoded)
        except Exception as e:
            return JsonResponse({'error': 'Invalid image data format.',"success": False}, status=400)


        # Convert byte data into an image
        try:
            image = Image.open(io.BytesIO(image_data))
            image_path = f"{template_name}.png"  # Use template name for file name
        except Exception as e:
            return JsonResponse({"error": "Failed to process the image.","success": False}, status=415)

        # Upload image to ImageKit
        image_url, error = upload_to_imagekit(image, image_path, imagekit_slug_id, workspace_name)

        if error:
            return JsonResponse({'error': error,"success": False}, status=500)

        # Return uploaded image URL
        return JsonResponse({'image_url': image_url,"success": True}, status=200)

    except Exception as e:
        print(f"Error in generate_template: {e}")
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)








