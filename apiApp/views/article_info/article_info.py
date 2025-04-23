from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import article_info_serializer
from apiApp.models import article_info, workspace
from django.db.models import Q
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from apiApp.views.base.process_pagination.process_pagination import process_pagination



# show article_info
@api_view(['GET'])
@workspace_permission_required
def list_article_info(request):
    try:
        request_user = request.user
        
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        api_provider = request.GET.get('api_provider', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')

        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if api_provider:
            filters &= Q(api_provider=api_provider)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(Q(article_id__slug_id=search) )

                
                
        if request_user.is_superuser:       
            obj = article_info.objects.filter(filters).order_by(order_by)
        if request.is_admin:
            obj = article_info.objects.filter(filters).order_by(order_by)
        
        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        print(obj,'obj')

        serialized_data = article_info_serializer(obj, many=True)
        
        return JsonResponse({
            "data":serialized_data.data,
            "success": True,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },
        }, status=200)

    except Exception as e:
        print("This error is list_article_info --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)

