

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import prompt_serializer
from apiApp.models import prompt, workspace, article_type, user_detail, domain
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from apiApp.views.decorator.domain_decorator import domain_permission_required
from django.db.models import Q



# show prompt
@api_view(['GET'])
@workspace_permission_required
@domain_permission_required
def list_prompt(request):
    try:
        request_user = request.user
        
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        article_type_slug_id = request.GET.get('article_type_slug_id', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        article_category = request.GET.get('article_category', None)
        category = request.GET.get('category', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        

        # Initialize filters
        filters = Q()
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
            
        if article_category:
            try:
                article_category = article_type.objects.get(article_category=article_category)
                filters &= Q(article_category=article_category)
            except article_type.DoesNotExist:
                return JsonResponse({"error": "article category not found."}, status=404)
        if category:
            try:
                category = article_type.objects.get(category=category)
                filters &= Q(category=category)
            except article_type.DoesNotExist:
                return JsonResponse({"error": "category not found."}, status=404)

        if article_type_slug_id:
            try:
                article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)
                filters &= Q(article_type_id=article_type_obj)
            except article_type.DoesNotExist:
                return JsonResponse({"error": "Article type not found."}, status=404)
        
        if request_user.is_superuser:
            try:
                obj = prompt.objects.filter(filters).order_by('-created_date')
            except prompt.DoesNotExist:
                return JsonResponse({
                    "error": "prompt not found.",
                }, status=404) 
        else:
            try:
                user_obj = user_detail.objects.get(user_id=request_user.id) 
            except user_detail.DoesNotExist:
                return JsonResponse({
                    "error": "user not found."
                }, status=404)

            if user_obj.role_id.name == 'admin':
                try:
                    obj = prompt.objects.filter(filters, created_by=request_user).distinct().order_by('-created_date')
                except prompt.DoesNotExist:
                    return JsonResponse({
                        "error": "prompt not found.",
                    }, status=404)   
            

        # Apply pagination
        total_count = obj.count()
        obj = obj[offset:offset + limit]

        
        serialized_data = prompt_serializer(obj, many=True)
        
        return JsonResponse({
            "redirect": "",
            "prompts":serialized_data.data,
            "total_count":total_count,
            
        }, status=200)

    except Exception as e:
        print("This error is list_prompt --->: ",e)
        return JsonResponse({"error": "Internal Server error."}, status=500)



# add prompt
@api_view(['POST'])
@workspace_permission_required
@domain_permission_required
def add_prompt(request):
    try:
        request_user = request.user
        
        workspace_slug_id = request.data.get('workspace_slug_id')
        article_type_slug_id = request.data.get('article_type_slug_id')
        
        if not workspace_slug_id:
            return JsonResponse({
                "error": "Workspace slug id are required ."
            }, status=404)
            
        if not article_type_slug_id:
            return JsonResponse({
                "error": "Article Type slug id are required."
            }, status=404)

        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
            article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Workspace not found."}, status=404)
        except article_type.DoesNotExist:
            return JsonResponse({"error": "Article Type not found."}, status=404)

        
        print(workspace_obj.id, article_type_obj.id)
        # Include data in the request data for the serializer
        data = request.data.copy()
        data['workspace_id'] = workspace_obj.id
        data['article_type_id'] = article_type_obj.id
        data['created_by'] = request_user.id
        
        print(data)
        serialized_data = prompt_serializer(data=data)

        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data added successfully.",
                "prompt": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is add_prompt --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update prompt
@api_view(['PUT'])
@workspace_permission_required
@domain_permission_required
def update_prompt(request, slug_id):
    try:

        try:
            obj = prompt.objects.get(slug_id=slug_id)
        except prompt.DoesNotExist:
            return JsonResponse({
                "error": "prompt not found.",
            }, status=404)   
        
        workspace_slug_id = request.data.get('workspace_slug_id')
        article_type_slug_id = request.data.get('article_type_slug_id')
        
        if not workspace_slug_id:
            return JsonResponse({
                "error": "Workspace slug id are required ."
            }, status=404)
            
        if not article_type_slug_id:
            return JsonResponse({
                "error": "Article Type slug id are required."
            }, status=404)

        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)
            
        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
            article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Workspace not found."}, status=404)
        except article_type.DoesNotExist:
            return JsonResponse({"error": "Article Type not found."}, status=404)


        # Include data in the request data for the serializer
        data = request.data.copy()
        data['workspace_id'] = workspace_obj.id
        data['article_type_id'] = article_type_obj.id
        data['created_by'] = obj.created_by.id
        # if 'created_by' in data:
        #     del data['created_by']

        serialized_data = prompt_serializer(instance=obj, data=data)        
        
        if serialized_data.is_valid():
            serialized_data.save()
            
            return JsonResponse({
                "message": "Data updated successfully.",
                "prompt": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
            }, status=400)

    except Exception as e:
        print("This error is update_prompt --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)



# delete prompt
@api_view(['DELETE'])
@workspace_permission_required
@domain_permission_required
def delete_prompt(request, slug_id):
    try:
        request_user = request.user
        try:
            obj = prompt.objects.get(slug_id=slug_id)
        except prompt.DoesNotExist:
            return JsonResponse({
                "error": "prompt not found.",
            }, status=404) 
   
        workspace_slug_id = request.GET.get("workspace_slug_id")
          
        if not request_user.is_superuser:
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
        print("This error is delete_prompt --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)




