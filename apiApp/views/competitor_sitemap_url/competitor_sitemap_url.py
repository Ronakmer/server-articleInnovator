from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import competitor_sitemap_url_serializer
from apiApp.models import competitor_sitemap_url, competitor
from django.db.models import Q


# show competitor_sitemap_url
@api_view(['GET'])
def list_competitor_sitemap_url(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        competitor_slug_id = request.GET.get('competitor_slug_id', None)
        slug_id = request.GET.get('slug_id', None)

        # Initialize filters
        filters = Q()

        if slug_id:
            filters &= Q(slug_id=slug_id)


        try:
            competitor_obj = competitor.objects.get(slug_id=competitor_slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({
                "error": "competitor not found.",
            }, status=404)         
            
        try:
            obj = competitor_sitemap_url.objects.filter(filters, competitor_id=competitor_obj).order_by('-created_date')
        except competitor_sitemap_url.DoesNotExist:
            return JsonResponse({
                "error": "competitor sitemap url not found.",
            }, status=404)
            
        # Apply pagination
        obj = obj[offset:offset + limit]
        
        # obj = competitor_sitemap_url.objects.all()
        serialized_data = competitor_sitemap_url_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "competitor_sitemap_urls":serialized_data.data,
        }, status=200)

    except Exception as e:
        print("This error is list_competitor_sitemap_url --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add competitor_sitemap_url
@api_view(['POST'])
def add_competitor_sitemap_url(request):
    try:
        
        competitor_slug_id = request.data.get('competitor_slug_id')
        
        if not competitor_slug_id:
            return JsonResponse({
                "error": "competitor slug required fields."
            }, status=400)

            
        try:
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found."}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  


        serialized_data = competitor_sitemap_url_serializer(data=data)
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "competitor_sitemap_url": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_competitor_sitemap_url --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update competitor_sitemap_url
@api_view(['PUT'])
def update_competitor_sitemap_url(request, slug_id):
    try:

        try:
            obj = competitor_sitemap_url.objects.get(slug_id=slug_id)
        except competitor_sitemap_url.DoesNotExist:
            return JsonResponse({
                "error": "competitor sitemap url not found.",
            }, status=404)   
            
        competitor_slug_id = request.data.get('competitor_slug_id')
        
        if not competitor_slug_id:
            return JsonResponse({
                "error": "competitor slug required fields."
            }, status=400)

            
        try:
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found."}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  
        

        serialized_data = competitor_sitemap_url_serializer(instance=obj, data=data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "competitor_sitemap_url": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_competitor_sitemap_url --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


# delete competitor_sitemap_url
@api_view(['DELETE'])
def delete_competitor_sitemap_url(request, slug_id):
    try:
        try:
            obj = competitor_sitemap_url.objects.get(slug_id=slug_id)
        except competitor_sitemap_url.DoesNotExist:
            return JsonResponse({
                "error": "competitor sitemap url not found.",
            }, status=404) 
                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_competitor_sitemap_url --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


