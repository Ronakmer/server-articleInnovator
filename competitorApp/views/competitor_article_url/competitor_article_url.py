from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from competitorApp.serializers import competitor_article_url_serializer
from competitorApp.models import competitor_article_url, competitor_domain_mapping, competitor_selected_url
from django.db.models import Q
from loguru import logger
import json
from competitorApp.views.base.process_pagination.process_pagination import process_pagination


@api_view(['GET'])
def list_competitor_article_url(request):
    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        competitor_id = request.GET.get('competitor_id', None)
        competitor_domain_name = request.GET.get('competitor_domain_name', None)
        search = request.GET.get('search', '')
        competitor_domain_mapping_slug_id = request.GET.get('competitor_domain_mapping_slug_id', None)
        competitor_selected_url_slug_id = request.GET.get('competitor_selected_url_slug_id', None)
        competior_article_url_slug_id = request.GET.get('competitor_article_url_slug_id', None)
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()
        
        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if competitor_id:
            filters &= Q(competitor_id=competitor_id)
        if competitor_domain_name:
            filters &= Q(competitor_domain_name=competitor_domain_name)
        if search:
            filters &= Q(article_url__icontains=search)
        if competitor_domain_mapping_slug_id:
            filters &= Q(competitor_domain_mapping_id__slug_id=competitor_domain_mapping_slug_id)
        if competitor_selected_url_slug_id:
            filters &= Q(competitor_selected_url_id__slug_id=competitor_selected_url_slug_id)
        if competior_article_url_slug_id:
            filters &= Q(slug_id=competior_article_url_slug_id)
        # Get objects with basic filtering
        obj = competitor_article_url.objects.select_related('competitor_selected_url_id', 'competitor_domain_mapping_id').filter(filters).order_by(order_by)

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        serialized_data = competitor_article_url_serializer(obj, many=True)

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
        print("Error in list_competitor_article_url:", e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)
    


@api_view(['POST'])
def add_competitor_article_url(request):
    try:
        data = request.data
        competitor_domain_mapping_slug_id = data.get('competitor_domain_mapping_slug_id')
        
        # Parse the JSON string of selected articles (contains URL and competitor_selected_url_slug_id)
        selected_articles_raw = data.get('selected_articles', [])
        if isinstance(selected_articles_raw, str):
            try:
                selected_articles = json.loads(selected_articles_raw)
            except json.JSONDecodeError:
                return JsonResponse({
                    "error": "Invalid JSON format for selected_articles.",
                    "success": False
                }, status=400)
        else:
            selected_articles = selected_articles_raw
            
        created_by = data.get('created_by')

        print(selected_articles, "selected_articles")
        if not selected_articles:
            return JsonResponse({
                "error": "No articles provided.",
                "success": False
            }, status=400)
        
        # Extract URLs from the article objects for comparison
        article_urls = [article['url'] for article in selected_articles]

        if not created_by:
            return JsonResponse({
                "error": "created_by field is required.",
                "success": False
            }, status=400)

        # Get existing URLs for this competitor and domain mapping
        existing_urls = competitor_article_url.objects.select_related('competitor_selected_url_id', 'competitor_domain_mapping_id').filter(
            competitor_domain_mapping_id__slug_id=competitor_domain_mapping_slug_id,

        ).values_list('article_url', flat=True)

        existing_urls_set = set(existing_urls)
        new_urls_set = set(article_urls)

        # URLs to add (in new set but not in existing set)
        urls_to_add = new_urls_set - existing_urls_set

        # URLs to delete (in existing set but not in new set)
        urls_to_delete = existing_urls_set - new_urls_set

        competitor_domain_mapping_obj = competitor_domain_mapping.objects.select_related('competitor_id').filter(slug_id=competitor_domain_mapping_slug_id).first()
        
        # Add new URLs
        new_urls_data = []
        for url in urls_to_add:
            # Find the corresponding article object with this URL
            article_obj = next((article for article in selected_articles if article['url'] == url), None)
            
            if article_obj:
                # Look up the competitor_selected_url using the slug_id
                competitor_selected_url_obj = None
                if article_obj.get('competitor_selected_url_slug_id'):
                    try:
                        competitor_selected_url_obj = competitor_selected_url.objects.get(
                            slug_id=article_obj['competitor_selected_url_slug_id']
                        )
                    except competitor_selected_url.DoesNotExist:
                        print(f"Warning: competitor_selected_url not found for slug_id: {article_obj['competitor_selected_url_slug_id']}")
                
                url_data = {
                    'competitor_domain_mapping_id': competitor_domain_mapping_obj.pk,
                    'article_url': url,
                    'competitor_selected_url_id': competitor_selected_url_obj.pk if competitor_selected_url_obj else None,
                    'created_by': created_by
                }
                new_urls_data.append(url_data)
        print(new_urls_data, "new_urls_data")
        # Bulk create new URLs
        if new_urls_data:
            serializer = competitor_article_url_serializer(data=new_urls_data, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return JsonResponse({
                    # "error": "Invalid article URL data.",
                    "errors": serializer.errors,
                    "success": False
                }, status=400)

        
        # Delete URLs not in the new list
        if urls_to_delete:
            competitor_article_url.objects.select_related('competitor_selected_url_id', 'competitor_domain_mapping_id').filter(
                competitor_domain_mapping_id=competitor_domain_mapping_obj.pk,
                article_url__in=urls_to_delete
            ).delete()

        return JsonResponse({
            "message": "Article URLs Added successfully.",
            "data": {
                "added_count": len(urls_to_add),
                "deleted_count": len(urls_to_delete),
                "skipped_count": len(existing_urls_set & new_urls_set)
            },
            "success": True
        }, status=200)

    except Exception as e:
        print("Error in add_competitor_article_url:", e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)


@api_view(['DELETE'])
def delete_competitor_article_url(request, competitor_selected_url_slug_id):
    try:
        obj = competitor_article_url.objects.select_related('competitor_selected_url_id', 'competitor_domain_mapping_id').filter(competitor_selected_url_id__slug_id=competitor_selected_url_slug_id)
        if obj.exists():
            obj.delete()
            return JsonResponse({
                "message": "Article URL deleted successfully.",
                "success": True
            }, status=200)
        else:
            return JsonResponse({
                "error": "Competitor article url not found.",
                "success": False
            }, status=404)
    except Exception as e:
        print("Error in delete_competitor_article_url:", e)
        return JsonResponse({"error": "Internal server error.", "success": False}, status=500)
    

