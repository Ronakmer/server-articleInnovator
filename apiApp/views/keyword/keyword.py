
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import keyword_serializer
from apiApp.models import keyword, prompt, workspace, article_type, country, language
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show keyword
@api_view(['GET'])
def list_keyword(request):
    try:
        request_user = request.user

        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        # status = request.GET.get('status', None)
        prompt_slug_id = request.GET.get('prompt_slug_id', None)
        article_type_slug_id = request.GET.get('article_type_slug_id', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        country_slug_id = request.GET.get('country_slug_id', None)
        language_slug_id = request.GET.get('language_slug_id', None)
        slug_id = request.GET.get('slug_id', None)
        order_by = request.GET.get('order_by', '-created_date')

     
        # Initialize filters
        filters = Q()
        if slug_id:
            filters &= Q(slug_id=slug_id)

        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
                filters &= Q(workspace_id=workspace_obj)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found.",
                    "success": False,
                }, status=404)  

        if prompt_slug_id:
            try:
                prompt_obj = prompt.objects.get(slug_id=prompt_slug_id)
                filters &= Q(prompt_id=prompt_obj)
            except prompt.DoesNotExist:
                return JsonResponse({"error": "Prompt not found.","success": False}, status=404)

        if article_type_slug_id:
            try:
                article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)
                filters &= Q(article_type_id=article_type_obj)
            except article_type.DoesNotExist:
                return JsonResponse({"error": "Article type not found.","success": False}, status=404)
        
        if country_slug_id:
            try:
                country_obj = country.objects.get(slug_id=country_slug_id)
                filters &= Q(country_id=country_obj)
            except country.DoesNotExist:
                return JsonResponse({"error": "Country not found.","success": False}, status=404)

        if language_slug_id:
            try:
                language_obj = language.objects.get(slug_id=language_slug_id)
                filters &= Q(language_id=language_obj)
            except language.DoesNotExist:
                return JsonResponse({"error": "Language not found.","success": False}, status=404)

        try:
            if request_user.is_superuser:
                obj = keyword.objects.filter(filters).order_by(order_by)
            if request.is_admin:
                if not workspace_slug_id:
                    return JsonResponse({
                        "error": "workspace not found.",
                        "success": False,
                    }, status=404)

                obj = keyword.objects.filter(filters).order_by(order_by)
                
        except keyword.DoesNotExist:
            return JsonResponse({
                "error": "keyword not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        serialized_data = keyword_serializer(obj, many=True)
        
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
        print("This error is list_keyword --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add keyword
@api_view(['POST'])
def add_keyword(request):
    try:
        request_user = request.user
        
        prompt_slug_id = request.data.get('prompt_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
        article_type_slug_id = request.data.get('article_type_slug_id')
        country_slug_id = request.data.get('country_slug_id')
        language_slug_id = request.data.get('language_slug_id')

        if not (prompt_slug_id and workspace_slug_id and article_type_slug_id and country_slug_id and language_slug_id):
            return JsonResponse({
                "error": "prompt, workspace, article type, country, language slug required fields.",
                "success": False,
            }, status=400)

        try:
            prompt_obj = prompt.objects.get(slug_id = prompt_slug_id)                
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)                
            article_type_obj = article_type.objects.get(slug_id = article_type_slug_id)                
            country_obj = country.objects.get(slug_id = country_slug_id)                
            language_obj = language.objects.get(slug_id = language_slug_id)                
        except prompt.DoesNotExist:
            return JsonResponse({"error": "user not found.","success": False}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace found.","success": False}, status=404)
        except article_type.DoesNotExist:
            return JsonResponse({"error": "article type found.","success": False}, status=404)
        except country.DoesNotExist:
            return JsonResponse({"error": "country found.","success": False}, status=404)
        except language.DoesNotExist:
            return JsonResponse({"error": "language found.","success": False}, status=404)

        data = request.data.copy()
        data["prompt_id"] = prompt_obj.id  
        data["workspace_id"] = workspace_obj.id  
        data["article_type_id"] = article_type_obj.id  
        data["country_id"] = country_obj.id  
        data["language_id"] = language_obj.id  
        data["created_by"] = request_user.id  

        serialized_data = keyword_serializer(data=data)
        
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
        print("This error is add_keyword --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
    
# update keyword
@api_view(['PATCH'])
def update_keyword(request, slug_id):
    try:

        try:
            obj = keyword.objects.get(slug_id=slug_id)
        except keyword.DoesNotExist:
            return JsonResponse({
                "error": "keyword not found.",
                "success": False,
            }, status=404)   

        prompt_slug_id = request.data.get('prompt_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
        article_type_slug_id = request.data.get('article_type_slug_id')
        country_slug_id = request.data.get('country_slug_id')
        language_slug_id = request.data.get('language_slug_id')

        if not (prompt_slug_id and workspace_slug_id and article_type_slug_id and country_slug_id and language_slug_id):
            return JsonResponse({
                "error": "prompt, workspace, article type, country, language slug required fields.",
                "success": False,
            }, status=400)

        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission.",
                "success": False,
            }, status=403)   
            
        try:
            prompt_obj = prompt.objects.get(slug_id = prompt_slug_id)                
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)                
            article_type_obj = article_type.objects.get(slug_id = article_type_slug_id)                
            country_obj = country.objects.get(slug_id = country_slug_id)                
            language_obj = language.objects.get(slug_id = language_slug_id)                
        except prompt.DoesNotExist:
            return JsonResponse({"error": "user not found.","success": False}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace found.","success": False}, status=404)
        except article_type.DoesNotExist:
            return JsonResponse({"error": "article type found.","success": False}, status=404)
        except country.DoesNotExist:
            return JsonResponse({"error": "country found.","success": False}, status=404)
        except language.DoesNotExist:
            return JsonResponse({"error": "language found.","success": False}, status=404)

        data = request.data.copy()
        data["prompt_id"] = prompt_obj.id  
        data["workspace_id"] = workspace_obj.id  
        data["article_type_id"] = article_type_obj.id  
        data["country_id"] = country_obj.id  
        data["language_id"] = language_obj.id
        data['created_by'] = obj.created_by.id 

        serialized_data = keyword_serializer(instance=obj, data=data, partial=True)        
        
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
        print("This error is update_keyword --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# delete keyword
@api_view(['DELETE'])
def delete_keyword(request, slug_id):
    try:
        try:
            obj = keyword.objects.get(slug_id=slug_id)
        except keyword.DoesNotExist:
            return JsonResponse({
                "error": "keyword not found.",
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
        print("This error is delete_keyword --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


