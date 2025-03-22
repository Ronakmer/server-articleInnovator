from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import competitor_article_url_mapping_serializer
from apiApp.models import competitor_article_url_mapping, competitor, competitor_article_url, domain, workspace
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show competitor article url mapping
@api_view(['GET'])
def list_competitor_article_url_mapping(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        # status = request.GET.get('status', None)
        competitor_slug_id = request.GET.get('competitor_slug_id', None)
        competitor_article_url_slug_id = request.GET.get('competitor_article_url_slug_id', None)
        domain_slug_id = request.GET.get('domain_slug_id', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        selected_article_url = request.GET.get('selected_article_url', None)
        slug_id = request.GET.get('slug_id', None)
        order_by = request.GET.get('order_by', '-created_date')

        if not (domain_slug_id and  competitor_slug_id and workspace_slug_id and competitor_article_url_slug_id):
            return JsonResponse({
                "error": "domain, competitor, competitor article url, workspace slug id is required in parameters.",
                "success": False,
            }, status=400)

       
        # Initialize filters
        filters = Q()
        if selected_article_url:
            filters |= Q(selected_article_url=selected_article_url)

        if slug_id:
            filters &= Q(slug_id=slug_id)

        try:
            domain_slug_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_slug_obj = workspace.objects.get(slug_id = workspace_slug_id)
            competitor_slug_obj = competitor.objects.get(slug_id = competitor_slug_id)
            competitor_article_url_slug_obj = competitor_article_url.objects.get(slug_id = competitor_article_url_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found.","success": False}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found.","success": False}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found.","success": False}, status=404)
        except competitor_article_url.DoesNotExist:
            return JsonResponse({"error": "competitor article url not found.","success": False}, status=404)

        filters &= Q(domain_id=domain_slug_obj, workspace_id=workspace_slug_obj, competitor_id=competitor_slug_obj, competitor_article_url_id = competitor_article_url_slug_obj)

        try:
            obj = competitor_article_url_mapping.objects.filter(filters).order_by(order_by)
        except competitor_article_url.DoesNotExist:
            return JsonResponse({
                "error": "competitor not found.",
                "success": False,
            }, status=404)
        
        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        
        serialized_data = competitor_article_url_mapping_serializer(obj, many=True)
        
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
        print("This error is list_competitor_article_url_mapping --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add competitor article url mapping
@api_view(['POST'])
def add_competitor_article_url_mapping(request):
    try:
        
        request_user = request.user
        
        competitor_slug_id = request.data.get('competitor_slug_id')
        competitor_article_url_slug_id = request.data.get('competitor_article_url_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        
        if not (domain_slug_id and  competitor_slug_id and workspace_slug_id and competitor_article_url_slug_id):
            return JsonResponse({
                "error": "domain, competitor, competitor sitemap url , workspace slug required fields.",
                "success": False,
            }, status=400)

            
        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
            competitor_article_url_obj = competitor_article_url.objects.get(slug_id = competitor_article_url_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found.","success": False}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found.","success": False}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found.","success": False}, status=404)
        except competitor_article_url.DoesNotExist:
            return JsonResponse({"error": "competitor article url not found.","success": False}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  
        data["domain_id"] = domain_obj.id  
        data["workspace_id"] = workspace_obj.id  
        data["competitor_article_url_id"] = competitor_article_url_obj.id  
        data["created_by"] = request_user.id
            
            
        serialized_data = competitor_article_url_mapping_serializer(data=data)
        
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
        print("This error is add_competitor_article_url_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update competitor article url mapping
@api_view(['PATCH'])
def update_competitor_article_url_mapping(request, slug_id):
    try:

        try:
            obj = competitor_article_url_mapping.objects.get(slug_id=slug_id)
        except competitor_article_url_mapping.DoesNotExist:
            return JsonResponse({
                "error": "competitor article url mapping not found.",
                "success": False,
            }, status=404)   
            
            
        competitor_slug_id = request.data.get('competitor_slug_id')
        competitor_article_url_slug_id = request.data.get('competitor_article_url_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        
        if not (domain_slug_id and  competitor_slug_id and workspace_slug_id and competitor_article_url_slug_id):
            return JsonResponse({
                "error": "domain, competitor, competitor sitemap url , workspace slug required fields.",
                "success": False,
            }, status=400)
            
        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission.",
                "success": False,
            }, status=403)
            
        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
            competitor_article_url_obj = competitor_article_url.objects.get(slug_id = competitor_article_url_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found.","success": False}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found.","success": False}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found.","success": False}, status=404)
        except competitor_article_url.DoesNotExist:
            return JsonResponse({"error": "competitor article url not found.","success": False}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  
        data["domain_id"] = domain_obj.id  
        data["workspace_id"] = workspace_obj.id  
        data["competitor_article_url_id"] = competitor_article_url_obj.id  
        data['created_by'] = obj.created_by.id


        serialized_data = competitor_article_url_mapping_serializer(instance=obj, data=data, partial=True)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "data": serialized_data.data,
                "success": False,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is update_competitor_article_url_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# delete competitor article url mapping
@api_view(['DELETE'])
def delete_competitor_article_url_mapping(request, slug_id):
    try:
        try:
            obj = competitor_article_url_mapping.objects.get(slug_id=slug_id)
        except competitor_article_url_mapping.DoesNotExist:
            return JsonResponse({
                "error": "competitor article url mapping not found.",
                "success": False,
            }, status=404) 
        workspace_slug_id = request.GET.get("workspace_slug_id")  
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace slug id is required.",
                "success": False,
            }, status=400)
            
        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission.",
                "success": False,
            }, status=403)
    
       
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_competitor_article_url_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


