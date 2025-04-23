from django.db.models import Sum
from apiApp.models import console_metrics
from django.http import JsonResponse
from django.db.models import Sum
from datetime import timedelta
from math import floor


# def get_analytics_metrics(queryset):
#     # Aggregate metrics
#     aggregates = queryset.aggregate(
#         total_traffics=Sum('active_users') or 0,
#         total_new_users=Sum('new_users') or 0,
#         total_average_time=Sum('average_session_duration') or 0
#     )

#     # Group metrics by date
#     grouped_data = queryset.values('date').annotate(
#         total_active_users=Sum('active_users'),
#         total_new_users=Sum('new_users'),
#         total_average_time=Sum('average_session_duration')
#     ).order_by('date')

#     # Convert grouped data to dictionaries with string keys
#     traffics_by_date = {record['date'].strftime('%Y-%m-%d'): record['total_active_users'] for record in grouped_data}
#     new_users_by_date = {record['date'].strftime('%Y-%m-%d'): record['total_new_users'] for record in grouped_data}
#     average_time_by_date = {record['date'].strftime('%Y-%m-%d'): record['total_average_time'] for record in grouped_data}






#     # # Calculate percentage change
#     # grouped_list = list(grouped_data)
#     # total_days = len(grouped_list)
#     # if total_days < 2:
#     #     # Not enough data to compare
#     #     percentage_changes = {
#     #         "traffic_change": 0,
#     #         "new_users_change": 0,
#     #         "average_time_change": 0
#     #     }
#     # else:
#     #     half = floor(total_days / 2)
#     #     first_half = grouped_list[:half]
#     #     second_half = grouped_list[half:]

#     #     def sum_field(data, field):
#     #         return sum(item[field] or 0 for item in data)

#     #     first_traffic = sum_field(first_half, 'total_active_users')
#     #     second_traffic = sum_field(second_half, 'total_active_users')

#     #     first_new_users = sum_field(first_half, 'total_new_users')
#     #     second_new_users = sum_field(second_half, 'total_new_users')

#     #     first_avg_time = sum_field(first_half, 'total_average_time')
#     #     second_avg_time = sum_field(second_half, 'total_average_time')

#     #     def calculate_percentage_change(current, previous):
#     #         if previous == 0:
#     #             return 0
#     #         return ((current - previous) / previous) * 100

#     #     percentage_changes = {
#     #         "traffic_change": calculate_percentage_change(second_traffic, first_traffic),
#     #         "new_users_change": calculate_percentage_change(second_new_users, first_new_users),
#     #         "average_time_change": calculate_percentage_change(second_avg_time, first_avg_time)
#     #     }




#     # Split into halves
#     grouped_list = list(grouped_data)
#     total_days = len(grouped_list)
#     if total_days < 2:
#         percentage_changes = {
#             "traffic_change": {"value": 0, "trend": "no_change"},
#             "new_users_change": {"value": 0, "trend": "no_change"},
#             "average_time_change": {"value": 0, "trend": "no_change"}
#         }
#     else:
#         half = floor(total_days / 2)
#         first_half = grouped_list[:half]
#         second_half = grouped_list[half:]

#         def sum_field(data, field):
#             return sum(item[field] or 0 for item in data)

#         first_traffic = sum_field(first_half, 'total_active_users')
#         second_traffic = sum_field(second_half, 'total_active_users')

#         first_new_users = sum_field(first_half, 'total_new_users')
#         second_new_users = sum_field(second_half, 'total_new_users')

#         first_avg_time = sum_field(first_half, 'total_average_time')
#         second_avg_time = sum_field(second_half, 'total_average_time')

#         def calculate_change(current, previous):
#             if previous == 0:
#                 return 0
#             return ((current - previous) / previous) * 100

#         def get_trend(change):
#             if change > 0:
#                 return "up"
#             elif change < 0:
#                 return "down"
#             return "no_change"

#         traffic_change = calculate_change(second_traffic, first_traffic)
#         new_users_change = calculate_change(second_new_users, first_new_users)
#         avg_time_change = calculate_change(second_avg_time, first_avg_time)

#         percentage_changes = {
#             "traffic_change": {"value": traffic_change, "trend": get_trend(traffic_change)},
#             "new_users_change": {"value": new_users_change, "trend": get_trend(new_users_change)},
#             "average_time_change": {"value": avg_time_change, "trend": get_trend(avg_time_change)}
#         }





 

#     print(percentage_changes['traffic_change'],'ssssssssssssssss')
#     print(percentage_changes['new_users_change'],'ssssssssssssssss')
#     print(percentage_changes['average_time_change'],'ssssssssssssssss')





#     # Prepare the response
#     return {
#         'aggregates': aggregates,
#         'traffics_by_date': traffics_by_date,
#         'new_users_by_date': new_users_by_date,
#         'average_time_by_date': average_time_by_date,
#         # 'percentage_data': percentage_changes,
        
#     }















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
    traffics_by_date = {
        record['date'].strftime('%Y-%m-%d'): record['total_active_users'] or 0
        for record in grouped_data
    }
    new_users_by_date = {
        record['date'].strftime('%Y-%m-%d'): record['total_new_users'] or 0
        for record in grouped_data
    }
    average_time_by_date = {
        record['date'].strftime('%Y-%m-%d'): record['total_average_time'] or 0
        for record in grouped_data
    }

    # Calculate percentage change with only 'up' or 'down'
    grouped_list = list(grouped_data)
    total_days = len(grouped_list)

    if total_days < 2:
        percentage_changes = {
            "traffic_change": {"value": 0, "trend": "up"},
            "new_users_change": {"value": 0, "trend": "up"},
            "average_time_change": {"value": 0, "trend": "up"}
        }
    else:
        half = floor(total_days / 2)
        first_half = grouped_list[:half]
        second_half = grouped_list[half:]

        def sum_field(data, field):
            return sum(item[field] or 0 for item in data)

        first_traffic = sum_field(first_half, 'total_active_users')
        second_traffic = sum_field(second_half, 'total_active_users')

        first_new_users = sum_field(first_half, 'total_new_users')
        second_new_users = sum_field(second_half, 'total_new_users')

        first_avg_time = sum_field(first_half, 'total_average_time')
        second_avg_time = sum_field(second_half, 'total_average_time')

        def calculate_change(current, previous):
            if previous == 0:
                return 100  # Assume 100% growth from 0
            return ((current - previous) / previous) * 100

        def get_trend(change):
            return "up" if change >= 0 else "down"

        traffic_change = calculate_change(second_traffic, first_traffic)
        new_users_change = calculate_change(second_new_users, first_new_users)
        avg_time_change = calculate_change(second_avg_time, first_avg_time)

        percentage_changes = {
            "traffic_change": {"value": traffic_change, "trend": get_trend(traffic_change)},
            "new_users_change": {"value": new_users_change, "trend": get_trend(new_users_change)},
            "average_time_change": {"value": avg_time_change, "trend": get_trend(avg_time_change)}
        }

    print(percentage_changes['traffic_change'],'ssssssssssssssss')
    print(percentage_changes['new_users_change'],'ssssssssssssssss')
    print(percentage_changes['average_time_change'],'ssssssssssssssss')


    print(grouped_data,'grouped_data')
    print(aggregates,'aggregates')


    # Prepare the response
    return {
        'aggregates': aggregates,
        'traffics_by_date': traffics_by_date,
        'new_users_by_date': new_users_by_date,
        'average_time_by_date': average_time_by_date,
        'percentage_data': percentage_changes,
    }















