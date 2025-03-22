
import requests
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from imagekitio import ImageKit
import json, io, os, base64
from imagekitio.models import UploadFileRequestOptions
from PIL import Image
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from apiApp.models import workspace


@api_view(['POST'])
def verify_image_kit_configuration(request):
    try:
        private_key = request.data.get("private_key")
        public_key = request.data.get("public_key")
        url_endpoint = request.data.get("url_endpoint")

        if not all([public_key, private_key, url_endpoint]):
            return JsonResponse({
                "error": "Missing required parameters. Please provide public key, private key, and url endpoint.",
                "success": False,
            }, status=400)

        imagekit = ImageKit(
            private_key=private_key,
            public_key=public_key,
            url_endpoint=url_endpoint
        )

        try:
            _ = imagekit.list_files()
            return JsonResponse({
                "message": 'success',
                "success": True,
            }, status=200)
        except Exception as e:
            print("API Verification Failed:", str(e))
            return JsonResponse({"error": f"API verification failed","success": False}, status=400)

    
    except Exception as e:
        print("This error is verify_image_kit_configuration --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)




