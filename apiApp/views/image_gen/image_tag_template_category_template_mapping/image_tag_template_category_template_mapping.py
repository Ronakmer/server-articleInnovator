from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import image_tag_template_category_template_mapping_serializer
from apiApp.models import image_tag_template_category_template_mapping, workspace, image_tag, image_template_category, image_template



# show image tag template category template mapping
@api_view(['GET'])
def list_image_tag_template_category_template_mapping(request):
    try:
        obj = image_tag_template_category_template_mapping.objects.all()
        serialized_data = image_tag_template_category_template_mapping_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "image_tag_template_category_template_mapping":serialized_data.data,
        }, status=200)

    except Exception as e:
        print("This error is list_image_tag_template_category_template_mapping --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add image tag template category template mapping
@api_view(['POST'])
def add_image_tag_template_category_template_mapping(request):
    try:
        request_user = request.user
        workspace_slug_id = request.data.get('workspace_slug_id')
        image_tag_slug_id = request.data.get('image_tag_slug_id')
        image_template_category_slug_id = request.data.get('image_template_category_slug_id')
        image_template_slug_id = request.data.get('image_template_slug_id')

        if not (workspace_slug_id and image_tag_slug_id and image_template_category_slug_id and image_template_slug_id):
            return JsonResponse({"error": "workspace, image tag, image template category, image template slug id is required fields."}, status=400)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
            image_tag_obj = image_tag.objects.get(slug_id=image_tag_slug_id)
            image_template_category_obj = image_template_category.objects.get(slug_id=image_template_category_slug_id)
            image_template_obj = image_template.objects.get(slug_id=image_template_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found.",}, status=404)  
        except image_tag.DoesNotExist:
            return JsonResponse({"error": "image tag not found.",}, status=404)  
        except image_template_category.DoesNotExist:
            return JsonResponse({"error": "image template category not found.",}, status=404)  
        except image_template.DoesNotExist:
            return JsonResponse({"error": "image template not found.",}, status=404)  

        # Prepare the data for the serializer, replacing slug with the workspace instance's PK
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id 
        data["created_by"] = request_user.id
        data["image_tag_id"] = image_tag_obj.id
        data["image_template_category_id"] = image_template_category_obj.id
        data["image_template_id"] = image_template_obj.id


        serialized_data = image_tag_template_category_template_mapping_serializer(data=data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "image_tag_template_category_template_mapping": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_image_tag_template_category_template_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update image tag template category template mapping
@api_view(['PUT'])
def update_image_tag_template_category_template_mapping(request, slug_id):
    try:

        try:
            obj = image_tag_template_category_template_mapping.objects.get(slug_id=slug_id)
        except image_tag_template_category_template_mapping.DoesNotExist:
            return JsonResponse({
                "error": "image mapping not found.",
            }, status=404)  
        
        workspace_slug_id = request.data.get('workspace_slug_id')
        image_tag_slug_id = request.data.get('image_tag_slug_id')
        image_template_category_slug_id = request.data.get('image_template_category_slug_id')
        image_template_slug_id = request.data.get('image_template_slug_id')

        if not (workspace_slug_id and image_tag_slug_id and image_template_category_slug_id and image_template_slug_id):
            return JsonResponse({"error": "workspace, image tag, image template category, image template slug id is required fields."}, status=400)
        
        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
            image_tag_obj = image_tag.objects.get(slug_id=image_tag_slug_id)
            image_template_category_obj = image_template_category.objects.get(slug_id=image_template_category_slug_id)
            image_template_obj = image_template.objects.get(slug_id=image_template_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found.",}, status=404)  
        except image_tag.DoesNotExist:
            return JsonResponse({"error": "image tag not found.",}, status=404)  
        except image_template_category.DoesNotExist:
            return JsonResponse({"error": "image template category not found.",}, status=404)  
        except image_template.DoesNotExist:
            return JsonResponse({"error": "image template not found.",}, status=404)  


        # Prepare the data for the serializer, replacing slug with the workspace instance's PK
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id 
        data["image_tag_id"] = image_tag_obj.id
        data["image_template_category_id"] = image_template_category_obj.id
        data["image_template_id"] = image_template_obj.id
        data['created_by'] = obj.created_by.id
        # if 'created_by' in data:
        #     del data['created_by']

        serialized_data = image_tag_template_category_template_mapping_serializer(instance=obj, data=data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "image_tag_template_category_template_mapping": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_image_tag_template_category_template_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)





# delete image tag template category template mapping
@api_view(['DELETE'])
def delete_image_tag_template_category_template_mapping(request, slug_id):
    try:
        try:
            obj = image_tag_template_category_template_mapping.objects.get(slug_id=slug_id)
        except image_tag_template_category_template_mapping.DoesNotExist:
            return JsonResponse({
                "error": "image mapping not found.",
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
        print("This error is delete_image_tag_template_category_template_mapping --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


