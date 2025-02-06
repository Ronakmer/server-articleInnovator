from django.http import JsonResponse
from django.db.models import Q, Sum
from django.core.serializers import serialize
import json
from apiApp.models import console_metrics, domain, workspace
from rest_framework.decorators import api_view


# Helper function to fetch metrics and aggregate data
def get_console_metrics(queryset):
    if not queryset.exists():
        return None

    aggregates = queryset.aggregate(
        total_clicks=Sum('clicks'),
        total_impressions=Sum('impression'),
        total_ctr=Sum('ctr'),
        total_position=Sum('position')
    )

    metrics_by_date = {
        'clicks': queryset.values('date').annotate(total=Sum('clicks')).order_by('date'),
        'impressions': queryset.values('date').annotate(total=Sum('impression')).order_by('date'),
        'ctr': queryset.values('date').annotate(total=Sum('ctr')).order_by('date'),
        'position': queryset.values('date').annotate(total=Sum('position')).order_by('date'),
    }

    metrics_by_date_dict = {
        key: {record['date'].isoformat(): record['total'] for record in value}
        for key, value in metrics_by_date.items()
    }

    return {
        'aggregates': {
            'total_clicks': aggregates.get('total_clicks', 0),
            'total_impressions': aggregates.get('total_impressions', 0),
            'total_ctr': aggregates.get('total_ctr', 0),
            'total_position': aggregates.get('total_position', 0),
        },
        'metrics_by_date': metrics_by_date_dict,
        # 'raw_data': serialize('json', queryset),
    }


