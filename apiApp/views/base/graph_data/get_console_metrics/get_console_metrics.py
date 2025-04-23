from django.http import JsonResponse
from django.db.models import Q, Sum
from django.core.serializers import serialize
import json
from apiApp.models import console_metrics, domain, workspace
from rest_framework.decorators import api_view


# # Helper function to fetch metrics and aggregate data
# def get_console_metrics(queryset):
#     if not queryset.exists():
#         return None

#     aggregates = queryset.aggregate(
#         total_clicks=Sum('clicks'),
#         total_impressions=Sum('impression'),
#         total_ctr=Sum('ctr'),
#         total_position=Sum('position')
#     )

#     metrics_by_date = {
#         'clicks': queryset.values('date').annotate(total=Sum('clicks')).order_by('date'),
#         'impressions': queryset.values('date').annotate(total=Sum('impression')).order_by('date'),
#         'ctr': queryset.values('date').annotate(total=Sum('ctr')).order_by('date'),
#         'position': queryset.values('date').annotate(total=Sum('position')).order_by('date'),
#     }

#     metrics_by_date_dict = {
#         key: {record['date'].isoformat(): record['total'] for record in value}
#         for key, value in metrics_by_date.items()
#     }
    
#     print(metrics_by_date,'metrics_by_date')
#     print(aggregates,'aggregates')

#     return {
#         'aggregates': {
#             'total_clicks': aggregates.get('total_clicks', 0),
#             'total_impressions': aggregates.get('total_impressions', 0),
#             'total_ctr': aggregates.get('total_ctr', 0),
#             'total_position': aggregates.get('total_position', 0),
#         },
#         'metrics_by_date': metrics_by_date_dict,
#         # 'raw_data': serialize('json', queryset),
#     }



from datetime import datetime
from django.db.models import Sum

def get_console_metrics(queryset):
    if not queryset.exists():
        return None

    def calculate_percentage_change(start, end):
        if start == 0:
            return 0
        return round(((end - start) / start) * 100, 2)

    def get_trend(change):
        return "up" if change >= 0 else "down"

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
    
    
    print(metrics_by_date,'metrics_by_date')
    print(len(metrics_by_date),'metrics_by_date')

    # Get first and last date from queryset
    ordered_dates = sorted(set(queryset.values_list('date', flat=True)))
    start_date = ordered_dates[0] if ordered_dates else None
    end_date = ordered_dates[-1] if ordered_dates else None

    percentage_diff = {}
    if start_date and end_date:
        for metric, values in metrics_by_date.items():
            start_value = next((item['total'] for item in values if item['date'] == start_date), 0)
            end_value = next((item['total'] for item in values if item['date'] == end_date), 0)
            change = calculate_percentage_change(start_value, end_value)
            percentage_diff[f'{metric}_change'] = {
                "value": change,
                "trend": get_trend(change)
            }

    print(percentage_diff, 'percentage_diff')

    return {
        'aggregates': {
            'total_clicks': aggregates.get('total_clicks', 0),
            'total_impressions': aggregates.get('total_impressions', 0),
            'total_ctr': aggregates.get('total_ctr', 0),
            'total_position': aggregates.get('total_position', 0),
        },
        'metrics_by_date': metrics_by_date_dict,
        'percentage_data': percentage_diff,
    }
