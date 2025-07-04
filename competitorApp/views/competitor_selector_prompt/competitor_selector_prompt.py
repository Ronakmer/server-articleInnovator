from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from competitorApp.serializers import competitor_serializer, competitor_domain_mapping_serializer, competitor_selector_prompt_serializer
from competitorApp.models import competitor, competitor_domain_mapping, competitor_selector_prompt
from django.db.models import Q
from loguru import logger
import json
from competitorApp.views.base.process_pagination.process_pagination import process_pagination


@api_view(['GET'])
def list_competitor_selector_prompt(request):
    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        search = request.GET.get('search', '')
        competitor_domain_mapping_slug_id = request.GET.get('competitor_domain_mapping_slug_id', None)
        competitor_selector_prompt_slug_id = request.GET.get('competitor_selector_prompt_slug_id', None)
        is_active = request.GET.get('is_active', None)
        order_by = request.GET.get('order_by', '-created_date')
        
        # Initialize filters
        filters = Q()
        
        # Apply filters based on provided parameters
        if search:
            filters &= Q(prompt__icontains=search)
        if competitor_domain_mapping_slug_id:
            filters &= Q(competitor_domain_mapping_id__slug_id=competitor_domain_mapping_slug_id)
        if competitor_selector_prompt_slug_id:
            filters &= Q(slug_id=competitor_selector_prompt_slug_id)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            filters &= Q(is_active=is_active)

        # Get objects with basic filtering
        obj = competitor_selector_prompt.objects.select_related('competitor_domain_mapping_id').filter(filters).order_by(order_by)

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        serialized_data = competitor_selector_prompt_serializer(obj, many=True)

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
        logger.error(f"Error in list_competitor_selector_prompt: {str(e)}")
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)


@api_view(['POST'])
def add_competitor_selector_prompt(request):
    try:
        data = json.loads(request.body)
        competitor_domain_mapping_slug_id = data.get('competitor_domain_mapping_slug_id')
        prompt = data.get('prompt', {})
        is_active = data.get('is_active', True)

        # Validate required fields
        if not competitor_domain_mapping_slug_id:
            return JsonResponse({
                "error": "competitor_domain_mapping_slug_id is required.",
                "success": False
            }, status=400)

        # Check if competitor_domain_mapping exists
        competitor_domain_mapping_obj = competitor_domain_mapping.objects.select_related('competitor_id').filter(
            slug_id=competitor_domain_mapping_slug_id
        ).first()

        if not competitor_domain_mapping_obj:
            return JsonResponse({
                "error": "Domain mapping not found.",
                "success": False
            }, status=404)

        # Create prompt data
        prompt_data = {
            'competitor_domain_mapping_id': competitor_domain_mapping_obj.id,
            'prompt': prompt,
            'is_active': is_active
        }

        # Create new prompt
        serializer = competitor_selector_prompt_serializer(data=prompt_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "message": "Competitor selector prompt added successfully.",
                "data": serializer.data,
                "success": True
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid prompt data.",
                "errors": serializer.errors,
                "success": False
            }, status=400)

    except Exception as e:
        logger.error(f"Error in add_competitor_selector_prompt: {str(e)}")
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)


@api_view(['PATCH'])
def update_competitor_selector_prompt(request, competitor_selector_prompt_slug_id):
    try:
        data = json.loads(request.body)

        # Check if prompt exists
        prompt_obj = competitor_selector_prompt.objects.select_related('competitor_domain_mapping_id').filter(
            slug_id=competitor_selector_prompt_slug_id
        ).first()

        if not prompt_obj:
            return JsonResponse({
                "error": "Competitor selector prompt not found.",
                "success": False
            }, status=404)

        # Update prompt
        serializer = competitor_selector_prompt_serializer(prompt_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "message": "Competitor selector prompt updated successfully.",
                "data": serializer.data,
                "success": True
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid prompt data.",
                "errors": serializer.errors,
                "success": False
            }, status=400)

    except Exception as e:
        logger.error(f"Error in update_competitor_selector_prompt: {str(e)}")
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)


@api_view(['DELETE'])
def delete_competitor_selector_prompt(request, competitor_selector_prompt_slug_id):
    try:
        prompt_obj = competitor_selector_prompt.objects.select_related('competitor_domain_mapping_id').filter(
            slug_id=competitor_selector_prompt_slug_id
        ).first()

        if prompt_obj:
            prompt_obj.delete()
            return JsonResponse({
                "message": "Competitor selector prompt deleted successfully.",
                "success": True
            }, status=200)
        else:
            return JsonResponse({
                "error": "Competitor selector prompt not found.",
                "success": False
            }, status=404)

    except Exception as e:
        logger.error(f"Error in delete_competitor_selector_prompt: {str(e)}")
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)
    

