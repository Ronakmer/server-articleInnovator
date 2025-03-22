from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import uuid



# generate invitation code details
@api_view(['POST'])
def generate_invitation_code(request):
    try:
        random_uuid = str(uuid.uuid4())
        # print(random_uuid)
        
        return JsonResponse({
            "message": "Generate invitation code successfully.",
            "data": random_uuid,
            "success": True,
        }, status=200)
       
    except Exception as e:
        print("This error is generate_invitation_code --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)
