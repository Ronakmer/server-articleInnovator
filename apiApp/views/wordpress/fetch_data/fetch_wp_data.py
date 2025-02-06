import threading
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from apiApp.views.wordpress.fetch_data.fetch_tag_data import fetch_tag_data, process_tags
from apiApp.views.wordpress.fetch_data.fetch_category_data import fetch_category_data, process_category
from apiApp.views.wordpress.fetch_data.fetch_author_data import fetch_author_data, process_author
from apiApp.views.wordpress.fetch_data.fetch_analytics_metrics_data import fetch_analytics_metrics_data, process_analytics_metrics
from apiApp.views.wordpress.fetch_data.fetch_console_metrics_data import fetch_console_metrics_data, process_console_metrics
from apiApp.views.wordpress.fetch_data.fetch_article_data import fetch_article_data, process_article
import time
from apiApp.models import domain, wp_tag, workspace


@api_view(['GET'])
def fetch_wp_data(request):
    try:
        
        # time.sleep(30)
        
        # Retrieve domain_id from GET request parameters
        domain_slug_id = request.GET.get('domain_slug_id')
        workspace_slug_id = request.GET.get('workspace_slug_id')

        print(domain_slug_id,'b0b')

        if not domain_slug_id:
            return JsonResponse({"error": "Domain ID is required."}, status=400)
        
        if not workspace_slug_id:
            return JsonResponse({"error": "workspace ID is required."}, status=400)


        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({
                "error": "Invalid domain.",
            }, status=404) 

        try:
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "Invalid workspace.",
            }, status=404)  


        print(domain_slug_id,workspace_slug_id)
        
        obj_data={
            "domain_obj":domain_obj,
            "workspace_obj":workspace_obj,
            "request_user":request.user,
        }
        
        #  background tag process
        background_tag_process = threading.Thread(target=process_tags, args=(obj_data,))
        background_tag_process.start()

        #  background category process
        background_category_process = threading.Thread(target=process_category, args=(obj_data,))
        background_category_process.start()
        
        #  background author process
        background_author_process = threading.Thread(target=process_author, args=(obj_data,))
        background_author_process.start()
        
        #  background article process
        background_article_process = threading.Thread(target=process_article, args=(obj_data,))
        background_article_process.start()
        
        #  background analytics metrics process
        background_analytics_metrics_process = threading.Thread(target=process_analytics_metrics, args=(obj_data,))
        background_analytics_metrics_process.start()
        
        #  background console metrics process
        background_console_metrics_process = threading.Thread(target=process_console_metrics, args=(obj_data,))
        background_console_metrics_process.start()


        # Return a response indicating the task has started
        return JsonResponse({"message": "Data fetching has started."}, status=200)

    except Exception as e:
        print("This error is fetch_wp_data --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)




