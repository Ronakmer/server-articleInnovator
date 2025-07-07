from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from competitorApp.serializers import competitor_serializer, competitor_domain_mapping_serializer, competitor_selected_url_serializer, category_url_selector_serializer
from competitorApp.models import competitor, competitor_domain_mapping, competitor_selected_url, category_url_selector
from django.db.models import Q
from loguru import logger
import json
from competitorApp.views.base.process_pagination.process_pagination import process_pagination


@api_view(['GET'])
def list_category_url_selector(request):
    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        search = request.GET.get('search', '')
        competitor_selected_url_slug_id = request.GET.get('competitor_selected_url_slug_id', None)
        category_url_selector_slug_id = request.GET.get('category_url_selector_slug_id', None)
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()
        
        # Apply filters based on provided parameters
        if search:
            filters &= (
                Q(selector_name__icontains=search) |
                Q(selector__icontains=search)
            )
        if competitor_selected_url_slug_id:
            filters &= Q(competitor_selected_url_id__slug_id=competitor_selected_url_slug_id)
        if category_url_selector_slug_id:
            filters &= Q(slug_id=category_url_selector_slug_id)

        # Get objects with basic filtering
        obj = category_url_selector.objects.select_related(
            'competitor_selected_url_id'
        ).filter(filters).order_by(order_by)

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        serialized_data = category_url_selector_serializer(obj, many=True)

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
        print("Error in list_category_url_selector:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)


@api_view(['POST'])
def add_category_url_selector(request):
    try:
        data = request.data
        competitor_selected_url_slug_id = data.get('competitor_selected_url_slug_id')
        selector_name = data.get('selector_name')
        selector = data.get('selector')

        # Validate required fields
        if not all([competitor_selected_url_slug_id, selector_name, selector]):
            return JsonResponse({
                "error": "Missing required fields: competitor_selected_url_slug_id, selector_name, and selector are required.",
                "success": False
            }, status=400)

        # Check if competitor_selected_url exists
        competitor_selected_url_obj = competitor_selected_url.objects.select_related(
            'competitor_domain_mapping_id'
        ).filter(
            slug_id=competitor_selected_url_slug_id
        ).first()

        if not competitor_selected_url_obj:
            return JsonResponse({
                "error": "Selected URL not found.",
                "success": False
            }, status=400)  # Don't return 404, just fail cleanly

        # Check if selector already exists
        existing_selector = category_url_selector.objects.select_related(
            'competitor_selected_url_id'
        ).filter(
            competitor_selected_url_id=competitor_selected_url_obj,
            selector_name=selector_name
        ).first()

        selector_data = {
            'competitor_selected_url_id': competitor_selected_url_obj.id,
            'selector_name': selector_name,
            'selector': selector
        }

        if existing_selector:
            # Update existing selector
            serializer = category_url_selector_serializer(existing_selector, data=selector_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    "message": "Selector updated successfully.",
                    "data": serializer.data,
                    "success": True
                }, status=200)
            else:
                return JsonResponse({
                    "error": "Invalid data while updating.",
                    "errors": serializer.errors,
                    "success": False
                }, status=400)

        # Create new selector
        serializer = category_url_selector_serializer(data=selector_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "message": "Selector created successfully.",
                "data": serializer.data,
                "success": True
            }, status=201)
        else:
            return JsonResponse({
                "error": "Invalid data provided.",
                "errors": serializer.errors,
                "success": False
            }, status=400)

    except Exception as e:
        print("Error in add_category_url_selector:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)


@api_view(['PATCH'])
def update_category_url_selector(request, category_url_selector_slug_id):
    try:
        data = json.loads(request.body)
        selector_name = data.get('selector_name')
        
        # Get existing selector
        selector = category_url_selector.objects.select_related(
            'competitor_selected_url_id'
        ).filter(
            slug_id=category_url_selector_slug_id
        ).first()
        
        if not selector:
            return JsonResponse({
                "error": "Category URL selector not found.",
                "success": False
            }, status=404)

        # If selector_name is being updated, check for duplicates
        if selector_name and selector_name != selector.selector_name:
            existing_selector = category_url_selector.objects.select_related(
                'competitor_selected_url_id'
            ).filter(
                competitor_selected_url_id=selector.competitor_selected_url_id,
                selector_name=selector_name
            ).exclude(slug_id=category_url_selector_slug_id).first()

            if existing_selector:
                return JsonResponse({
                    "error": f"Selector name '{selector_name}' already exists for this URL.",
                    "success": False
                }, status=400)

        # Update selector
        serializer = category_url_selector_serializer(selector, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "message": "Category URL selector updated successfully.",
                "data": serializer.data,
                "success": True
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data provided.",
                "errors": serializer.errors,
                "success": False
            }, status=400)

    except Exception as e:
        print("Error in update_category_url_selector:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)


@api_view(['DELETE'])
def delete_category_url_selector(request, category_url_selector_slug_id):
    try:
        selector = category_url_selector.objects.select_related(
            'competitor_selected_url_id'
        ).filter(
            slug_id=category_url_selector_slug_id
        )
        
        if selector.exists():
            selector.delete()
            return JsonResponse({
                "message": "Category URL selector deleted successfully.",
                "success": True
            }, status=200)
        else:
            return JsonResponse({
                "error": "Category URL selector not found.",
                "success": False
            }, status=404)
            
    except Exception as e:
        print("Error in delete_category_url_selector:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)




