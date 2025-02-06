from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import competitor_sitemap_url_mapping_serializer
from apiApp.models import competitor_sitemap_url_mapping, competitor, competitor_sitemap_url, domain, workspace
from django.db.models import Q


# show competitor sitemap url mapping
@api_view(['GET'])
def list_competitor_sitemap_url_mapping(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        # status = request.GET.get('status', None)
        competitor_slug_id = request.GET.get('competitor_slug_id', None)
        domain_slug_id = request.GET.get('domain_slug_id', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        selected_sitemap_url = request.GET.get('selected_sitemap_url', None)
        competitor_sitemap_url_slug_id = request.GET.get('competitor_sitemap_url_slug_id', None)
        slug_id = request.GET.get('slug_id', None)

        if not (domain_slug_id and  competitor_slug_id and workspace_slug_id and competitor_sitemap_url_slug_id):
            return JsonResponse({
                "error": "domain, competitor, competitor sitemap url, workspace slug id is required in parameters."
            }, status=400)

        # Initialize filters
        filters = Q()
        if selected_sitemap_url:
            filters &= Q(selected_sitemap_url=selected_sitemap_url)
        if slug_id:
            filters &= Q(slug_id=slug_id)

        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
            competitor_sitemap_url_obj = competitor_sitemap_url.objects.get(slug_id = competitor_sitemap_url_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found."}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found."}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found."}, status=404)
        except competitor_sitemap_url.DoesNotExist:
            return JsonResponse({"error": "competitor sitemap url not found."}, status=404)

        filters &= Q(domain_id=domain_obj, workspace_id=workspace_obj, competitor_id=competitor_obj, competitor_sitemap_url_id = competitor_sitemap_url_obj)
       
        try:
            obj = competitor_sitemap_url_mapping.objects.filter(filters).order_by('-created_date')
        except competitor_sitemap_url_mapping.DoesNotExist:
            return JsonResponse({
                "error": "competitor not found.",
            }, status=404)
        
        # Apply pagination
        obj = obj[offset:offset + limit]
        
        # obj = competitor_sitemap_url_mapping.objects.all()
        serialized_data = competitor_sitemap_url_mapping_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "competitor_sitemap_url_mappings":serialized_data.data,
        }, status=200)

    except Exception as e:
        print("This error is list_competitor_sitemap_url_mapping --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add competitor sitemap url mapping
@api_view(['POST'])
def add_competitor_sitemap_url_mapping(request):
    try:
        
        request_user = request.user
        
        competitor_slug_id = request.data.get('competitor_slug_id')
        competitor_sitemap_url_slug_id = request.data.get('competitor_sitemap_url_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        
        if not (domain_slug_id and  competitor_slug_id and workspace_slug_id and competitor_sitemap_url_slug_id):
            return JsonResponse({
                "error": "domain, competitor, competitor sitemap url , workspace slug required fields."
            }, status=400)

            
        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
            competitor_sitemap_url_obj = competitor_sitemap_url.objects.get(slug_id = competitor_sitemap_url_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found."}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found."}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found."}, status=404)
        except competitor_sitemap_url.DoesNotExist:
            return JsonResponse({"error": "competitor sitemap url not found."}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  
        data["domain_id"] = domain_obj.id  
        data["workspace_id"] = workspace_obj.id  
        data["competitor_sitemap_url_id"] = competitor_sitemap_url_obj.id  
        data["created_by"] = request_user.id

        serialized_data = competitor_sitemap_url_mapping_serializer(data=data)
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "competitor_sitemap_url_mapping": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_competitor_sitemap_url_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update competitor sitemap url mapping
@api_view(['PUT'])
def update_competitor_sitemap_url_mapping(request, slug_id):
    try:

        try:
            obj = competitor_sitemap_url_mapping.objects.get(slug_id=slug_id)
        except competitor_sitemap_url_mapping.DoesNotExist:
            return JsonResponse({
                "error": "competitor sitemap url mapping not found.",
            }, status=404)   
            
            
        competitor_slug_id = request.data.get('competitor_slug_id')
        competitor_sitemap_url_slug_id = request.data.get('competitor_sitemap_url_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        
        if not (domain_slug_id and  competitor_slug_id and workspace_slug_id and competitor_sitemap_url_slug_id):
            return JsonResponse({
                "error": "domain, competitor, competitor sitemap url , workspace slug required fields."
            }, status=400)

        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)
       
        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
            competitor_sitemap_url_obj = competitor_sitemap_url.objects.get(slug_id = competitor_sitemap_url_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found."}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found."}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found."}, status=404)
        except competitor_sitemap_url.DoesNotExist:
            return JsonResponse({"error": "competitor sitemap url not found."}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  
        data["domain_id"] = domain_obj.id  
        data["workspace_id"] = workspace_obj.id  
        data["competitor_sitemap_url_id"] = competitor_sitemap_url_obj.id  
        data['created_by'] = obj.created_by.id
        # if 'created_by' in data:
        #     del data['created_by']


        serialized_data = competitor_sitemap_url_mapping_serializer(instance=obj, data=data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "competitor_sitemap_url_mapping": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_competitor_sitemap_url_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)



# delete competitor sitemap url mapping
@api_view(['DELETE'])
def delete_competitor_sitemap_url_mapping(request, slug_id):
    try:
        try:
            obj = competitor_sitemap_url_mapping.objects.get(slug_id=slug_id)
        except competitor_sitemap_url_mapping.DoesNotExist:
            return JsonResponse({
                "error": "competitor sitemap url mapping not found.",
            }, status=404) 

        workspace_slug_id = request.GET.get("workspace_slug_id")  
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace slug id is required."
            }, status=400)
            
        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)             

        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
        }, status=200)

    except Exception as e:
        print("This error is delete_competitor_sitemap_url_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


