from functools import wraps
from django.http import JsonResponse
from apiApp.models import user_detail, domain, role, role_has_permissions, permission

def domain_permission_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        user = request.user
        
        print('---------- Checking domain permission -----------------')
        print(f"User: {user}, Request Path: {request.path}, Method: {request.method}")
        
        # If the user is a superuser, skip the domain check and proceed with the view
        if user.is_superuser:
            return func(request, *args, **kwargs)
        
        elif not user.is_superuser:

            current_page = request.path.strip('/').rsplit('/', 1)[0] 
            print(current_page,'current_page')
                
            # Get the function name
            try:
                current_url = request.resolver_match.view_name
                print(current_url, 'current_url')
            except AttributeError:
                current_url = None
                print("Function name could not be resolved.")

                
                
            # Extract domain_slug_id based on request method
            if request.method in ['POST', 'PUT']:
                if request.content_type == 'application/json':
                    domain_slug_id = request.data.get('domain_slug_id') 
                else:
                    domain_slug_id = request.POST.get('domain_slug_id')  
            elif request.method == 'GET':
                domain_slug_id = request.GET.get('domain_slug_id')
            elif request.method == 'DELETE':
                domain_slug_id = request.GET.get('domain_slug_id')

            print(domain_slug_id, 'domain_slug_id')
                
                
            # Check if the user is associated with any domain
            try:
                user_details = user_detail.objects.get(user_id=user)
            except user_detail.DoesNotExist:
                return JsonResponse({"error": "User details not found."}, status=400)

            # If the user's role is 'admin', allow access
            if user_details.role_id.name == 'admin':
                print(f"Granted: User {user} is an admin. Skipping domain check.")
                return func(request, *args, **kwargs)


            # # Otherwise, check if the user has access to any domain
            # user_domains = domain.objects.filter(manager_id=user_details) | domain.objects.filter(writer_id=user_details)
            # print(user_domains,'user_domains')
            # print(user_domains.id,'user_domains')
            try:
                domain_obj = domain.objects.get(slug_id = domain_slug_id)
            except domain.DoesNotExist:
                return JsonResponse({
                    "error": "domain not found.",
                }, status=404)   

            # Check if the request_user is a manager or writer of the domain
            if domain_obj.manager_id.filter(user_id=user).exists():
                domain_user = domain_obj.manager_id.get(user_id=user)
                role_name = 'manager'
  
            elif domain_obj.writer_id.filter(user_id=user).exists():
                domain_user = domain_obj.writer_id.get(user_id=user)
                role_name = 'writer'
            else:
                role_name = None
                
            
            # print(role_name)
            if role_name == 'manager':
                print(current_url,'current_url')
                # permission_url = [
                #     'update_tag', 'add_tag', 'delete_tag', 'list_tag', 'add_author', 'update_author', 'list_author', 'delete_author',
                #     'add_category', 'update_category', 'list_category', 'delete_category', 'add_article', 'update_article', 'list_article' , 'delete_article',
                #     'add_prompt', 'update_prompt', 'list_prompt', 'detele_prompt', 'list_competitor', 'add_competitor', 'update_competitor', 'delete_competitor',
                #     'list_competitor_domain_mapping', 'add_competitor_domain_mapping', 'update_competitor_domain_mapping', 'delete_competitor_domain_mapping', 
                #     'list_competitor_sitemap_url', 'add_competitor_sitemap_url', 'update_competitor_sitemap_url', 'delete_competitor_sitemap_url',
                #     'list_competitor_sitemap_url_mapping', 'add_competitor_sitemap_url_mapping', 'update_competitor_sitemap_url_mapping', 'delete_competitor_sitemap_url_mapping',
                #     'list_competitor_article_url', 'add_competitor_article_url', 'update_competitor_article_url', 'delete_competitor_article_url',
                #     'list_competitor_article_url_mapping', 'add_competitor_article_url_mapping', 'update_competitor_article_url_mapping', 'delete_competitor_article_url_mapping',
                #     'list_competitor_extraction', 'add_competitor_extraction', 'update_competitor_extraction', 'delete_competitor_extraction',
                #     'list_competitor_extraction_mapping', 'add_competitor_extraction_mapping', 'update_competitor_extraction_mapping', 'delete_competitor_extraction_mapping',
                #     'list_competitor_seo_extraction_mapping', 'add_competitor_seo_extraction_mapping', 'update_competitor_seo_extraction_mapping', 'delete_competitor_seo_extraction_mapping',
                #     # '', '', '', '',
                #     # '', '', '', '',
                #     # '', '', '', '',
                    
                # ]
                role_obj = role.objects.get(name='manager')
            
                # Get all permissions assigned to the role
                role_permissions = role_has_permissions.objects.filter(role_id=role_obj)
                permission_url = role_permissions.values_list('permission_id__name', flat=True)

                if current_url in permission_url:
                    print("Permission granted for this URL.")
                    return func(request, *args, **kwargs)

            if role_name == 'writer':
                print(current_url,'current_url')
                # permission_url = [
                #     'update_tag', 'add_tag', 'delete_tag', 'list_tag', 'add_author', 'update_author', 'list_author', 'delete_author',
                #     'add_category', 'update_category', 'list_category', 'delete_category', 'add_article', 'update_article', 'list_article' , 'delete_article',
                #     'add_prompt', 'update_prompt', 'list_prompt', 'detele_prompt', 'list_competitor', 'add_competitor', 'update_competitor', 'delete_competitor',
                #     'list_competitor_domain_mapping', 'add_competitor_domain_mapping', 'update_competitor_domain_mapping', 'delete_competitor_domain_mapping', 
                #     'list_competitor_sitemap_url', 'add_competitor_sitemap_url', 'update_competitor_sitemap_url', 'delete_competitor_sitemap_url',
                #     'list_competitor_sitemap_url_mapping', 'add_competitor_sitemap_url_mapping', 'update_competitor_sitemap_url_mapping', 'delete_competitor_sitemap_url_mapping',
                #     'list_competitor_article_url', 'add_competitor_article_url', 'update_competitor_article_url', 'delete_competitor_article_url',
                #     'list_competitor_article_url_mapping', 'add_competitor_article_url_mapping', 'update_competitor_article_url_mapping', 'delete_competitor_article_url_mapping',
                #     'list_competitor_extraction', 'add_competitor_extraction', 'update_competitor_extraction', 'delete_competitor_extraction',
                #     'list_competitor_extraction_mapping', 'add_competitor_extraction_mapping', 'update_competitor_extraction_mapping', 'delete_competitor_extraction_mapping',
                #     'list_competitor_seo_extraction_mapping', 'add_competitor_seo_extraction_mapping', 'update_competitor_seo_extraction_mapping', 'delete_competitor_seo_extraction_mapping',
                # ]
                role_obj = role.objects.get(name='writer')
            
                # Get all permissions assigned to the role
                role_permissions = role_has_permissions.objects.filter(role_id=role_obj)
                permission_url = role_permissions.values_list('permission_id__name', flat=True)

                if current_url in permission_url:
                    print("Permission granted for this URL.")
                    return func(request, *args, **kwargs)
                
        # Default response if no conditions are met
        return JsonResponse({"error": "Permission denied or invalid request."}, status=403)
                

    return wrap
