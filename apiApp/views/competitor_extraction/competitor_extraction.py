from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import competitor_extraction_serializer
from apiApp.models import competitor_extraction, domain, workspace, competitor
from django.db.models import Q


# show competitor extraction
@api_view(['GET'])
def list_competitor_extraction(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        # status = request.GET.get('status', None)
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
            obj = competitor_extraction.objects.filter(filters, competitor_id=competitor_obj).order_by('-created_date')
        except competitor_extraction.DoesNotExist:
            return JsonResponse({
                "error": "competitor domain not found.",
            }, status=404)


        # Apply pagination
        obj = obj[offset:offset + limit]

        
        serialized_data = competitor_extraction_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "competitor_extractions":serialized_data.data,
        }, status=200)

    except Exception as e:
        print("This error is list_competitor_extraction --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add competitor extraction
@api_view(['POST'])
def add_competitor_extraction(request):
    try:
        
        request_user = request.user
        
        competitor_slug_id = request.data.get('competitor_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        
        if not (domain_slug_id and  competitor_slug_id and workspace_slug_id):
            return JsonResponse({
                "error": "domain, competitor, workspace slug required fields."
            }, status=400)

            
        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            competitor_obj = competitor.objects.get(slug_id = competitor_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found."}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found."}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found."}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  
        data["domain_id"] = domain_obj.id  
        data["workspace_id"] = workspace_obj.id  
        data["created_by"] = request_user.id

        
        
        serialized_data = competitor_extraction_serializer(data=data)
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "competitor_extraction": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_competitor_extraction --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
    
# update competitor extraction
@api_view(['PUT'])
def update_competitor_extraction(request, slug_id):
    try:

        try:
            obj = competitor_extraction.objects.get(slug_id=slug_id)
        except competitor_extraction.DoesNotExist:
            return JsonResponse({
                "error": "competitor extraction not found.",
            }, status=404)   

 
        competitor_slug_id = request.data.get('competitor_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        
        if not (domain_slug_id and  competitor_slug_id and workspace_slug_id):
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
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found."}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found."}, status=404)
        except competitor.DoesNotExist:
            return JsonResponse({"error": "competitor not found."}, status=404)

        data = request.data.copy()
        data["competitor_id"] = competitor_obj.id  
        data["domain_id"] = domain_obj.id  
        data["workspace_id"] = workspace_obj.id 
        data['created_by'] = obj.created_by.id 
        # if 'created_by' in data:
        #     del data['created_by']
        
        serialized_data = competitor_extraction_serializer(instance=obj, data=data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "competitor_extraction": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_competitor_extraction --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)



# delete competitor extraction
@api_view(['DELETE'])
def delete_competitor_extraction(request, slug_id):
    try:
        try:
            obj = competitor_extraction.objects.get(slug_id=slug_id)
        except competitor_extraction.DoesNotExist:
            return JsonResponse({
                "error": "competitor extraction not found.",
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
        print("This error is delete_competitor_extraction --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


