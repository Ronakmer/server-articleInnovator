from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import uuid



# generate user api key
@api_view(['POST'])
def generate_user_api_key(request):
    try:
        random_uuid = str(uuid.uuid4())
        # print(random_uuid)
        
        return JsonResponse({
            "message": "Generate api key successfully.",
            "invitation_code": random_uuid,
        }, status=200)
       
    except Exception as e:
        print("This error is generate_api_key --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)
