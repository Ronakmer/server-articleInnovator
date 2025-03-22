from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import competitor_article_url_serializer
from apiApp.models import competitor_article_url, competitor
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination



# show competitor article url
@api_view(['GET'])
def list_competitor_article_url(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        # status = request.GET.get('status', None)
        competitor_slug_id = request.GET.get('competitor_slug_id', None)
        slug_id = request.GET.get('slug_id', None)
        order_by = request.GET.get('order_by', '-created_date')

        # Initialize filters
        filters = Q()

        # # Apply filters based on provided parameters
        if slug_id:
            filters &= Q(slug_id=slug_id)
        try:
            competitor_obj = competitor.objects.get(slug_id=competitor_slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({
                "error": "competitor slug id is required in parameters.",
                "success": False,
            }, status=400)         
            
        try:
            obj = competitor_article_url.objects.filter(competitor_id=competitor_obj).order_by(order_by)
        except competitor_article_url.DoesNotExist:
            return JsonResponse({
                "error": "competitor sitemap url not found.",
                "success": False,
            }, status=404)
            

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        
        serialized_data = competitor_article_url_serializer(obj, many=True)
        
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
        print("This error is list_competitor_article_url --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add competitor article url
@api_view(['POST'])
def add_competitor_article_url(request):
    try:
        
        competitor_slug_id = request.data.get('competitor_slug_id')
        
        if not competitor_slug_id:
            return JsonResponse({
                "error": "competitor slug required fields.",
                "success": False,
            }, status=400)

            
        try:
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found.","success": False}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  

        serialized_data = competitor_article_url_serializer(data=data)
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "data": serialized_data.data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is add_competitor_article_url --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update competitor article url
@api_view(['PATCH'])
def update_competitor_article_url(request, slug_id):
    try:

        try:
            obj = competitor_article_url.objects.get(slug_id=slug_id)
        except competitor_article_url.DoesNotExist:
            return JsonResponse({
                "error": "competitor sitemap url not found.",
                "success": False,
            }, status=404)   
            
        competitor_slug_id = request.data.get('competitor_slug_id')
        
        if not competitor_slug_id:
            return JsonResponse({
                "error": "competitor slug required fields.",
                "success": False,
            }, status=400)
            
        try:
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found.","success": False}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  
        

        serialized_data = competitor_article_url_serializer(instance=obj, data=data, partial=True)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "data": serialized_data.data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is update_competitor_article_url --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


# delete competitor article url
@api_view(['DELETE'])
def delete_competitor_article_url(request, slug_id):
    try:
        try:
            obj = competitor_article_url.objects.get(slug_id=slug_id)
        except competitor_article_url.DoesNotExist:
            return JsonResponse({
                "error": "competitor sitemap url not found.",
                "success": False,
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_competitor_article_url --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


