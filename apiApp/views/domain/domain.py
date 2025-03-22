from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import domain_serializer
from apiApp.models import domain, user_detail, workspace
from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from django.db.models import Q
from apiApp.views.wordpress.perma_links.perma_links import get_perma_links, update_perma_links
from apiApp.views.base.process_pagination.process_pagination import process_pagination


# show domain
@api_view(['GET'])
@workspace_permission_required
def list_domain(request):
    try:
        request_user = request.user

        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        workspace_slug_id = request.GET.get('workspace_slug_id', None)
        manager = request.GET.get('manager', None)
        writer = request.GET.get('writer', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')


        # Initialize filters
        filters = Q()
        
        # Apply filters based on provided parameters

        if manager:
            filters &= Q(manager_id=manager)
        if writer:
            filters &= Q(writer_id=writer)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(name__icontains=search)

        if workspace_slug_id:
            try:
                workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
            except workspace.DoesNotExist:
                return JsonResponse({
                    "error": "workspace not found ",
                    "success": False,
                }, status=404)


        if request_user.is_superuser:
            try:
                obj = domain.objects.filter(filters, workspace_id=workspace_obj).order_by(order_by) 
 
            except domain.DoesNotExist:
                return JsonResponse({
                    "error": "domain not found.",
                    "success": False,
                }, status=404)  

        if not request_user.is_superuser:
        
            if request.is_admin:
                try:
                    obj = domain.objects.filter(filters, workspace_id=workspace_obj).distinct().order_by(order_by)
                except domain.DoesNotExist:
                    return JsonResponse({
                        "error": "domain not found.",
                        "success": False,
                    }, status=404)   
            else:
                try:
                    obj = domain.objects.filter(Q(manager_id__user_id=request_user) | Q(writer_id__user_id=request_user),workspace_id=workspace_obj).distinct().order_by(order_by)
                except domain.DoesNotExist:
                    return JsonResponse({
                        "error": "domain not found.",
                        "success": False,
                    }, status=404)   

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)


        serialized_data = domain_serializer(obj, many=True)
        
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
        print("This error is list_domain --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add domain
@api_view(['POST'])
@workspace_permission_required
def add_domain(request):
    try:
        request_user = request.user
        if not request_user.is_superuser:   
            try:
                user_obj = user_detail.objects.get(user_id=request_user.id)

                domain_count_obj = domain.objects.filter(manager_id=user_obj).count()  
                domain_limit = user_obj.domain_limitation  

                if domain_count_obj >= domain_limit:
                    return JsonResponse({
                        "error": "Domain limit exceeded. Please upgrade your limit.",
                        "success": False,
                    }, status=409)
                    
            except user_detail.DoesNotExist:
                return JsonResponse({"error": "User details not found.","success": False}, status=404)
        
        workspace_slug_id = request.data.get('workspace_slug_id')
        
        if not (workspace_slug_id):
            return JsonResponse({"error": "workspace slug required fields.","success": False}, status=400)
    
        print(workspace_slug_id,'workspace_slug_id')
        
        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found ","success": False}, status=404)

        manager_objs = ''
        manager_slug_ids = request.data.get('manager_slug_id')  
        print(manager_slug_ids,'manager_slug_ids')
        if manager_slug_ids:
            manager_objs_list = manager_slug_ids.split(",")
            print(manager_objs_list,'manager_objs_list') 
            try:
                manager_objs_list = [data for data in manager_objs_list]
                manager_objs = user_detail.objects.filter(slug_id__in=manager_objs_list,workspace_id=workspace_obj)
                if len(manager_objs) != len(manager_objs_list):
                    return JsonResponse({"error": "manager do not belong to the specified workspace.","success": False}, status=400)

            except user_detail.DoesNotExist:
                return JsonResponse({"error": "manager not found ","success": False}, status=404)

        writer_objs = ''
        writer_slug_ids = request.data.get('writer_slug_id') 
        if writer_slug_ids:
            writer_objs_list = writer_slug_ids.split(",") 
            try:
                writer_objs_list = [data for data in writer_objs_list]
                writer_objs = user_detail.objects.filter(slug_id__in=writer_objs_list,workspace_id=workspace_obj)
                if len(manager_objs) != len(manager_objs_list):
                    return JsonResponse({"error": "writer do not belong to the specified workspace.","success": False}, status=400)
                
            except user_detail.DoesNotExist:
                return JsonResponse({"error": "writer not found ","success": False}, status=404)


        wordpress_username = request.data.get('wordpress_username')        
        wordpress_application_password = request.data.get('wordpress_application_password')        
        domain_name = request.data.get('name')        
        permalinks = request.data.get('permalinks')        


        data={
            "name":domain_name,
            "wordpress_username":wordpress_username,
            "wordpress_application_password":wordpress_application_password,
            "new_perma_links":permalinks,
        }

        perma_links_response = get_perma_links(data)

        current_structure = perma_links_response.get('current_structure')

        print(current_structure,'current_structure')
        print(permalinks,'permalinks')

        new_structure = current_structure

        if permalinks != current_structure:
            update_response = update_perma_links(data)
            new_structure = update_response.get('new_structure')
        
        print(new_structure,'new_structure')
             
        data = request.data.copy()
        data["created_by"] = request_user.id  
        data["workspace_id"] = workspace_obj.id  
        data["permalinks"] = new_structure  


        # Serialize and validate the data
        serialized_data = domain_serializer(data=data)

        if serialized_data.is_valid():
            # Save the domain with related fields
            domain_instance = serialized_data.save()
            
            # Associate manager and writer ManyToMany fields
            if manager_objs:
                domain_instance.manager_id.set(manager_objs)
            if writer_objs:
                domain_instance.writer_id.set(writer_objs)
                
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
        print("This error is add_domain --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


# update domain
@api_view(['PATCH'])
@workspace_permission_required
def update_domain(request, slug_id):
    try:
        request_user = request.user
        
        try:
            obj = domain.objects.get(slug_id=slug_id)
        except domain.DoesNotExist:
            return JsonResponse({
                "error": "domain not found.",
                "success": False,
            }, status=404)   

        workspace_slug_id = request.data.get('workspace_slug_id')

        if not (workspace_slug_id):
            return JsonResponse({"error": "workspace slug required fields.","success": False}, status=400)
        
        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission.",
                "success": False,
            }, status=403)
                    
        try:
            workspace_obj = workspace.objects.get(slug_id=workspace_slug_id)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found ","success": False}, status=404)

        manager_objs = None
        manager_slug_ids = request.data.get('manager_slug_id')  
        if manager_slug_ids:
            manager_objs_list = manager_slug_ids.split(",") 
            try:
                manager_objs_list = [data for data in manager_objs_list]
                manager_objs = user_detail.objects.filter(slug_id__in=manager_objs_list,workspace_id=workspace_obj)
                if len(manager_objs) != len(manager_objs_list):
                    return JsonResponse({"error": "manager do not belong to the specified workspace.","success": False}, status=400)

            except user_detail.DoesNotExist:
                return JsonResponse({"error": "manager not found ","success": False}, status=404)
            
        writer_objs = None
        writer_slug_ids = request.data.get('writer_slug_id') 
        if writer_slug_ids:
            writer_objs_list = writer_slug_ids.split(",") 
            try:
                writer_objs_list = [data for data in writer_objs_list]
                writer_objs = user_detail.objects.filter(slug_id__in=writer_objs_list,workspace_id=workspace_obj)
                if len(manager_objs) != len(manager_objs_list):
                    return JsonResponse({"error": "writer do not belong to the specified workspace.","success": False}, status=400)
                
            except user_detail.DoesNotExist:
                return JsonResponse({"error": "writer not found "}, status=404)


        data = request.data.copy()
        data['created_by'] = obj.created_by.id
        data["workspace_id"] = workspace_obj.id 

        # Serialize and validate the data
        serialized_data = domain_serializer(instance=obj, data=data, partial=True) 

        if serialized_data.is_valid():
            # Save the domain with related fields
            domain_instance = serialized_data.save()
            
            # Associate manager and writer ManyToMany fields
            if manager_objs:
                domain_instance.manager_id.set(manager_objs)
            
            if writer_objs:
                domain_instance.writer_id.set(writer_objs)
                
            return JsonResponse({
                "message": "Data updated successfully.",
                "success": True,
                "data": serialized_data.data,
            }, status=200)
        else:
            return JsonResponse({
                "error": "Invalid data.",
                "errors": serialized_data.errors, 
                "success": False,
            }, status=400)

    except Exception as e:
        print("This error is update_domain --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# delete domain
@api_view(['DELETE'])
@workspace_permission_required
def delete_domain(request, slug_id):
    try:
        try:
            obj = domain.objects.get(slug_id=slug_id)
        except domain.DoesNotExist:
            return JsonResponse({
                "error": "domain not found.",
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
        print("This error is delete_domain --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


