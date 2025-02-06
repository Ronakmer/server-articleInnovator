from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import wp_category_serializer
from apiApp.models import wp_category, domain, workspace
import base64
import requests
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from apiApp.views.decorator.domain_decorator import domain_permission_required
from django.db.models import Q


# show wp category
@api_view(['GET'])
@workspace_permission_required
@domain_permission_required
def list_category(request):
    try:

        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        domain_slug_id = request.GET.get('domain_slug_id')
        workspace_slug_id = request.GET.get('workspace_slug_id')
        slug_id = request.GET.get('slug_id', None)

        
        # Initialize filters
        filters = Q()

        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if slug_id:
            filters &= Q(slug_id=slug_id)
            
        # Check if domain_slug_id is provided
        if not domain_slug_id:
            return JsonResponse({"error": "domain slug id is required in parameters."}, status=400)
        if not workspace_slug_id:
            return JsonResponse({"error": "workspace slug id is required in parameters."}, status=400)


        # Fetch the domain using slug_id
        try:
            domain_obj = domain.objects.get(slug_id=domain_slug_id)
            print(domain_obj,'domain_obj')
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain slug id not found."}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace slug id not found."}, status=404)    

        filters &= Q(domain_id=domain_obj, workspace_id=workspace_obj)


        try:
            obj = wp_category.objects.filter(filters).order_by('-created_date')
        except wp_category.DoesNotExist:
            return JsonResponse({"error": "No categories found for the specified domain."}, status=404)    


        # Apply pagination
        total_count = obj.count()

        obj = obj[offset:offset + limit]

        serialized_data = wp_category_serializer(obj, many=True)
        
        return JsonResponse({
            "categories": serialized_data.data,
            "total_count": total_count,
            
        }, status=200)
    
    except Exception as e:
        print("This error is list_category --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)



# add wp category
@api_view(['POST'])
@workspace_permission_required
@domain_permission_required
def add_category(request):
    try:
        
        name = request.data.get('name')
        slug = request.data.get('slug')
        description = request.data.get('description')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
        
            
        if not (name and slug and description and domain_slug_id and workspace_slug_id):
            return JsonResponse({"error": "name, slug, domain, workspace slug id is required fields."}, status=400)
        
        try:
            domain_id = domain.objects.get(slug_id = domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "Invalid domain ID."}, status=404)

        try:
            workspace_id = workspace.objects.get(slug_id = workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Invalid workspace."}, status=404)

        # Check if the category already exists in the database for this domain
        if wp_category.objects.filter(name=name, domain_id=domain_id).exists():
            return JsonResponse({"error": "Category with this name already exists for the specified domain."}, status=400)

        # Api Call
        url = f'https://{domain_id.name}/wp-json/wp/v2/categories'
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
            print(f"Category API request error: {e}")
            return JsonResponse({"error": "Failed to connect to WordPress API."}, status=500)

        if 'id' in response_data:
            cat_id = response_data['id']
        elif response_data.get('code') == 'term_exists':
            cat_id = response_data['data']['term_id']
        else:
            print(f"Failed to create category: {response_data.get('message', 'Unknown error')}")
            return JsonResponse({
                "error": f"Failed to create category: {response_data.get('message', 'Unknown error')}"
            }, status=400)
            
        if 200 <= response.status_code < 300:

            #  Add in databse
            category_obj = wp_category()
            category_obj.name = name
            category_obj.slug = slug
            category_obj.description = description
            category_obj.domain_id = domain_id
            category_obj.wp_cat_id = cat_id
            category_obj.workspace_id = workspace_id
            category_obj.save()
                
            serialized_category_data = wp_category_serializer(category_obj).data

            return JsonResponse({
                "message": "Data added successfully.",
                "category": serialized_category_data,
                # "name": category_obj.name,
                # "slug": category_obj.slug,
                # "description": category_obj.description,
                # "wp_cat_id": category_obj.wp_cat_id,
                # "slug_id": category_obj.slug_id,
                # "workspace_slug_id": category_obj.workspace_id.slug_id if category_obj.domain_id else None,
                # "domain_id": category_obj.domain_id.name if category_obj.domain_id else None,
                
            }, status=200)
        else:
            return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}"}, status=500)
        
    except Exception as e:
        print("This error is add_category --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)

    
    
# update wp category
@api_view(['PUT'])
@workspace_permission_required
@domain_permission_required
def update_category(request, slug_id):
    try:

        name = request.data.get('name')
        slug = request.data.get('slug')
        description = request.data.get('description')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
            
            
        print(name,'name')
        print(slug,'slug')
        print(description,'description')
        print(domain_slug_id,'domain_slug_id')
        print(workspace_slug_id,'workspace_slug_id')
        
        if not (name and slug and description and domain_slug_id and workspace_slug_id):
            return JsonResponse({"error": "name, slug, domain, workspace slug id is required fields."}, status=400)
        
        try:
            category_obj = wp_category.objects.get(slug_id = slug_id)
        except category_obj.DoesNotExist:
            return JsonResponse({"error": "Invalid category slug ID."}, status=404)

        if (category_obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)

        try:
            workspace_id = workspace.objects.get(slug_id = workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Invalid workspace."}, status=404)

        try:
            domain_id = domain.objects.get(slug_id = domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "Invalid domain ID."}, status=404)

        # Check if another category with the same name exists for this domain
        existing_category = wp_category.objects.filter(name=name, domain_id=domain_id).exclude(id=request.data.get('wp_cat_id')).first()
        if existing_category:
            return JsonResponse({"error": "Category with this name already exists for the specified domain."}, status=400)

        # Api Call
        url = f'https://{domain_id.name}/wp-json/wp/v2/categories/{category_obj.wp_cat_id}'
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
            print(f"Category API request error: {e}")
            return JsonResponse({"error": "Failed to connect to WordPress API."}, status=500)
            
        if 200 <= response.status_code < 300:
            #  update in databse
            category_obj.name = name
            category_obj.slug = slug
            category_obj.description = description
            category_obj.domain_id = domain_id
            category_obj.workspace_id = workspace_id
            category_obj.save()
         
            serialized_category_data = wp_category_serializer(category_obj).data
       
            return JsonResponse({
                "message": "Data updated successfully.",
                "category": serialized_category_data,
                # "name": category_obj.name,
                # "slug": category_obj.slug,
                # "description": category_obj.description,
                # "wp_cat_id": category_obj.wp_cat_id,
                # "slug_id": category_obj.slug_id,
                # "workspace_slug_id": category_obj.workspace_id.slug_id if category_obj.domain_id else None,
                # "domain_id": category_obj.domain_id.name if category_obj.domain_id else None,
                
            }, status=200)
        else:
            return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}"}, status=500)
            
    except Exception as e:
        print("This error is update_category --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


# delete wp category
@api_view(['DELETE'])
@workspace_permission_required
@domain_permission_required
def delete_category(request, slug_id):
    try:
        try:
            category_obj = wp_category.objects.get(slug_id=slug_id)
        except wp_category.DoesNotExist:
            return JsonResponse({
                "error": "category not found.",
            }, status=404) 
                      
        domain_obj = category_obj.domain_id
       
       
        workspace_slug_id = request.GET.get("workspace_slug_id")  
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace slug id is required."
            }, status=400)
    
        if (category_obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)

        #  Delete APi
        url = f'https://{domain_obj.name}/wp-json/wp/v2/categories/{category_obj.wp_cat_id}?force=true'
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
            print(f"Category API request error: {e}")
            return JsonResponse({"error": "Failed to connect to WordPress API."}, status=500)

        if 200 <= response.status_code < 300:
            category_obj.delete()
            
            return JsonResponse({
                "message": "Data Deleted successfully.",
            }, status=200)
        else:
            return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}"}, status=500)

    except Exception as e:
        print("This error is delete_category --->: ", e)
        return JsonResponse({"error": "Internal server error."}, status=500)


