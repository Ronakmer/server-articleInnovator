from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import console_metrics_serializer
from apiApp.models import console_metrics, domain

# from .serializers import ImageUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from apiApp.views.console_metrics.console_metrics_data import console_metrics_data 
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show console_metrics
@api_view(['GET'])
def list_console_metrics(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        slug_id = request.GET.get('slug_id', None)
        domain_slug_id = request.GET.get('domain_slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        

        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(name__icontains=search)

        if domain_slug_id:
            try:
                domain_obj = domain.objects.get(slug_id=domain_slug_id)
                filters &= Q(domain_id=domain_obj)
            except domain.DoesNotExist:
                return JsonResponse({
                    "error": "domain not found.",
                    "success": False,
                }, status=404) 

        try:
            obj = console_metrics.objects.filter(filters).order_by(order_by)
        except console_metrics.DoesNotExist:
            return JsonResponse({
                "error": "console_metrics not found.",
                "success": False,
            }, status=404) 

        if domain_slug_id:
            console_metrics_data_obj = console_metrics_data(obj)

            if not isinstance(console_metrics_data_obj, dict):
                console_metrics_data_obj = {
                    "data": list(console_metrics_data_obj)  # Convert to list if iterable
                }



        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        
        serialized_data = console_metrics_serializer(obj, many=True)
        
        return JsonResponse({ 
            "console_metrics":serialized_data.data,
            "console_metrics_data_obj": console_metrics_data_obj,
            "success": True,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },            
        }, status=200)

    except Exception as e:
        print("This error is list_console_metrics --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)
