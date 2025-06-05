from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import article_serializer
from apiApp.models import article, article_info, domain, workspace, article_type, prompt, wp_author, wp_category, wp_tag, user_detail
import base64
import requests
from apiApp.views.base.s3.article_josn_method.create_article_folder_and_file_s3.create_article_folder_and_file_s3 import create_article_folder_and_file_s3
from apiApp.views.base.s3.article_josn_method.delete_file_from_s3.delete_file_from_s3 import delete_file_from_s3
from apiApp.views.base.s3.article_josn_method.show_file_from_s3.show_file_from_s3 import show_file_from_s3

from apiApp.views.decorator.workspace_decorator import workspace_permission_required
from apiApp.views.decorator.domain_decorator import domain_permission_required
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination
import threading

from apiApp.views.article.supportive_methods.add_manual_article import add_manual_article
from apiApp.views.article.supportive_methods.add_ai_article import add_ai_article
from apiApp.views.article.supportive_methods.create_input_json import create_input_json
from apiApp.views.rabbitmq_api.send_rabbitmq_message_api.send_rabbitmq_message_api import send_rabbitmq_message_api



# show article
@api_view(['GET'])
# @workspace_permission_required
@domain_permission_required
def list_article(request):
    try:
        request_user = request.user

        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
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
            filters &= Q(wp_title__icontains=search) 

        if request_user.is_superuser:
            try:
                obj = article.objects.filter(filters).order_by(order_by) 
            except article.DoesNotExist:
                return JsonResponse({
                    "error": "article not found.",
                    "success": False,
                }, status=404)  

        if request.is_admin:
            try:
                user_obj = user_detail.objects.get(user_id=request_user.id) 
            except user_detail.DoesNotExist:
                return JsonResponse({
                    "error": "user not found.",
                    "success": False,
                }, status=404)

            if request.is_admin:
                try:
                    obj = article.objects.filter(filters).distinct().order_by(order_by)
                except article.DoesNotExist:
                    return JsonResponse({
                        "error": "article not found.",
                        "success": False,
                    }, status=404)
                
        print(obj,'obj0')    
        
        
        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        serialized_data = article_serializer(obj, many=True)
        
        # s3_url = 's3://article-innovator-article-josn-files/ronak-wolf.botxbyte.com/87676037-9254-40d8-bd0a-dbb7cdf8687d/article_content.json'
        # s3_url = 's3://article-innovator-article-josn-files/ronak-wolf.botxbyte.com/33f8c175-b727-4b0e-a768-11b631c5ce79/article_content.json'
        s3_url = 's3://article-innovator-article-josn-files/ronak-wolf.botxbyte.com/ac32a588-6319-4872-a452-b21baa69313b/article_content.json'
        response = show_file_from_s3(s3_url)
        print(response,'response')

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
        print("This error is list_article --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)




# add article
@api_view(['POST'])
# @workspace_permission_required
@domain_permission_required
def add_article(request):
    try:
        request_user = request.user
        
        article_type_slug_id = request.data.get('article_type_slug_id')
    
        if not article_type_slug_id:
            return JsonResponse({"error": "article_type_slug_id is required."}, status=400)

        print(article_type_slug_id,'article_type_slug_idx')
        try:
            article_type_obj = article_type.objects.get(slug_id=article_type_slug_id)
        except article_type.DoesNotExist:
            return JsonResponse({"error": "Invalid article_type_slug_id."}, status=400)

        article_type_category = article_type_obj.article_category.lower()
        print(article_type_category,'article_type_category')

        response = None
        if article_type_category in ["outliner", "generative", "rephrase"]:
            print('jjjjjjjjjjjjjj')
            response = add_ai_article(request_user, request.data)
            print(response,'ssxxss')
            
            
            if response.get("success"):
                # Run rabbitmq_api in the background
                def run_rabbitmq_api():
                    input_json = create_input_json(response.get("article_slug_id"))
                    print(input_json,'input_jsonsssssddfd')
                    # send_rabbitmq_message_api(input_json)

                threading.Thread(target=run_rabbitmq_api).start()


        elif article_type_category == "manual":
            print('xxxxxxxxxxxxxxx')
            
            response = add_manual_article(request_user, request.data)

        print(response,'response')
        
        if response.get("success"):
            return JsonResponse(response, status=200)
        elif "error" in response:
            return JsonResponse(response, status=400)
        else:
            return JsonResponse({"error": "Unexpected error."}, status=500)

        
        
        
        
        
        # temp_article_type = request.data.get('temp_article_type')
        # article_type_slug_id = request.data.get('article_type_slug_id')
        # prompt_slug_id = request.data.get('prompt_slug_id')
        # domain_slug_id = request.data.get('domain_slug_id')
        # author_slug_id = request.data.get('author_slug_id')
        # category_slug_id = request.data.get('category_slug_id')
        # tag_slug_id = request.data.get('tag_slug_id')
        # workspace_slug_id = request.data.get('workspace_slug_id')

        # wp_title = request.data.get('wp_title')
        # keyword = request.data.get('keyword')
        # url = request.data.get('url')    
        # wp_content = request.data.get('wp_content')
        # article_status = request.data.get('article_status')
        # wp_featured_image = request.data.get('wp_featured_image')
        # wp_excerpt = request.data.get('wp_excerpt')
        # wp_status = request.data.get('wp_status')        
        # wp_schedule_time = request.data.get('wp_schedule_time')
        # wp_slug=request.data.get('wp_slug')                
                
        # print(temp_article_type, '-> temp_article_type')
        # print(article_type_slug_id, '-> article_type_slug_id')
        # print(prompt_slug_id, '-> prompt_slug_id')
        # print(domain_slug_id, '-> domain_slug_id')
        # print(author_slug_id, '-> author_slug_id')
        # print(category_slug_id, '-> category_slug_id')
        # print(tag_slug_id, '-> tag_slug_id')
        # print(workspace_slug_id, '-> workspace_slug_id')
        # print(wp_title, '-> wp_title')
        # print(keyword, '-> keyword')
        # print(url, '-> url')
        # print(wp_content, '-> wp_content')
        # print(article_status, '-> article_status')
        # print(wp_featured_image, '-> wp_featured_image')
        # print(wp_excerpt, '-> wp_excerpt')
        # print(wp_status, '-> wp_status')
        # print(wp_schedule_time, '-> wp_schedule_time')
        # print(wp_slug, '-> wp_slug')
                
        # if temp_article_type == 'manual':
            
        #     if not (article_type_slug_id and author_slug_id and domain_slug_id and category_slug_id and tag_slug_id and workspace_slug_id):
        #         return JsonResponse({
        #             "error": "article_type, domain, author, category, tag, workspace slug required fields.",
        #             "success": False,
        #         }, status=400)
                
        # if temp_article_type == 'ai':
            
        #     if not ( prompt_slug_id and domain_slug_id and workspace_slug_id):
        #         return JsonResponse({
        #             "error": "prompt, domain, workspace slug required fields.",
        #             "success": False,
        #         }, status=400)
        
        # try:
        #     domain_obj = domain.objects.get(slug_id = domain_slug_id)
        #     workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
        #     article_type_obj = article_type.objects.get(slug_id = article_type_slug_id)

        #     wp_author_obj = None
        #     if temp_article_type == 'manual':
        #         wp_author_obj = wp_author.objects.get(slug_id = author_slug_id)
        #         # wp_tag_obj = wp_tag.objects.get(slug_id = tag_slug_id)
        #         # wp_category_id = wp_category.objects.get(slug_id = category_slug_id)
        #     prompt_obj = None
        #     if prompt_slug_id:
        #         if temp_article_type == 'ai':
        #             prompt_obj = prompt.objects.get(slug_id = prompt_slug_id)
        #             # Check if the prompt is associated with the given article type
        #             if prompt_obj.article_type_id != article_type_obj:
        #                 return JsonResponse({
        #                     "error": "The selected prompt is not associated with the given article type.",
        #                     "success": False,
        #                 }, status=400)
                    
        # except domain.DoesNotExist:
        #     return JsonResponse({"error": "domain not found.","success": False}, status=404)
        # except workspace.DoesNotExist:
        #     return JsonResponse({"error": "workspace not found.","success": False}, status=404)
        # except article_type.DoesNotExist:
        #     return JsonResponse({"error": "article type not found.","success": False}, status=404)
        # except prompt.DoesNotExist:
        #     return JsonResponse({"error": "prompt not found.","success": False}, status=404)
        # except wp_author.DoesNotExist:
        #     return JsonResponse({"error": "author not found.","success": False}, status=404)
        # # except wp_tag.DoesNotExist:
        # #     return JsonResponse({"error": "tag not found."}, status=404)
        # # except wp_category.DoesNotExist:
        # #     return JsonResponse({"error": "category not found."}, status=404)

        # category_ids = None
        # tag_ids = None

        # if temp_article_type == 'manual':
        
        #     wp_slug = domain_obj.name + '/' +wp_slug
            
        #     if category_slug_id:
        #         #  get category ids 
        #         category_objs_list = category_slug_id.split(",")
        #         category_objs_list = [data for data in category_objs_list]

        #         # Now filter the  objects using the list of IDs
        #         category_ids = wp_category.objects.filter(slug_id__in=category_objs_list)
            
        #     if tag_slug_id:
        #         #  get tag ids 
        #         tag_objs_list = tag_slug_id.split(",")
        #         tag_objs_list = [data for data in tag_objs_list]

        #         # Now filter the  objects using the list of IDs
        #         tag_ids = wp_tag.objects.filter(slug_id__in=tag_objs_list)

        
        # #  api call
        # username = domain_obj.name
        # user_login = domain_obj.wordpress_username
        # password = domain_obj.wordpress_application_password

        # api_url = f'https://{username}/wp-json/botxbyte/v1/dynamic-article-publish/'

        # credentials = base64.b64encode(f'{user_login}:{password}'.encode('utf-8')).decode('utf-8')
        # data = {
        #     "post_title": f"{wp_title}",
        #     "content": f"{wp_content}",
        #     "keyword": f"{keyword}",
        #     "category": f"{article_status}",
        #     "wp_slug": f"{wp_slug}",
        #     "status": f"{wp_status}",
        #     "wp_featured_image": f"{wp_featured_image}",
        #     "wp_schedule_time": f"{wp_schedule_time}",
        #     "wp_excerpt": f"{wp_excerpt}",
        # }

        # headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': f'Basic {credentials}',
        # }

        # response = requests.post(api_url, headers=headers, json=data)
        # print(response.json(),'0000')
        # response_data = response.json()
        # wp_post_id = response_data.get('post_id')

        # if response.status_code in (200, 201):
        #     article_obj = article()
        #     article_obj.wp_title = wp_title
        #     article_obj.keyword = keyword
        #     article_obj.wp_slug = wp_slug
        #     article_obj.article_status = article_status
        #     article_obj.user_id = request_user
        #     article_obj.wp_featured_image = wp_featured_image
        #     article_obj.url = url
        #     article_obj.wp_post_id = wp_post_id
            
        #     # article_obj.wp_status = wp_status
        #     wp_status_choices = dict(article.WP_STATUS_CHOICES)
            
        #     if wp_status in wp_status_choices:
        #         article_obj.wp_status = wp_status

        #     if wp_status == 'scheduled' and wp_schedule_time:
        #         article_obj.wp_schedule_time = wp_schedule_time

        #     if prompt_obj:
        #         article_obj.prompt_id = prompt_obj
        #     article_obj.article_type_id = article_type_obj
        #     article_obj.domain_id = domain_obj
        #     article_obj.workspace_id = workspace_obj
            
        #     if wp_author_obj:
        #         article_obj.wp_author_id = wp_author_obj
                            
        #     article_obj.save()
            
        #     if tag_ids:
        #         article_obj.wp_tag_id.set(tag_ids)
        #     if category_ids:
        #         article_obj.wp_category_id.set(category_ids)
               
        #     temp_article_id = article_obj.id
        #     print(temp_article_id,'temp_article_id')
    
        #     data = {
        #         "domain_slug_id": f"{article_obj.domain_id.name}",
        #         "article_slug_id": f"{article_obj.slug_id}",
        #         "wp_content": f"{wp_content}",
        #         "wp_excerpt": f"{wp_excerpt}"
        #     }

        #     try:
        #         s3_file_path = create_article_folder_and_file_s3(data)
        #         print(s3_file_path,'s3_file_path')

        #         #  save url of 
        #         article_obj = article.objects.get(id = temp_article_id)
        #         article_obj.wp_content = s3_file_path
        #         article_obj.wp_excerpt = s3_file_path
        #         article_obj.save()
        #     except Exception as e:
        #         print("This error is add_article in call this create_article_folder_and_file_s3  --->: ", e)
        #         return JsonResponse({"error": "Internal server error.","success": False}, status=500)
               
        #     return JsonResponse({
        #         "message": "Data added successfully.",
        #         "success": True,
        #         # "article": serialized_data.data,
        #     }, status=200)
        # else:
        #     return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}","success": False}, status=500)

    except Exception as e:
        print("This error is add_article --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
    
    
    
    
# update article
@api_view(['PATCH'])
# @workspace_permission_required
@domain_permission_required
def update_article(request, slug_id):
    try:

        try:
            obj = article.objects.get(slug_id=slug_id)
        except article.DoesNotExist:
            return JsonResponse({
                "error": "article not found.",
            }, status=404)   

        temp_article_type = request.data.get('temp_article_type')
        article_type_slug_id = request.data.get('article_type_slug_id')
        prompt_slug_id = request.data.get('prompt_slug_id')
        domain_slug_id = request.data.get('domain_slug_id')
        author_slug_id = request.data.get('author_slug_id')
        category_slug_id = request.data.get('category_slug_id')
        tag_slug_id = request.data.get('tag_slug_id')
        workspace_slug_id = request.data.get('workspace_slug_id')

        wp_title = request.data.get('wp_title')
        keyword = request.data.get('keyword')
        url = request.data.get('url')    
        wp_content = request.data.get('wp_content')
        article_status = request.data.get('article_status')
        wp_featured_image = request.data.get('wp_featured_image')
        wp_excerpt = request.data.get('wp_excerpt')
        wp_status = request.data.get('wp_status')        
        wp_schedule_time = request.data.get('wp_schedule_time')
        wp_slug=request.data.get('wp_slug')
        
        
        print(temp_article_type, '-> temp_article_type')
        print(article_type_slug_id, '-> article_type_slug_id')
        print(prompt_slug_id, '-> prompt_slug_id')
        print(domain_slug_id, '-> domain_slug_id')
        print(author_slug_id, '-> author_slug_id')
        print(category_slug_id, '-> category_slug_id')
        print(tag_slug_id, '-> tag_slug_id')
        print(workspace_slug_id, '-> workspace_slug_id')
        print(wp_title, '-> wp_title')
        print(keyword, '-> keyword')
        print(url, '-> url')
        print(wp_content, '-> wp_content')
        print(article_status, '-> article_status')
        print(wp_featured_image, '-> wp_featured_image')
        print(wp_excerpt, '-> wp_excerpt')
        print(wp_status, '-> wp_status')
        print(wp_schedule_time, '-> wp_schedule_time')
        print(wp_slug, '-> wp_slug')        

        if temp_article_type == 'manual':
            
            if not (article_type_slug_id and author_slug_id and domain_slug_id and category_slug_id and tag_slug_id and workspace_slug_id):
                return JsonResponse({
                    "error": "article_type, domain, author, category, tag, workspace slug required fields.",
                    "success": False,
                }, status=400)
                
        if temp_article_type == 'ai':
            
            if not ( prompt_slug_id and domain_slug_id and workspace_slug_id):
                return JsonResponse({
                    "error": "prompt, domain, workspace slug required fields.",
                    "success": False,
                }, status=400)
                
        # if not (article_type_slug_id and prompt_slug_id and author_slug_id and domain_slug_id and category_slug_id and tag_slug_id and workspace_slug_id):
        #     return JsonResponse({
        #         "error": "article_type, prompt, domain, author, category, tag, workspace slug required fields."
        #     }, status=400)
            
        if (obj.workspace_id.slug_id != workspace_slug_id):
            return JsonResponse({
                "error": "You Don't have permission."
            }, status=404)
            
        try:
            domain_obj = domain.objects.get(slug_id = domain_slug_id)
            workspace_obj = workspace.objects.get(slug_id = workspace_slug_id)
            article_type_obj = article_type.objects.get(slug_id = article_type_slug_id)

            wp_author_obj = None
            if temp_article_type == 'manual':
                wp_author_obj = wp_author.objects.get(slug_id = author_slug_id)
                # wp_tag_obj = wp_tag.objects.get(slug_id = tag_slug_id)
                # wp_category_id = wp_category.objects.get(slug_id = category_slug_id)
            prompt_obj = None
            if prompt_slug_id:
                if temp_article_type == 'ai':
                    prompt_obj = prompt.objects.get(slug_id = prompt_slug_id)
                    # Check if the prompt is associated with the given article type
                    if prompt_obj.article_type_id != article_type_obj:
                        return JsonResponse({
                            "error": "The selected prompt is not associated with the given article type.",
                            "success": False,
                        }, status=400)
                    
        except domain.DoesNotExist:
            return JsonResponse({"error": "domain not found.","success": False}, status=404)
        except workspace.DoesNotExist:
            return JsonResponse({"error": "workspace not found.","success": False}, status=404)
        except article_type.DoesNotExist:
            return JsonResponse({"error": "article type not found.","success": False}, status=404)
        except prompt.DoesNotExist:
            return JsonResponse({"error": "prompt not found.","success": False}, status=404)
        except wp_author.DoesNotExist:
            return JsonResponse({"error": "author not found.","success": False}, status=404)
        # except wp_tag.DoesNotExist:
        #     return JsonResponse({"error": "tag not found."}, status=404)
        # except wp_category.DoesNotExist:
        #     return JsonResponse({"error": "category not found."}, status=404)

        wp_slug = domain_obj.name + '/' +wp_slug

        #  get category ids 
        category_objs_list = category_slug_id.split(",")
        category_objs_list = [data for data in category_objs_list]

        # Now filter the  objects using the list of IDs
        category_ids = wp_category.objects.filter(slug_id__in=category_objs_list)
        
        #  get tag ids 
        tag_objs_list = tag_slug_id.split(",")
        tag_objs_list = [data for data in tag_objs_list]

        # Now filter the  objects using the list of IDs
        tag_ids = wp_tag.objects.filter(slug_id__in=tag_objs_list)


        #  api call
        domain_name = domain_obj.name
        username = domain_obj.wordpress_username
        password = domain_obj.wordpress_application_password

        api_url = f'https://{domain_name}/wp-json/botxbyte/v1/dynamic-article-publish/{obj.wp_post_id}'

        print(api_url,'api_url0120')

        credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
        data = {
            "post_title": f"{wp_title}",
            "content": f"{wp_content}",
            "keyword": f"{keyword}",
            "category": f"{article_status}",
            "wp_slug": f"{wp_slug}",
            "status": f"{wp_status}",
            "wp_featured_image": f"{wp_featured_image}",
            "wp_schedule_time": f"{wp_schedule_time}",
            "wp_excerpt": f"{wp_excerpt}",
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {credentials}',
        }

        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code in (200, 201):

            obj.wp_title = wp_title
            obj.keyword = keyword
            obj.wp_slug = wp_slug
            obj.article_status = article_status
            obj.wp_featured_image = wp_featured_image
            obj.url = url
            
            # obj.wp_status = wp_status
            wp_status_choices = dict(article.WP_STATUS_CHOICES)
            
            if wp_status in wp_status_choices:
                obj.wp_status = wp_status

            if wp_status == 'scheduled' and wp_schedule_time:
                obj.wp_schedule_time = wp_schedule_time

            if prompt_obj:
                obj.prompt_id = prompt_obj
            obj.article_type_id = article_type_obj
            obj.domain_id = domain_obj
            obj.workspace_id = workspace_obj
            if wp_author_obj:
                obj.wp_author_id = wp_author_obj
                            
            obj.save()
            
            if tag_ids:
                obj.wp_tag_id.add(*tag_ids)
            if category_ids:
                obj.wp_category_id.add(*category_ids)
               
            temp_article_id = obj.id
    
            data = {
                "domain_slug_id": f"{obj.domain_id.name}",
                "article_slug_id": f"{obj.slug_id}",
                "wp_content": f"{wp_content}",
                "wp_excerpt": f"{wp_excerpt}"
            }

            try:
                s3_file_path = create_article_folder_and_file_s3(data)
                print(s3_file_path,'s3_file_path')

                #  save url of 
                obj = article.objects.get(id = temp_article_id)
                obj.wp_content = s3_file_path
                obj.wp_excerpt = s3_file_path
                obj.save()
            except Exception as e:
                print("This error is update_article in call this create_article_folder_and_file_s3  --->: ", e)
                return JsonResponse({"error": "Internal server error.","success": False}, status=500)
               
        else:
            return JsonResponse({"error": f"WordPress API error: {response.status_code} - {response.text}","success": False}, status=500)
      
        return JsonResponse({
            "message": "Data updated successfully.",
            "success": True,
            # "article": serialized_data.data,
        }, status=200)
    
    except Exception as e:
        print("This error is update_article --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)





# delete article
@api_view(['DELETE'])
# @workspace_permission_required
@domain_permission_required
def delete_article(request, slug_id):
    try:
        try:
            obj = article.objects.get(slug_id=slug_id)
        except article.DoesNotExist:
            return JsonResponse({
                "error": "article not found.",
                "success": False,
            }, status=404) 
            
        print(obj.wp_content)
          
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
     
        #  s3 delete call  
        file_path = obj.wp_content
        delete_file_from_s3(file_path)
             
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_article --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)


