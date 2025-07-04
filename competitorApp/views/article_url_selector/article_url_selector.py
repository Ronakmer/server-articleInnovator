from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from competitorApp.serializers import competitor_serializer, competitor_domain_mapping_serializer
from competitorApp.models import competitor, competitor_article_url, competitor_domain_mapping, competitor_selected_url
from django.db.models import Q
import json
from competitorApp.views.base.process_pagination.process_pagination import process_pagination
from competitorApp.serializers import article_url_selector_serializer
from competitorApp.models import article_url_selector


@api_view(['GET'])
def list_article_url_selector(request):
    try:
        # Get pagination parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        
        # Get filter parameters
        search = request.GET.get('search', '')
        is_verified = request.GET.get('is_verified', None)
        competitor_selected_url_slug_id = request.GET.get('competitor_selected_url_slug_id', None)
        competitor_article_url_slug_id = request.GET.get('competitor_article_url_slug_id', None)
        order_by = request.GET.get('order_by', '-created_date')

        # Initialize filters
        filters = Q()
        
        # Apply filters based on provided parameters
        if search:
            filters &= (
                Q(title__icontains=search) |
                Q(slug_id__icontains=search)
            )
            
        if is_verified is not None:
            is_verified = is_verified.lower() == 'true'
            filters &= Q(is_verified=is_verified)
            
        if competitor_selected_url_slug_id:
            filters &= Q(competitor_selected_url_id__slug_id=competitor_selected_url_slug_id)
            
        if competitor_article_url_slug_id:
            filters &= Q(competitor_article_url_id__slug_id=competitor_article_url_slug_id)

        try:
            # Get queryset with filters, ordering and select_related for foreign keys
            obj = article_url_selector.objects.select_related(
                'competitor_article_url_id',
                'competitor_selected_url_id'
            ).filter(filters).order_by(order_by)
            
        except article_url_selector.DoesNotExist:
            return JsonResponse({
                "error": "Article URL selector not found.",
                "success": False,
            }, status=404)

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        # Serialize the data
        serialized_data = article_url_selector_serializer(obj, many=True)

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
        print(f"Error in list_article_url_selector: {str(e)}")
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)


@api_view(['POST'])
def add_article_url_selector(request):
    try:
        data = request.data
        print("Data:", data)
        # Required fields
        competitor_article_url_slug_id = data.get('competitor_article_url_slug_id')
        competitor_selected_url_slug_id = data.get('competitor_selected_url_slug_id')
        print("Competitor Article URL Slug ID:", competitor_article_url_slug_id)
        
        if not competitor_article_url_slug_id or not competitor_selected_url_slug_id:
            return JsonResponse({
                "error": "competitor_article_url_slug_id and competitor_selected_url_slug_id are required.",
                "success": False
            }, status=400)

        competitor_article_url_obj = competitor_article_url.objects.get(slug_id=competitor_article_url_slug_id)
        competitor_selected_url_obj = competitor_selected_url.objects.get(slug_id=competitor_selected_url_slug_id)
        
        # Try to get existing selector first
        try:
            selector_obj = article_url_selector.objects.get(
                competitor_article_url_id=competitor_article_url_obj,
                competitor_selected_url_id=competitor_selected_url_obj
            )
            created = False
            print(f"Found existing selector record - will update it")
        except article_url_selector.DoesNotExist:
            # Create new selector if it doesn't exist
            selector_obj = article_url_selector.objects.create(
                competitor_article_url_id=competitor_article_url_obj,
                competitor_selected_url_id=competitor_selected_url_obj,
                source_title={},
                source_content={},
                source_featured_image={},
                source_author={},
                source_published_date={},
                source_categories={},
                source_tags={},
                source_meta_title={},
                source_meta_description={},
                source_meta_keywords={},
                source_outline=[],
                source_internal_links=[],
                source_external_links=[],
                source_faqs=[],
                is_verified=False,
                verified_by=''
            )
            created = True
            print(f"Created new selector record")

        # Update fields if they exist in the request
        fields_to_update = {
            'source_title': data.get('source_title'),
            'source_content': data.get('source_content'),
            'source_featured_image': data.get('source_featured_image'),
            'source_author': data.get('source_author'),
            'source_published_date': data.get('source_published_date'),
            'source_categories': data.get('source_categories'),
            'source_tags': data.get('source_tags'),
            'source_meta_title': data.get('source_meta_title'),
            'source_meta_description': data.get('source_meta_description'),
            'source_meta_keywords': data.get('source_meta_keywords'),
            'source_outline': data.get('source_outline'),
            'source_internal_links': data.get('source_internal_links'),
            'source_external_links': data.get('source_external_links'),
            'source_faqs': data.get('source_faqs'),
            'is_verified': data.get('is_verified'),
            'verified_by': data.get('verified_by')
        }

        # Only update fields that are present in the request
        update_fields = []
        for field, value in fields_to_update.items():
            if value is not None:
                # Handle JSON string data for selector fields
                if field.startswith('source_') and isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        pass  # Keep as string if not valid JSON
                
                # Handle boolean string conversion for Django BooleanField
                elif field in ['is_verified'] and isinstance(value, str):
                    value = value.lower() in ['true']
                
                setattr(selector_obj, field, value)
                update_fields.append(field)

        if update_fields:
            selector_obj.save(update_fields=update_fields)

        serialized_data = article_url_selector_serializer(selector_obj)
        
        # Dynamic message based on whether it was created or updated
        message = "Article URL selector created successfully." if created else "Article URL selector updated successfully."
        
        return JsonResponse({
            "message": message,
            "data": serialized_data.data,
            "success": True,
            "created": created
        }, status=201 if created else 200)

    except Exception as e:
        print(f"Error in add_article_url_selector: {str(e)}")
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)
    
# def update_article_url_selector(request, article_url_selector_slug_id):
#     try:
#         pass
#     except Exception as e:
#         print("Error in update_article_url_selector:", e)
#         return JsonResponse({"error": str(e), "success": False}, status=500)
    
@api_view(['DELETE'])
def delete_article_url_selector(request, article_url_selector_slug_id):
    try:
        article_url_selector_obj = article_url_selector.objects.get(slug_id=article_url_selector_slug_id)
        article_url_selector_obj.delete()
        return JsonResponse({"message": "Article URL selector deleted successfully.", "success": True}, status=200)
    except Exception as e:
        print(f"Error in delete_article_url_selector: {str(e)}")
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)



