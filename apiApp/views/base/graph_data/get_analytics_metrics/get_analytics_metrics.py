from django.db.models import Sum
from apiApp.models import console_metrics
from django.http import JsonResponse
from django.db.models import Sum

def get_analytics_metrics(queryset):
    # Aggregate metrics
    aggregates = queryset.aggregate(
        total_traffics=Sum('active_users') or 0,
        total_new_users=Sum('new_users') or 0,
        total_average_time=Sum('average_session_duration') or 0
    )

    # Group metrics by date
    grouped_data = queryset.values('date').annotate(
        total_active_users=Sum('active_users'),
        total_new_users=Sum('new_users'),
        total_average_time=Sum('average_session_duration')
    ).order_by('date')

    # Convert grouped data to dictionaries with string keys
    traffics_by_date = {record['date'].strftime('%Y-%m-%d'): record['total_active_users'] for record in grouped_data}
    new_users_by_date = {record['date'].strftime('%Y-%m-%d'): record['total_new_users'] for record in grouped_data}
    average_time_by_date = {record['date'].strftime('%Y-%m-%d'): record['total_average_time'] for record in grouped_data}

    # Prepare the response
    return {
        'aggregates': aggregates,
        'traffics_by_date': traffics_by_date,
        'new_users_by_date': new_users_by_date,
        'average_time_by_date': average_time_by_date,
    }
