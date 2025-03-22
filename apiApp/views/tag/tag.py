from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import wp_tag_serializer
from apiApp.models import wp_tag, domain, workspace
import base64
import requests
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from apiApp.views.decorator.domain_decorator import domain_permission_required
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show wp tag
@api_view(['GET'])
# @workspace_permission_required
@domain_permission_required
def list_tag(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        domain_slug_id = request.GET.get('domain_slug_id')
        workspace_slug_id = request.GET.get('workspace_slug_id')
        slug_id = request.GET.get('slug_id', None)
        order_by = request.GET.get('order_by', '-created_date')
        

        # Initialize filters
        filters = Q()
        if slug_id:
            filters &= Q(slug_id=slug_id)

        # Apply filters based on provided parameters

        # Check if domain_slug_id is provided
        if not domain_slug_id:
            return JsonResponse({"error": "domain slug id is required in parameters.","success": False}, status=400)
        if not workspace_slug_id:
            return JsonResponse({"error": "workspace slug id is required in parameters.","success": False}, status=400)

        # Fetch the domain using slug_id
        try:
            domain_obj = domain.objects.get(slug_id=domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain slug id not found.","success": False}, status=404)    
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace slug id not found.","success": False}, status=404)    
        
        filters &= Q(domain_id=domain_obj, workspace_id=workspace_obj)

        try:
            obj = wp_tag.objects.filter(filters).order_by(order_by)           
        except wp_tag.DoesNotExist:
            return JsonResponse({"error": "No tag found for the specified domain.","success": False}, status=404)    
    
        # Apply pagination
        # obj = obj[offset:offset + limit]
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        
        try:
            serialized_data = wp_tag_serializer(obj, many=True)
            return JsonResponse({
                "data": serialized_data.data,
                "success": True,
                "pagination": {
                    "total_count": total_count,
                    "page": page,
                    "page_size": limit,
                    "total_pages": total_pages
                },
            }, status=200)
        except Exception as e:
            print("Serialization error:", e)
            return JsonResponse({"error": "Error serializing data.","success": False}, status=500)
        

    except Exception as e:
        print("This error is list_tag --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# add wp tag
@api_view(['POST'])
# @workspace_permission_required
@domain_permission_required
def add_tag(request):
    try:
        
        name = request.data.get('name')
        slug = request.data.get('slug')
        description = request.data.get('description')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
            
        if not (name and slug and description and domain_slug_id):
            return JsonResponse({"error": "name, slug, domain, workspace slug id is required fields.","success": False}, status=400)
        
        try:
            domain_id = domain.objects.get(slug_id = domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "Invalid domain."}, status=404)
 
        try:
            workspace_id = workspace.objects.get(slug_id = workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Invalid workspace."}, status=404)

        # Check if the tag already exists in the database for this domain
        if wp_tag.objects.filter(name=name, domain_id=domain_id).exists():
            return JsonResponse({"error": "Tag with this name already exists for the specified domain.","success": False}, status=409)

        # Api Call
        url = f'https://{domain_id.name}/wp-json/wp/v2/tags'
        username = domain_id.wordpress_username
        password = domain_id.wordpress_application_password
        credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}',
        }
        data = {
            'name': name,
            'slug': slug,
            'description': description,
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Tag API request error: {e}")
            return JsonResponse({"error": "Failed to connect to WordPress API.","success": False}, status=500)

        if 'id' in response_data:
            tag_id = response_data['id']
        elif response_data.get('code') == 'term_exists':
            tag_id = response_data['data']['term_id']
        else:
            print(f"Failed to create tag: {response_data.get('message', 'Unknown error')}")
            return JsonResponse({
                "error": f"Failed to create tag: {response_data.get('message', 'Unknown error')}",
                "success": False,
            }, status=400)
            
        if response.status_code in (200, 201):

            #  Add in databse
            tag_obj = wp_tag()
            tag_obj.name = name
            tag_obj.slug = slug
            tag_obj.description = description
            tag_obj.domain_id = domain_id
            tag_obj.wp_tag_id = tag_id
            tag_obj.workspace_id = workspace_id
            tag_obj.save()
                
            serialized_tag_data = wp_tag_serializer(tag_obj).data

            return JsonResponse({
                "message": "Data added successfully.",
                "data":serialized_tag_data,            
                "success": True,    
            }, status=200)
        else:
            return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}","success": False}, status=500)
        
    except Exception as e:
        print("This error is add_tag --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update wp tag
@api_view(['PATCH'])
# @workspace_permission_required
@domain_permission_required
def update_tag(request, slug_id):
    try:

        name = request.data.get('name')
        slug = request.data.get('slug')
        description = request.data.get('description')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
            
        if not (name and slug and description and domain_slug_id):
            return JsonResponse({"error": "name, slug, domain, workspace slug id is required fields.","success": False}, status=400)
        
        try:
            tag_obj = wp_tag.objects.get(slug_id = slug_id)
        except tag_obj.DoesNotExist:
            return JsonResponse({"error": "Invalid tag slug ID.","success": False}, status=404)

        try:
            domain_id = domain.objects.get(slug_id = domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "Invalid domain ID.","success": False}, status=404)

        if (tag_obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission.",
                "success": False,
            }, status=403)
            
        try:
            workspace_id = workspace.objects.get(slug_id = workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Invalid workspace.","success": False}, status=404)


        # Check if another tag with the same name exists for this domain
        existing_tag = wp_tag.objects.filter(name=name, domain_id=domain_id).exclude(id=request.data.get('tag_id')).first()
        if existing_tag:
            return JsonResponse({"error": "Tag with this name already exists for the specified domain.","success": False}, status=400)

        # Api Call
        url = f'https://{domain_id.name}/wp-json/wp/v2/tags/{tag_obj.wp_tag_id}'
        username = domain_id.wordpress_username
        password = domain_id.wordpress_application_password
        credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}',
        }
        data = {
            'name': name,
            'slug': slug,
            'description': description,
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Tag API request error: {e}")
            return JsonResponse({"error": "Failed to connect to WordPress API.","success": False}, status=500)
            
        if response.status_code in (200, 201):

            #  update in databse
            tag_obj.name = name
            tag_obj.slug = slug
            tag_obj.description = description
            tag_obj.domain_id = domain_id
            tag_obj.workspace_id = workspace_id
            tag_obj.save()
                
            serialized_tag_data = wp_tag_serializer(tag_obj).data

            return JsonResponse({
                "message": "Data updated successfully.",
                "data":serialized_tag_data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}","success": False}, status=500)
            
    except Exception as e:
        print("This error is update_tag --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


# delete wp tag
@api_view(['DELETE'])
# @workspace_permission_required
@domain_permission_required
def delete_tag(request, slug_id):
    try:
        try:
            tag_obj = wp_tag.objects.get(slug_id=slug_id)
        except wp_tag.DoesNotExist:
            return JsonResponse({
                "error": "tag not found.",
                "success": False,
            }, status=404) 
                      
        domain_obj = tag_obj.domain_id
       
        workspace_slug_id = request.GET.get("workspace_slug_id")  
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace slug id is required.",
                "success": False,
            }, status=400)
            
        if (tag_obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission.",
                "success": False,
            }, status=403)

    
        #  Delete APi
        url = f'https://{domain_obj.name}/wp-json/wp/v2/tags/{tag_obj.wp_tag_id}?force=true'
        username = domain_obj.wordpress_username
        password = domain_obj.wordpress_application_password
        credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

        headers = {
            'Authorization': f'Basic {credentials}',
        }

        # Make the DELETE request
        try:
            response = requests.delete(url, headers=headers)
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Tag API request error: {e}")
            return JsonResponse({"error": "Failed to connect to WordPress API.","success": False}, status=500)
        if response.status_code in (200, 201):
            tag_obj.delete()
            
            return JsonResponse({
                "message": "Data Deleted successfully.",
                "success": True,
            }, status=200)
        else:
            return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}","success": False}, status=500)

    except Exception as e:
        print("This error is delete_tag --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


