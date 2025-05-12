from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import wp_author_serializer
from apiApp.models import wp_author, domain, workspace
import base64
import requests
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from apiApp.views.decorator.domain_decorator import domain_permission_required
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show wp author
@api_view(['GET'])
# @workspace_permission_required
@domain_permission_required
def list_author(request):
    try:
        request_user = request.user
        
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

        # Apply filters based on provided parameters
        if slug_id:
            filters &= Q(slug_id=slug_id)
        # Check if domain_slug_id is provided
        if not domain_slug_id:
            return JsonResponse({"error": "domain slug id is required in parameters.","success": False}, status=400)
        if not workspace_slug_id:
            return JsonResponse({"error": "workspace slug id is required in parameters.","success": False}, status=400)
        
        try:
            domain_obj = domain.objects.get(slug_id=domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain slug id not found.","success": False}, status=404)    
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace slug id not found.","success": False}, status=404)    

        filters &= Q(domain_id=domain_obj, workspace_id=workspace_obj)

        try:
            obj = wp_author.objects.filter(filters).order_by(order_by)
        except wp_author.DoesNotExist:
            return JsonResponse({"error": "No author found for the specified domain.","success": False}, status=404)    

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)


        try:
            serialized_data = wp_author_serializer(obj, many=True)
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
        print("This error is list_author --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# add wp author
@api_view(['POST'])
# @workspace_permission_required
@domain_permission_required
def add_author(request):
    try:   
        author_username = request.data.get('username')
        bio = request.data.get('bio')
        author_password = request.data.get('password')
        author_first_name = request.data.get('first_name')
        author_last_name = request.data.get('last_name')
        author_email = request.data.get('email')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
        request_user = request.user
            
        if not (author_username and author_password and author_email and domain_slug_id and workspace_slug_id):
            return JsonResponse({"error": "author username, password, email, domain and  workspce slug id is required fields.","success": False}, status=400)
        
        try:
            domain_id = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "Invalid domain ID.","success": False}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Invalid workspace.","success": False}, status=404)

        #  create cutsom mail
        author_email = author_email + '@' +domain_id.name

        # Check if the author already exists in the database for this domain
        if wp_author.objects.filter(username=author_username, domain_id=domain_id).exists():
            return JsonResponse({"error": "Author with this name already exists for the specified domain.","success": False}, status=409)

        # Api Call
        url = f'https://{domain_id.name}/wp-json/wp/v2/users'
        username = domain_id.wordpress_username
        password = domain_id.wordpress_application_password
        credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}',
        }
        data = {
            'username': author_username,
            'email': author_email,
            'password': author_password,
            'roles': ['author'] ,
            'first_name': author_first_name,
            'last_name': author_last_name,
            'description': bio
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            print(response_data,'response_data')
        except requests.exceptions.RequestException as e:
            print(f"Author API request error: {e}")
            return JsonResponse({"error": "Failed to connect to WordPress API.","success": False}, status=500)

        if 'id' in response_data:
            author_id = response_data['id']
        elif response_data.get('code') == 'term_exists':
            author_id = response_data['data']['term_id']
        else:
            print(f"Failed to create author: {response_data.get('message', 'Unknown error')}")
            return JsonResponse({
                "error": f"Failed to create author: {response_data.get('message', 'Unknown error')}"
            }, status=400)
            
        if response.status_code in (200, 201):

            #  Add in databse
            author_obj = wp_author()
            author_obj.username = author_username
            author_obj.author_password = author_password
            author_obj.first_name = author_first_name
            author_obj.last_name = author_last_name
            author_obj.email = author_email
            author_obj.domain_id = domain_id
            author_obj.wp_author_id = author_id
            author_obj.workspace_id = workspace_obj
            author_obj.bio = bio
            author_obj.created_by = request_user.id 
            author_obj.save()
                
            serialized_author_data = wp_author_serializer(author_obj).data

            return JsonResponse({
                "message": "Data added successfully.",
                "data":serialized_author_data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}","success": False}, status=500)
        
    except Exception as e:
        print("This error is add_author --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    

# update wp author
@api_view(['PATCH'])
# @workspace_permission_required
@domain_permission_required
def update_author(request, slug_id):
    try:
        author_username = request.data.get('username')
        bio = request.data.get('bio')
        author_password = request.data.get('password')
        author_first_name = request.data.get('first_name')
        author_last_name = request.data.get('last_name')
        author_email = request.data.get('email')
        domain_slug_id = request.data.get('domain_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')
            
        if not (author_username and author_password and author_email and domain_slug_id and workspace_slug_id):
            return JsonResponse({"error": "author username, password, email, domain and  workspce slug id is required fields.","success": False}, status=400)

        try:
            author_obj = wp_author.objects.get(slug_id = slug_id)
        except author_obj.DoesNotExist:
            return JsonResponse({"error": "Invalid author slug ID.","success": False}, status=404)

        if (author_obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)
            
        try:
            workspace_id = workspace.objects.get(slug_id = workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "Invalid workspace.","success": False}, status=404)

        try:
            domain_id = domain.objects.get(slug_id = domain_slug_id)
        except domain.DoesNotExist:
            return JsonResponse({"error": "Invalid domain ID.","success": False}, status=404)
        
        # Api Call
        url = f'https://{domain_id.name}/wp-json/wp/v2/users/{author_obj.wp_author_id}'
        username = domain_id.wordpress_username
        password = domain_id.wordpress_application_password
        credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}',
        }
        data = {
            'username': author_username,
            'email': author_email,
            'password': author_password,
            'roles': ['author'] ,
            'first_name': author_first_name,
            'last_name': author_last_name,
            'description': bio
        }

        try:
            response = requests.put(url, headers=headers, json=data)
            response_data = response.json()
            print(response_data,'response_data4')
        except requests.exceptions.RequestException as e:
            print(f"Author API request error: {e}")
            return JsonResponse({"error": "Failed to connect to WordPress API.","success": False}, status=500)
            
        if response.status_code in (200, 201):

            #  update in databse
            author_obj.username = author_username
            author_obj.author_password = author_password
            author_obj.first_name = author_first_name
            author_obj.last_name = author_last_name
            author_obj.email = author_email
            author_obj.domain_id = domain_id
            author_obj.workspace_id = workspace_id
            author_obj.bio = bio
            author_obj.save()
                
            serialized_author_data = wp_author_serializer(author_obj).data

            return JsonResponse({
                "message": "Data added successfully.",
                "data":serialized_author_data,
                "success": True,
            }, status=200)
        else:
            return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}","success": False}, status=500)


            
    except Exception as e:
        print("This error is update_author --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)    


# delete wp author
@api_view(['DELETE'])
# @workspace_permission_required
@domain_permission_required
def delete_author(request, slug_id):
    try:
        try:
            author_obj = wp_author.objects.get(slug_id=slug_id)
        except wp_author.DoesNotExist:
            return JsonResponse({
                "error": "author not found.",
            }, status=404) 
           
        workspace_slug_id = request.GET.get("workspace_slug_id")  
        if not workspace_slug_id:
            return JsonResponse({
                "error": "workspace slug id is required.",
                "success": False,
            }, status=400)
   
        if (author_obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission.",
                "success": False,
            }, status=404)
                      
        domain_obj = author_obj.domain_id
        new_author = request.GET.get('new_author')
        
        try:
            new_author_obj = wp_author.objects.get(username=new_author)
        except wp_author.DoesNotExist:
            return JsonResponse({"error": "new author not found.","success": False}, status=404)

        #  Delete APi
        url = f'https://{domain_obj.name}/wp-json/wp/v2/users/{author_obj.wp_author_id}?force=true&reassign={new_author_obj.wp_author_id}'
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
            print(f"Author API request error: {e}")
            return JsonResponse({"error": "Failed to connect to WordPress API.","success": False}, status=500)
        
                    
        if response.status_code in (200, 201):

            author_obj.delete()
            
            return JsonResponse({
                "message": "Data Deleted successfully.",
                "success": True,
            }, status=200)
        else:
            return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}","success": False}, status=500)

    except Exception as e:
        print("This error is delete_author --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


