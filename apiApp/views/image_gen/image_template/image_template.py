from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import image_template_serializer
from apiApp.models import image_template, workspace
from django.db.models import Q



# show image template
@api_view(['GET'])
def list_image_template(request):
    try:
        request_user = request.user

        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        

        # Initialize filters
        filters = Q()
       
        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(name__icontains=search) 


        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id=workspace_obj)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found.",
                }, status=404)  
            
        try:
            if request_user.is_superuser:
                obj = image_template.objects.filter(filters).order_by('-created_date')
            else:
                if not workspace_slug_id:
                    return JsonResponse({
                        "error": "workspace not found.",
                    }, status=404)
                    
                obj = image_template.objects.filter(filters).order_by('-created_date')
        except image_template.DoesNotExist:
            return JsonResponse({
                "error": "image template not found.",
            }, status=404)  

        # Apply pagination
        total_count = obj.count()
        obj = obj[offset:offset + limit]

        # obj = image_template.objects.all()
        serialized_data = image_template_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "image_templates":serialized_data.data,
            "total_count": total_count,
            
        }, status=200)

    except Exception as e:
        print("This error is list_image_template --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add image template
@api_view(['POST'])
def add_image_template(request):
    try:
        request_user = request.user
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace is required fields."
            }, status=404)


        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found.",
            }, status=404)  

        # Prepare the data for the serializer, replacing slug with the workspace instance's PK
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id 
        data["created_by"] = request_user.id


        serialized_data = image_template_serializer(data=data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "image_template": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_image_template --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update image template
@api_view(['PUT'])
def update_image_template(request, slug_id):
    try:

        try:
            obj = image_template.objects.get(slug_id=slug_id)
        except image_template.DoesNotExist:
            return JsonResponse({
                "error": "image template not found.",
            }, status=404)  
        
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace is required fields."
            }, status=404)

        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found.",
            }, status=404)  
        

        # Remove 'created_by' from the update request data as it should not be updated
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id 
        data['created_by'] = obj.created_by.id
        # if 'created_by' in data:
        #     del data['created_by']


        serialized_data = image_template_serializer(instance=obj, data=data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "image_template": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_image_template --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)





# delete image template
@api_view(['DELETE'])
def delete_image_template(request, slug_id):
    try:
        try:
            obj = image_template.objects.get(slug_id=slug_id)
        except image_template.DoesNotExist:
            return JsonResponse({
                "error": "image template not found.",
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
        print("This error is delete_image_template --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


