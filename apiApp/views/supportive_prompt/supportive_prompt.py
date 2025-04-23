from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import supportive_prompt_serializer
from apiApp.models import supportive_prompt, supportive_prompt_type, workspace
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination



# show supportive_prompt
@api_view(['GET'])
def list_supportive_prompt(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        workspace_slug_id = request.GET.get('workspace_slug_id')


        # Initialize filters
        filters = Q()
        
        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            # filters &= Q(name__icontains=search) 
            filters &= Q(Q(name__icontains=search) | Q(supportive_prompt_type_id__slug_id=search) )
            
        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
                print(workspace_obj,'workspace_obj')
                filters &= Q(workspace_id=workspace_obj)
                
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found ",
                    "success": False,
                }, status=404)


        print(search,'search')

        try:
            obj = supportive_prompt.objects.filter(filters).order_by(order_by)
        except supportive_prompt.DoesNotExist:
            return JsonResponse({
                "error": "wp prompt not found",
                "success": False,
            }, status=404)

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        print(obj,'obk')

        serialized_data = supportive_prompt_serializer(obj, many=True)
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
        print("This error is list_supportive_prompt --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add supportive_prompt
@api_view(['POST'])
def add_supportive_prompt(request):
    try:
        print(request.data,'dataasss')
        supportive_prompt_type_slug_id = request.data.get('supportive_prompt_type_slug_id') 
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not supportive_prompt_type_slug_id:
            return JsonResponse({
                "error": " wp prompt type are required.",
                "success": False,
            }, status=400)
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace are required.",
                "success": False,
            }, status=400)

        try:
            supportive_prompt_type_obj = supportive_prompt_type.objects.get(slug_id=supportive_prompt_type_slug_id)
        except supportive_prompt_type.DoesNotExist:
            return JsonResponse({"error": "wp prompt type not found.","success": False}, status=404)


        # Convert workspace_slug_id to a list if it's a string
        if isinstance(workspace_slug_id, str):
            workspace_slug_id = workspace_slug_id.split(",")


        workspace_objs = workspace.objects.filter(slug_id__in=workspace_slug_id)
        if workspace_objs.count() != len(workspace_slug_id):
            return JsonResponse({
                "error": "One or more workspace(s) not found.",
                "success": False,
            }, status=404)

        created_data = []
        errors = []


        for workspace_obj in workspace_objs:

            data = request.data.copy()
            data['supportive_prompt_type_id'] = supportive_prompt_type_obj.id
            data['workspace_id'] = workspace_obj.id

            serialized_data = supportive_prompt_serializer(data=data)
            
            if serialized_data.is_valid(): 
                serialized_data.save()
                created_data.append(serialized_data.data)
            else:
                errors.append(serialized_data.errors)

         
        if errors:
            return JsonResponse({
                "error": "Some prompts failed to add.",
                "success": False,
                "errors": errors,
                "data": created_data,
            }, status=400)
        
        return JsonResponse({
            "message": "All data added successfully.",
            "success": True,
            "data": created_data,
        }, status=201)
    

    except Exception as e:
        print("This error is add_supportive_prompt --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update wp prompt 
@api_view(['PATCH'])
def update_supportive_prompt(request, slug_id):
    try:
        try:
            obj = supportive_prompt.objects.get(slug_id=slug_id)
        except supportive_prompt.DoesNotExist:
            return JsonResponse({
                "error": "wp prompt not found.",
                "success": False,
            }, status=404)   
            
        supportive_prompt_type_slug_id = request.data.get('supportive_prompt_type_slug_id') 
        workspace_slug_id = request.data.get('workspace_slug_id')

        if not supportive_prompt_type_slug_id:
            return JsonResponse({
                "error": "wp prompt type are required.",
                "success": False,
            }, status=400)
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace are required.",
                "success": False,
            }, status=400)


        try:
            supportive_prompt_type_obj = supportive_prompt_type.objects.get(slug_id=supportive_prompt_type_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
        except supportive_prompt_type.DoesNotExist:
            return JsonResponse({"error": "wp prompt type not found.","success": False}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found.","success": False}, status=404)


        # Include `supportive_prompt_type_id` in the request data for the serializer
        data = request.data.copy()
        data['supportive_prompt_type_id'] = supportive_prompt_type_obj.id
        data['workspace_id'] = workspace_obj.id


        serialized_data = supportive_prompt_serializer(instance=obj, data=data, partial=True)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "success": False,
                "data": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is update_supportive_prompt --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# delete wp prompt
@api_view(['DELETE'])
def delete_supportive_prompt(request, slug_id):
    try:
        try:
            obj = supportive_prompt.objects.get(slug_id=slug_id)
        except supportive_prompt.DoesNotExist:
            return JsonResponse({
                "error": "wp prompt not found.",
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
        print("This error is delete_supportive_prompt --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



