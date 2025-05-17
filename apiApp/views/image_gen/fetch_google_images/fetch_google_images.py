

from django.http import JsonResponse
from rest_framework.decorators import api_view
# from apiApp.serializers import user_detail_serializer
# from apiApp.models import user_detail, role, workspace
from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
# from apiApp.views.base.dynamic_avatar_image_process.dynamic_avatar_image_process import dynamic_avatar_image_process
# from apiApp.views.base.process_pagination.process_pagination import process_pagination
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_IMAGE_API_KEY = os.getenv('GOOGLE_IMAGE_API_KEY')
GOOGLE_IMAGE_API_URL = os.getenv('GOOGLE_IMAGE_API_URL')






# fetch_google_images
@api_view(['POST'])
def fetch_google_images(request):
    try:
        # Extract query from POST body
        query = request.data.get('query')
        if not query:
            return JsonResponse({"error": "Missing 'query' parameter.", "success": False}, status=400)

        print(GOOGLE_IMAGE_API_KEY,'GOOGLE_IMAGE_API_KEYx')
        print(GOOGLE_IMAGE_API_URL,'GOOGLE_IMAGE_API_URLx')
        print(query,'queryx')
        
        
        # GOOGLE_IMAGE_API_KEYx ='D92B03D0EC80405C8DE89B94F9887C8C'
        # GOOGLE_IMAGE_API_URLx='https://serpapi.com/search.json'
        
        params = {
            'api_key': GOOGLE_IMAGE_API_KEY,
            'search_type': 'images',
            'q': query,
            # 'tbm': 'isch' 
        }

        response = requests.get(GOOGLE_IMAGE_API_URL, params=params)
        response_data = response.json()
        print(response_data,'response_dataz')
        if response.status_code in [200, 201]:
            image_results = response_data.get('image_results', [])
            return JsonResponse({
                "message": "Images fetched successfully.",
                "success": True,
                "data": image_results,
            }, status=200)
        else:
            error_message = response_data.get("error", "Something went wrong while fetching images.")
            return JsonResponse({"error": error_message, "success": False}, status=response.status_code)

    except Exception as e:
        print("This error is fetch_google_images --->: ", e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)
    
    
    
    
# D92B03D0EC80405C8DE89B94F9887C8C GOOGLE_IMAGE_API_KEYx
# https://serpapi.com/search.json GOOGLE_IMAGE_API_URLx
# pizza queryx
# Unauthorized: /api/fetch/google-images/