from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from competitorApp.serializers import competitor_serializer, competitor_domain_mapping_serializer
from competitorApp.models import competitor, competitor_article_url, competitor_domain_mapping
from django.db.models import Q
from loguru import logger
import json
from competitorApp.views.base.process_pagination.process_pagination import process_pagination
from competitorApp.serializers import competitor_selected_url_serializer
from competitorApp.models import competitor_selected_url


@api_view(['GET'])
def list_competitor_selected_url(request):
    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        competitor_slug_id = request.GET.get('competitor_slug_id', None)
        competitor_domain_name = request.GET.get('competitor_domain_name', None)
        search = request.GET.get('search', '')
        competitor_domain_mapping_slug_id = request.GET.get('competitor_domain_mapping_slug_id', None)
        competitor_selected_url_slug_id = request.GET.get('competitor_selected_url_slug_id', None)
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()
        
        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if competitor_slug_id:
            filters &= Q(competitor_id__slug_id=competitor_slug_id)
        if competitor_domain_name:
            filters &= Q(competitor_domain_name=competitor_domain_name)
        if search:
            filters &= (
                Q(competitor_domain_name__icontains=search) |
                Q(competitor_id__competitor_domain_name__icontains=search)
            )
        if competitor_domain_mapping_slug_id:
            filters &= Q(competitor_domain_mapping_id__slug_id=competitor_domain_mapping_slug_id)
        if competitor_selected_url_slug_id:
            filters &= Q(slug_id=competitor_selected_url_slug_id)

        
        # Use select_related or prefetch_related for related fields
        obj = competitor_selected_url.objects.select_related('competitor_id', 'competitor_domain_mapping_id').filter(filters).prefetch_related('competitor_domain_mapping_set').order_by(order_by)
            
        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        serialized_data = competitor_selected_url_serializer(obj, many=True)

        return JsonResponse({
            "data": serialized_data.data,
            "success": True,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": limit,
                "total_pages": total_pages
            },
        }, status=200)

    except Exception as e:
        print("Error in list_competitor_selected_url:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)
    


@api_view(['POST'])
def add_competitor_selected_url(request):
    try:
        data = request.data
        competitor_slug_id = data.get('competitor_slug_id')
        competitor_domain_mapping_slug_id = data.get('competitor_domain_mapping_slug_id')
        
        # Handle URLs - parse JSON string if needed
        urls_data = data.get('selected_urls', '[]')
        if isinstance(urls_data, str):
            try:
                urls = json.loads(urls_data)
            except json.JSONDecodeError:
                urls = []
        else:
            urls = urls_data if isinstance(urls_data, list) else []
            
        created_by = data.get('created_by')

        if not urls:
            return JsonResponse({
                "error": "No URLs provided.",
                "success": False
            }, status=400)

        if not created_by:
            return JsonResponse({
                "error": "created_by field is required.",
                "success": False
            }, status=400)

        # Get existing URLs for this competitor and domain mapping
        existing_urls = competitor_selected_url.objects.select_related('competitor_id', 'competitor_domain_mapping_id').filter(
            competitor_id__slug_id=competitor_slug_id,
            competitor_domain_mapping_id__slug_id=competitor_domain_mapping_slug_id
        ).values_list('selected_url', flat=True)

        competitor_domain_mapping_obj = competitor_domain_mapping.objects.select_related('competitor_id').filter(slug_id=competitor_domain_mapping_slug_id).first()
        if not competitor_slug_id:
            competitor_slug_id = competitor_domain_mapping_obj.competitor_id.slug_id

        competitor_obj = competitor.objects.filter(slug_id=competitor_slug_id).first()

        if not competitor_obj or not competitor_domain_mapping_obj:
            return JsonResponse({
                "error": "Competitor or domain mapping not found.",
                "success": False
            }, status=404)

        existing_urls_set = set(existing_urls)
        new_urls_set = set(urls)

        # URLs to add (in new set but not in existing set)
        urls_to_add = new_urls_set - existing_urls_set

        # URLs to delete (in existing set but not in new set)
        urls_to_delete = existing_urls_set - new_urls_set

        # Add new URLs
        new_urls_data = []
        for url in urls_to_add:
            url_data = {
                'competitor_id': competitor_obj.pk,  # Use PK instead of object
                'competitor_domain_mapping_id': competitor_domain_mapping_obj.pk,  # Use PK instead of object
                'selected_url': url,
                'created_by': created_by
            }
            new_urls_data.append(url_data)

        # Bulk create new URLs
        if new_urls_data:
            serializer = competitor_selected_url_serializer(data=new_urls_data, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return JsonResponse({
                    "error": "Invalid URL data.",
                    "errors": serializer.errors,
                    "success": False
                }, status=400)

        # Delete URLs not in the new list
        if urls_to_delete:
            competitor_selected_url.objects.select_related('competitor_id', 'competitor_domain_mapping_id').filter(
                competitor_id__slug_id=competitor_slug_id,
                competitor_domain_mapping_id__slug_id=competitor_domain_mapping_slug_id,
                selected_url__in=urls_to_delete
            ).delete()

        return JsonResponse({
            "message": "URLs processed successfully.",
            "data": {
                "added_count": len(urls_to_add),
                "deleted_count": len(urls_to_delete),
                "skipped_count": len(existing_urls_set & new_urls_set)
            },
            "success": True
        }, status=200)

    except Exception as e:
        print("Error in add_competitor_selected_url:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)


@api_view(['DELETE'])
def delete_competitor_selected_url(request, competitor_domain_mapping_slug_id):
    try:
        selected_urls = competitor_selected_url.objects.select_related('competitor_id', 'competitor_domain_mapping_id').filter(
            competitor_domain_mapping_id__slug_id=competitor_domain_mapping_slug_id
        )

        if selected_urls.exists():
            competitor_article_url.objects.select_related('competitor_selected_url_id', 'competitor_domain_mapping_id').filter(
                competitor_selected_url_id__in=selected_urls
            ).delete()
            selected_urls.delete()
            return JsonResponse({
                "message": "URL deleted successfully.",
                "success": True
            }, status=200)
        else:
            return JsonResponse({
                "error": "Competitor selected url not found.",
                "success": False
            }, status=404)
    except Exception as e:
        print("Error in delete_competitor_selected_url:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)
    