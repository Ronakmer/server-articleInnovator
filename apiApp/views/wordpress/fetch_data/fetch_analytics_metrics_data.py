
from django.shortcuts import render,redirect
from apiApp.models import domain, analytics_metrics, workspace, domain_install_log, domain_install_log_percentage
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
import requests
from django.core.serializers import serialize
import base64
from rest_framework.decorators import api_view
from datetime import datetime, timedelta




def process_analytics_metrics(obj_data):
    
    domain_obj = obj_data.get("domain_obj")
    workspace_obj = obj_data.get("workspace_obj")
    
    
    # Domain credentials
    domain_name = domain_obj.name
    username = domain_obj.wordpress_username
    password = domain_obj.wordpress_application_password

    # Add category API URL
    api_url = f'https://{domain_name}/wp-json/botxbyte/v1/analytics-data/'

    credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

    headers = {
        'Accept': 'application/json, */*;q=0.1',
        'Authorization': f"Basic {credentials}",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
        'Connection': 'keep-alive',
    }

    # Calculate start and end date
    today = datetime.today()
    start_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')  # Approximately 3 months ago
    end_date = today.strftime('%Y-%m-%d')


    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    # Using for loop to iterate through dates between start_date and end_date
    date_range = [current_date + timedelta(days=i) for i in range((end_date_obj - current_date).days + 1)]

    for current_date in date_range:
        date_str = current_date.strftime('%Y-%m-%d')

        params = {
            'startDate': date_str,
            'endDate': date_str,
            'metrics': 'activeUsers,newUsers,averageSessionDuration',
            'dimensions': 'date,pagePath',
            'limit': 25000  # Max limit per request
        }

        # Make API request for the current date
        response = requests.get(api_url, params=params, headers=headers)
        
        if response.status_code != 200:
            return "Failed to fetch analytics data from API."

        data = response.json()
        # Check if 'rows' is present in the data
        if 'rows' not in data:
            return "No data available for the requested period or invalid response format."

        total_records = len(data['rows'])

        if total_records == 0:
            # No data for the current date, move to next date
            continue

        # Process the batch of data for the current date
        batch_size = 1000
        for i in range(0, total_records, batch_size):
            batch = data['rows'][i:i + batch_size]

            for row in batch:
                date_value = row["dimensionValues"][0]["value"]
                page_value = row["dimensionValues"][1]["value"]
                active_users = int(row["metricValues"][0]["value"])
                new_users = int(row["metricValues"][1]["value"])
                average_session_duration = float(row["metricValues"][2]["value"])

                # Convert date_value from string to date format
                date_value = datetime.strptime(date_value, "%Y%m%d").date()

                # Check if record exists for the given date
                existing_record_obj = analytics_metrics.objects.filter(date=date_value, domain_id=domain_obj).first()

                # Save or update the record in the database
                if existing_record_obj:
                    existing_record_obj.domain_id = domain_obj
                    existing_record_obj.workspace_id = workspace_obj
                    existing_record_obj.page = page_value
                    existing_record_obj.active_users = active_users
                    existing_record_obj.new_users = new_users
                    existing_record_obj.average_session_duration = average_session_duration
                    existing_record_obj.save()
                else:
                    analytics_metrics_obj = analytics_metrics()
                    analytics_metrics_obj.domain_id = domain_obj
                    analytics_metrics_obj.workspace_id = workspace_obj
                    analytics_metrics_obj.date = date_value
                    analytics_metrics_obj.page = page_value
                    analytics_metrics_obj.active_users = active_users
                    analytics_metrics_obj.new_users = new_users
                    analytics_metrics_obj.average_session_duration = average_session_duration
                    analytics_metrics_obj.save()

                # Log installation progress
                install_log_obj = domain_install_log()
                install_log_obj.log_type = 'analytics metrics'
                install_log_obj.log_text = f"analytics metrics: {page_value}"
                install_log_obj.domain_id = domain_obj
                install_log_obj.save()

                analytics_metrics_progress = 30 / total_records

                percentage_log_obj = domain_install_log_percentage()
                percentage_log_obj.domain_install_log_id = install_log_obj
                percentage_log_obj.log_percentage = analytics_metrics_progress
                percentage_log_obj.domain_id = domain_obj
                percentage_log_obj.save()

    return "analytics metrics add successfully."

    


@api_view(['POST'])
def fetch_analytics_metrics_data(request):
    try:


        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not domain_slug_id:
            return JsonResponse({"error": "Domain slug ID is required.","success": False}, status=400)

        if not workspace_slug_id:
            return JsonResponse({"error": "Workspace slug ID is required.","success": False}, status=400)

        try:
            domain_obj = domain.objects.get(slug_id=domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "Invalid domain.","success": False}, status=404)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Invalid workspace.","success": False}, status=404)

        obj_data={
            "domain_obj":domain_obj,
            "workspace_obj":workspace_obj,
        }
        
        result = process_analytics_metrics(obj_data)
        if "Failed" in result:
            return JsonResponse({"error": result,"success": False}, status=500)
        
        return JsonResponse({'message': result,"success": True}, status=200)

            
    except Exception as e:
        print("This error is fetch_analytics_metrics_data --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


