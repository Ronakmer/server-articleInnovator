
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import rabbitmq_queue_serializer
from apiApp.models import prompt, workspace, article_type, user_detail, domain, rabbitmq_queue
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from apiApp.views.decorator.domain_decorator import domain_permission_required
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination
import json
import os, requests
RABBITMQ_BASE_URL = os.getenv("RABBITMQ_BASE_URL")  

# show queue
@api_view(['GET'])
# @workspace_permission_required
def list_queues(request):
    try:
        request_user = request.user
        
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        article_type_slug_id = request.GET.get('article_type_slug_id', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            # filters &= Q(name__icontains=search)
            filters &= (
                Q(name__icontains=search) |
                Q(article_type_id__slug_id__icontains=search)
            )
            
        print(search,'searchx')


        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id=workspace_obj)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found.",
                    "success": False,
                }, status=404)  
            
        if article_type_slug_id:
            try:
                article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)
                filters &= Q(article_type_id=article_type_obj)
            except article_type.DoesNotExist:
                return JsonResponse({"error": "Article type not found.","success": False}, status=404)
        
        try:
            obj = rabbitmq_queue.objects.filter(filters).order_by(order_by)
        except rabbitmq_queue.DoesNotExist:
            return JsonResponse({
                "error": "rabbitmq_queue not found.",
                "success": False,
            }, status=404) 
        
        print(obj,'77777777777777777777')
        print(len(obj),'77777777777777777777')
        
        queue_names = [q.name for q in obj]
        queues_obj = get_queues(queue_names) 
        if not queues_obj.get("success"):
            return JsonResponse({"error": queues_obj.get("error", "Unknown error"), "success": False}, status=500)
        queue_results = queues_obj.get("queue_results", [])
        print(queue_results,'88888888888888888888888')

        # limit = 2
        total_count = len(queue_results)  # Count the total number of queue results
        queue_results = queue_results[offset:offset + limit]  # Apply pagination
        print(total_count,'99999999999999999999999999')
        
        page = (offset // limit) + 1 if limit > 0 else 1
        total_pages = (total_count // limit) + (1 if total_count % limit > 0 else 0)

        
        
        return JsonResponse({
            "data":queue_results,
            "success": True,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },            
        }, status=200)

    except Exception as e:
        print("This error is list_queues --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)












import requests

def get_queues(queue_names):
    try:
        print(queue_names, 'queue_namesx')
        queue_results = []

        for queue in queue_names:
            url = f'{RABBITMQ_BASE_URL}/queue/list?queue_names={queue}'
            response = requests.get(url)

            try:
                # response.raise_for_status()
                data = response.json()
                print(response,'responsexxxxxxxxxxxx')
                # If data exists and is valid, add it
                if response.status_code in [200, 201]:
                    queue_results.append({
                        "queue_name": queue,
                        "data": data,
                        "found": True
                    })
                elif response.status_code == 404:
                    print(f'this is not found{queue}')
                    # Queue not found, add default "Not Found" structure
                    queue_results.append({
                        "queue_name": queue,
                        "data": {
                            "arguments": {
                                "x-queue-type": "classic"
                            },
                            "auto_delete": 0,
                            "durable": 0,
                            "exclusive": 0,
                            "idle_since": 0,
                            "memory": 0,
                            "messages": 0,
                            "messages_persistent": 0,
                            "messages_ready": 0,
                            "messages_unacknowledged": 0,
                            "name": queue,
                            "node": "",
                            "reductions": 0,
                            "state": "Not-Found",
                            "type": "",
                            "vhost": "",
                            "worker_count": 0,
                            "worker_pids": [],
                            "workers": []
                        },
                        "found": False
                    })

            except requests.HTTPError as http_err:
                print(f"HTTP error for queue '{queue}': {http_err}")

        print(queue_results, 'queue_resultsx')
        return {"success": True, "queue_results": queue_results}

    except Exception as e:
        print("This error is get_queues --->: ", e)
        return {"error": "Internal Server error.", "success": False}
