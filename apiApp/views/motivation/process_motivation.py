from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import motivation_serializer
from apiApp.models import motivation, workspace
from django.db.models import Q
from datetime import date, timedelta


# get motivation
@api_view(['GET'])
def process_motivation(request):
    try:
        request_user = request.user
        
        # Get query parameters
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        
        selected_date = date.today()

        # Initialize filters
        filters = Q(start_date__lte=selected_date, end_date__gte=selected_date)

        if workspace_slug_id:
            try:
                workspace_slug_id = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id=workspace_slug_id)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found.",
                    "success": False,
                }, status=404) 
        
        obj = motivation.objects.filter(filters)
        if not request_user.is_superuser:
            obj = obj.exclude(created_by__is_superuser=True)

        obj = obj.first()
        
        if not obj:
            obj = motivation.objects.filter(filters).first()
    
        print(obj)
        serialized_data = motivation_serializer(obj)
        
        return JsonResponse({
            "data":serialized_data.data,
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is process_motivation --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)

