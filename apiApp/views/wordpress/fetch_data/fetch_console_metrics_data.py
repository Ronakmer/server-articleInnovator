
from django.shortcuts import render,redirect
from apiApp.models import domain, console_metrics, workspace, domain_install_log, domain_install_log_percentage
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
import requests
from django.core.serializers import serialize
import base64
from rest_framework.decorators import api_view
from datetime import datetime, timedelta


# def process_console_metrics(obj_data):
    
#     # time.sleep(30)
    
#     domain_obj = obj_data.get("domain_obj")
#     workspace_obj = obj_data.get("workspace_obj")
#     request_user = obj_data.get("request_user")
#     print(f"domain_obj: {domain_obj}")
#     print(f"workspace_obj: {workspace_obj}")
        
#     # Domain credentials
#     # domain_name = 'www.wikilistia.com'
#     # username = 'Monty Dhanda'
#     # password = 'Ocxq 6E3x mvJs zDvp UuoD vnnM'
    
#     domain_name = domain_obj.name
#     username = domain_obj.wordpress_username
#     password = domain_obj.wordpress_application_password


#     api_url = f'https://{domain_name}/wp-json/botxbyte/v1/search-console-data/'

#     # Encode credentials
#     credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

#     headers = {
#         'Accept': 'application/json, */*;q=0.1',
#         'Authorization': f"Basic {credentials}",
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
#         'Connection': 'keep-alive',
#     }

#     # Calculate start and end date
#     today = datetime.today()
#     start_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')  # Approximately 3 months ago
#     end_date = today.strftime('%Y-%m-%d')

#     print(f"Fetching data from {start_date} to {end_date}")

#     current_date = datetime.strptime(start_date, '%Y-%m-%d')
#     end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

#     while current_date <= end_date_obj:
#         # Format the current_date for the API request
#         date_str = current_date.strftime('%Y-%m-%d')

#         params = {
#             'startDate': date_str,
#             'endDate': date_str,
#             'dimensions': 'query, page, country, device, date',
#             'limit': 25000,
#         }

#         response = requests.get(api_url, params=params, headers=headers)
#         if response.status_code != 200:
#             # return JsonResponse({'error': f'Failed to fetch data for {date_str}'}, status=500)
#             return "Failed to fetch Console data from API."

#         data = response.json()
#         total_records = len(data)
#         print(f"Processing data for {date_str}, total records: {total_records}")

#         if not data:
#             current_date += timedelta(days=1)
#             continue

#         # Process the data in batches
#         batch_size = 1000
#         for i in range(0, total_records, batch_size):
#             batch = data[i:i + batch_size]
#             for record in batch:
#                 date_filter = record['keys'][4]

#                 existing_record_obj = console_metrics.objects.filter(date=date_filter).first()
#                 if existing_record_obj:
#                     # Update existing record
#                     existing_record_obj.domain_id = domain_obj
#                     existing_record_obj.workspace_id = workspace_obj
#                     existing_record_obj.query = record['keys'][0]
#                     existing_record_obj.page = record['keys'][1]
#                     existing_record_obj.country = record['keys'][2]
#                     existing_record_obj.device = record['keys'][3]
#                     existing_record_obj.date = record['keys'][4]
#                     existing_record_obj.clicks = round(record['clicks'], 2)
#                     existing_record_obj.ctr = round(record['ctr'], 2)
#                     existing_record_obj.impression = round(record['impressions'], 2)
#                     existing_record_obj.position = round(record['position'], 2)
#                     existing_record_obj.save()
#                 else:
#                     # Create new record
#                     console_metrics_obj = console_metrics()
#                     console_metrics_obj.domain_id = domain_obj
#                     console_metrics_obj.workspace_id = workspace_obj
#                     console_metrics_obj.query = record['keys'][0]
#                     console_metrics_obj.page = record['keys'][1]
#                     console_metrics_obj.country = record['keys'][2]
#                     console_metrics_obj.device = record['keys'][3]
#                     console_metrics_obj.date = record['keys'][4]
#                     console_metrics_obj.clicks = round(record['clicks'], 2)
#                     console_metrics_obj.ctr = round(record['ctr'], 2)
#                     console_metrics_obj.impression = round(record['impressions'], 2)
#                     console_metrics_obj.position = round(record['position'], 2)
#                     console_metrics_obj.save()
                
#                 # Add your provided code for logging and progress tracking
#                 install_log_obj = domain_install_log()
#                 install_log_obj.log_type = 'console metrics'
#                 install_log_obj.log_text = f"console metrics: {record['keys'][0]}"
#                 install_log_obj.domain_id = domain_obj
#                 install_log_obj.save()

#                 console_metrics_progress = 30 / total_records

#                 percentage_log_obj = domain_install_log_percentage()
#                 percentage_log_obj.domain_install_log_id = install_log_obj
#                 percentage_log_obj.log_percentage = console_metrics_progress
#                 percentage_log_obj.domain_id = domain_obj
#                 percentage_log_obj.save()

#         # Move to the next day
#         current_date += timedelta(days=1)

#     return 'Console metrics add successfully.'
    
    
    

def process_console_metrics(obj_data):
    domain_obj = obj_data.get("domain_obj")
    workspace_obj = obj_data.get("workspace_obj")
    request_user = obj_data.get("request_user")
    print(f"domain_obj: {domain_obj}")
    print(f"workspace_obj: {workspace_obj}")

    # Domain credentials
    domain_name = 'www.wikilistia.com'
    username = 'Monty Dhanda'
    password = 'Ocxq 6E3x mvJs zDvp UuoD vnnM'


    # # Domain credentials
    # domain_name = domain_obj.name
    # username = domain_obj.wordpress_username
    # password = domain_obj.wordpress_application_password

    api_url = f'https://{domain_name}/wp-json/botxbyte/v1/search-console-data/'

    # Encode credentials
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

    print(f"Fetching data from {start_date} to {end_date}")

    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    # Iterate over the range of dates between start_date and end_date
    for date_obj in (current_date + timedelta(days=x) for x in range((end_date_obj - current_date).days + 1)):
        date_str = date_obj.strftime('%Y-%m-%d')

        params = {
            'startDate': date_str,
            'endDate': date_str,
            'dimensions': 'query, page, country, device, date',
            'limit': 25000,
        }

        response = requests.get(api_url, params=params, headers=headers)
        if response.status_code != 200:
            return "Failed to fetch Console data from API."

        data = response.json()
        total_records = len(data)
        print(f"Processing data for {date_str}, total records: {total_records}")

        if not data:
            continue

        # Process the data in batches
        batch_size = 1000
        for i in range(0, total_records, batch_size):
            batch = data[i:i + batch_size]
            for record in batch:
                date_filter = record['keys'][4]

                existing_record_obj = console_metrics.objects.filter(date=date_filter).first()
                if existing_record_obj:
                    # Update existing record
                    existing_record_obj.domain_id = domain_obj
                    existing_record_obj.workspace_id = workspace_obj
                    existing_record_obj.query = record['keys'][0]
                    existing_record_obj.page = record['keys'][1]
                    existing_record_obj.country = record['keys'][2]
                    existing_record_obj.device = record['keys'][3]
                    existing_record_obj.date = record['keys'][4]
                    existing_record_obj.clicks = round(record['clicks'], 2)
                    existing_record_obj.ctr = round(record['ctr'], 2)
                    existing_record_obj.impression = round(record['impressions'], 2)
                    existing_record_obj.position = round(record['position'], 2)
                    existing_record_obj.save()
                else:
                    # Create new record
                    console_metrics_obj = console_metrics()
                    console_metrics_obj.domain_id = domain_obj
                    console_metrics_obj.workspace_id = workspace_obj
                    console_metrics_obj.query = record['keys'][0]
                    console_metrics_obj.page = record['keys'][1]
                    console_metrics_obj.country = record['keys'][2]
                    console_metrics_obj.device = record['keys'][3]
                    console_metrics_obj.date = record['keys'][4]
                    console_metrics_obj.clicks = round(record['clicks'], 2)
                    console_metrics_obj.ctr = round(record['ctr'], 2)
                    console_metrics_obj.impression = round(record['impressions'], 2)
                    console_metrics_obj.position = round(record['position'], 2)
                    console_metrics_obj.save()

                # Add your provided code for logging and progress tracking
                install_log_obj = domain_install_log()
                install_log_obj.log_type = 'console metrics'
                install_log_obj.log_text = f"console metrics: {record['keys'][0]}"
                install_log_obj.domain_id = domain_obj
                install_log_obj.save()

                console_metrics_progress = 30 / total_records

                percentage_log_obj = domain_install_log_percentage()
                percentage_log_obj.domain_install_log_id = install_log_obj
                percentage_log_obj.log_percentage = console_metrics_progress
                percentage_log_obj.domain_id = domain_obj
                percentage_log_obj.save()

    return 'Console metrics added successfully.'
    
    
    
    
    
    
    
    
    
    
    
    

@api_view(['POST'])
def fetch_console_metrics_data(request):
    try:
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not domain_slug_id:
            return JsonResponse({"error": "Domain slug ID is required."}, status=400)

        if not workspace_slug_id:
            return JsonResponse({"error": "Workspace slug ID is required."}, status=400)

        try:
            domain_obj = domain.objects.get(slug_id=domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "Invalid domain."}, status=404)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Invalid workspace."}, status=404)

        
        obj_data={
            "domain_obj":domain_obj,
            "workspace_obj":workspace_obj,
        }
            
        result = process_console_metrics(obj_data)
        if "Failed" in result:
            return JsonResponse({"error": result}, status=500)
        
        return JsonResponse({'message': result}, status=200)
        
    except Exception as e:
        print("This error is fetch_console_metrics_data --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)
