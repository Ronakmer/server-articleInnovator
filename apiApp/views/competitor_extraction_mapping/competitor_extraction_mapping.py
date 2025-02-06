from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import competitor_extraction_mapping_serializer
from apiApp.models import competitor_extraction_mapping, domain, workspace, competitor, competitor_extraction
from django.db.models import Q


# show competitor_extraction_mapping
@api_view(['GET'])
def list_competitor_extraction_mapping(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        # status = request.GET.get('status', None)
        competitor_slug_id = request.GET.get('competitor_slug_id', None)
        competitor_extraction_slug_id = request.GET.get('competitor_extraction_slug_id', None)
        domain_slug_id = request.GET.get('domain_slug_id', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        selected_article_url = request.GET.get('selected_article_url', None)
        slug_id = request.GET.get('slug_id', None)

        if not (domain_slug_id and  competitor_slug_id and workspace_slug_id and competitor_extraction_slug_id):
            return JsonResponse({
                "error": "domain, competitor, competitor extraction, workspace slug id is required in parameters."
            }, status=400)

        # Initialize filters
        filters = Q()
        if selected_article_url:
            filters &= Q(selected_article_url=selected_article_url)

        if slug_id:
            filters &= Q(slug_id=slug_id)

        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
            competitor_extraction_obj = competitor_extraction.objects.get(slug_id=competitor_extraction_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found."}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found."}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found."}, status=404)
        except competitor_extraction.DoesNotExist:
            return JsonResponse({"error": "competitor extraction not found."}, status=404)

        filters &= Q(domain_id=domain_obj, workspace_id=workspace_obj, competitor_id=competitor_obj, competitor_extraction_id = competitor_extraction_obj)

        try:
            obj = competitor_extraction_mapping.objects.filter(filters).order_by('-created_date')
        except competitor_extraction_mapping.DoesNotExist:
            return JsonResponse({
                "error": "competitor extraction mapping not found.",
            }, status=404)
        
        # Apply pagination
        obj = obj[offset:offset + limit]

        # obj = competitor_extraction_mapping.objects.all()
        serialized_data = competitor_extraction_mapping_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "competitor_extraction_mappings":serialized_data.data,
        }, status=200)

    except Exception as e:
        print("This error is list_competitor_extraction_mapping --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add competitor_extraction_mapping
@api_view(['POST'])
def add_competitor_extraction_mapping(request):
    try:
        
        request_user = request.user
        
        competitor_slug_id = request.data.get('competitor_slug_id')
        competitor_extraction_slug_id = request.data.get('competitor_extraction_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not (domain_slug_id and competitor_slug_id and workspace_slug_id and competitor_extraction_slug_id):
            return JsonResponse({
                "error": "domain, competitor, workspace, competitor extraction slug required fields."
            }, status=400)

        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
            competitor_extraction_obj = competitor_extraction.objects.get(slug_id = competitor_extraction_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found."}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found."}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found."}, status=404)
        except competitor_extraction.DoesNotExist:
            return JsonResponse({"error": "competitor extraction not found."}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  
        data["domain_id"] = domain_obj.id  
        data["workspace_id"] = workspace_obj.id  
        data["competitor_extraction_id"] = competitor_extraction_obj.id  
        data["created_by"] = request_user.id
        
        serialized_data = competitor_extraction_mapping_serializer(data=data)
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "competitor_extraction_mapping": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_competitor_extraction_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
    
# update competitor_extraction_mapping
@api_view(['PUT'])
def update_competitor_extraction_mapping(request, slug_id):
    try:

        try:
            obj = competitor_extraction_mapping.objects.get(slug_id=slug_id)
        except competitor_extraction_mapping.DoesNotExist:
            return JsonResponse({
                "error": "competitor extraction mapping not found.",
            }, status=404)   

 
        competitor_slug_id = request.data.get('competitor_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
        competitor_extraction_slug_id = request.data.get('competitor_extraction_slug_id')

        
        if not (domain_slug_id and  competitor_slug_id and workspace_slug_id and competitor_extraction_slug_id):
            return JsonResponse({
                "error": "domain, competitor, workspace slug required fields."
            }, status=400)
            
        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)
            
        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
            competitor_extraction_obj = competitor_extraction.objects.get(slug_id = competitor_extraction_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found."}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found."}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found."}, status=404)
        except competitor_extraction.DoesNotExist:
            return JsonResponse({"error": "competitor extraction not found."}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  
        data["domain_id"] = domain_obj.id  
        data["workspace_id"] = workspace_obj.id  
        data["competitor_extraction_id"] = competitor_extraction_obj.id  
        data['created_by'] = obj.created_by.id
        # if 'created_by' in data:
        #     del data['created_by']
        
        serialized_data = competitor_extraction_mapping_serializer(instance=obj, data=data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "competitor_extraction_mapping": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_competitor_extraction_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)



# delete competitor_extraction_mapping
@api_view(['DELETE'])
def delete_competitor_extraction_mapping(request, slug_id):
    try:
        try:
            obj = competitor_extraction_mapping.objects.get(slug_id=slug_id)
        except competitor_extraction_mapping.DoesNotExist:
            return JsonResponse({
                "error": "competitor extraction mapping not found.",
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
        print("This error is delete_competitor_extraction_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


