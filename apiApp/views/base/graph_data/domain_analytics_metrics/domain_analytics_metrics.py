
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.core.serializers import serialize
import json
from apiApp.models import analytics_metrics, domain, workspace
from rest_framework.decorators import api_view
from apiApp.views.base.graph_data.get_analytics_metrics.get_analytics_metrics import get_analytics_metrics
from django.utils import timezone
from datetime import datetime


@api_view(['GET'])
def domain_analytics_metrics(request):
    try:
        domain_slug_id = request.GET.get('domain_slug_id', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        if not domain_slug_id or not start_date or not end_date:
            return JsonResponse({'error': 'Missing required parameters.'}, status=400)

        try:
            domain_obj = domain.objects.get(slug_id=domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found.",}, status=404)   

        print(domain_obj,'domain_obj')
        
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)


        queryset = analytics_metrics.objects.filter(
            Q(date__range=(start_date_obj, end_date_obj)) & Q(domain_id=domain_obj)
        )

        print(queryset,'queryset0.0.0')
    
        metrics = get_analytics_metrics(queryset)
        print(metrics,'metrics')
        if not metrics:
            # return JsonResponse({'error': 'No metrics found for the specified domain.'}, status=404)
            return JsonResponse({'metrics_data': None}, status=200)
        
        return JsonResponse({'metrics_data': metrics}, status=200)


    except Exception as e:
        print("This error is domain_analytics_metrics --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)
