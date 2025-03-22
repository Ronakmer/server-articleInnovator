from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import image_template_serializer
from apiApp.models import image_template, workspace, image_tag, image_template_category
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination
from django.contrib.auth.models import User



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
        order_by = request.GET.get('order_by', '-created_date')
        

        # Initialize filters
        filters = Q()
       
        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= (
                Q(name__icontains=search) |
                Q(image_tag_id__name__icontains=search) |
                Q(image_template_category_id__name__icontains=search)
            )


        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id=workspace_obj)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found.",
                    "success": False,
                }, status=404)  
            
        try:
            if request_user.is_superuser:
                obj = image_template.objects.filter(filters).order_by(order_by)
            if request.is_admin:
                if not workspace_slug_id:
                    return JsonResponse({
                        "error": "workspace not found.",
                        "success": False,
                    }, status=404)
                    
                obj = image_template.objects.filter(filters).order_by(order_by)
        except image_template.DoesNotExist:
            return JsonResponse({
                "error": "image template not found.",
                "success": False,
            }, status=404)  

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        # obj = image_template.objects.all()
        serialized_data = image_template_serializer(obj, many=True)
        
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
        print("This error is list_image_template --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)




@api_view(['GET'])
def get_superadmin_templates(request):
    try:
        request_user = request.user

        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        

        # Initialize filters
        filters = Q()
       
        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(name__icontains=search) 
            
        try:
            super_admin_user = User.objects.filter(is_superuser=True)

            obj = image_template.objects.filter(filters, created_by__in=super_admin_user).order_by(order_by)
                    
        except image_template.DoesNotExist:
            return JsonResponse({
                "error": "image template not found.",
                "success": False,
            }, status=404)  

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        # obj = image_template.objects.all()
        serialized_data = image_template_serializer(obj, many=True)
        
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
        print("This error is get_superadmin_templates --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)






@api_view(['POST'])
def add_image_template(request):
    try:
        request_user = request.user
        template_name = request.data.get('template_name')
        workspace_slug_id = request.data.get('workspace_slug_id')
        image_tag_slug_ids = request.data.get('image_tags', [])
        image_template_category_slug_ids = request.data.get('image_template_category', [])

        if not workspace_slug_id:
            return JsonResponse({"error": "workspace is a required field.","success": False}, status=400)
        if not template_name:
            return JsonResponse({"error": "template name is a required field.","success": False}, status=400)

        # Fetch workspace instance
        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Workspace not found.","success": False}, status=404)

        # Fetch Image Tag Objects
        image_tag_objs = image_tag.objects.filter(slug_id__in=image_tag_slug_ids) if image_tag_slug_ids else []

        # Fetch Image Template Category Objects
        image_template_category_objs = image_template_category.objects.filter(slug_id__in=image_template_category_slug_ids) if image_template_category_slug_ids else []


        # Prepare the data for serialization
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id
        data["created_by"] = request_user.id
        data["name"] = template_name

        # Serialize data
        serialized_data = image_template_serializer(data=data)

        if serialized_data.is_valid():
            image_template_obj = serialized_data.save()
            if image_tag_objs:
                image_template_obj.image_tag_id.set(image_tag_objs)  # Set ManyToManyField
            if image_template_category_objs:
                image_template_obj.image_template_category_id.set(image_template_category_objs)  # Set ManyToManyField
                
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
        print("This error occurred in add_image_template:", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update image template
@api_view(['PATCH'])
def update_image_template(request, slug_id):
    try:

        try:
            obj = image_template.objects.get(slug_id=slug_id)
        except image_template.DoesNotExist:
            return JsonResponse({
                "error": "image template not found.",
                "success": False,
            }, status=404)  
        
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace is required fields.",
                "success": False,
            }, status=400)

        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission.",
                "success": False,
            }, status=403)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({
                "error": "workspace not found.",
                "success": False,
            }, status=404)  
        

        # Remove 'created_by' from the update request data as it should not be updated
        data = request.data.copy()
        data["workspace_id"] = workspace_obj.id 
        data['created_by'] = obj.created_by.id

        serialized_data = image_template_serializer(instance=obj, data=data, partial=True)        
        
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
        print("This error is update_image_template --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)





# delete image template
@api_view(['DELETE'])
def delete_image_template(request, slug_id):
    try:
        try:
            obj = image_template.objects.get(slug_id=slug_id)
        except image_template.DoesNotExist:
            return JsonResponse({
                "error": "image template not found.",
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
            }, status=404)    

        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_image_template --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


