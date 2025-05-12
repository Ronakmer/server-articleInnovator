from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from apiApp.serializers import article_type_serializer, article_type_field_serializer
from apiApp.models import article_type, article_type_field, color_detail
from django.db.models import Q
from apiApp.views.base.process_pagination.process_pagination import process_pagination
from apiApp.views.variables.variables import add_variables, update_variables

from apiApp.views.rabbitmq_api.create_rabbitmq_queues_for_article_type.create_rabbitmq_queues_for_article_type import create_rabbitmq_queues_for_article_type
from apiApp.views.rabbitmq_api.delete_rabbitmq_queues_for_article_type.delete_rabbitmq_queues_for_article_type import delete_rabbitmq_queues_for_article_type
from apiApp.views.rabbitmq_api.update_rabbitmq_queues_for_article_type.update_rabbitmq_queues_for_article_type import update_rabbitmq_queues_for_article_type

import threading


# show article type
@api_view(['GET'])
def list_article_type(request):
    try:
        # Get query parameters
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        article_category = request.GET.get('article_category', None)
        category = request.GET.get('category', None)
        slug_id = request.GET.get('slug_id', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')
        

        # Initialize filters
        filters = Q()
        
        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if article_category:
            filters &= Q(article_category=article_category)
        if category:
            filters &= Q(category=category)
        if slug_id:
            filters &= Q(slug_id=slug_id)
        if search:
            filters &= Q(name__icontains=search) 

        try:
            obj = article_type.objects.filter(filters).order_by(order_by)
        except article_type.DoesNotExist:
            return JsonResponse({
                "error": "article type not found",
                "success": False,
            }, status=404)

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)

        serialized_data = article_type_serializer(obj, many=True)
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
        print("This error is list_article_type --->: ",e)
        return JsonResponse({"error": "Internal Server error.","success": False}, status=500)



# add article type
@api_view(['POST'])
def add_article_type(request):
    try:
        color_detail_slug_id = request.data.get('color_detail_slug_id') 
        article_type_field_slug_ids = request.data.get('article_type_field_slug_id') 
        supportive_variables_data = request.data.get('supportive_variables_data') 
        print(supportive_variables_data,'supportive_variables_data')
        article_category = request.data.get("article_category")
        print(article_category,'article_category')


        if not color_detail_slug_id:
            return JsonResponse({
                "error": "color detail slug id are required.",
                "success": False,
            }, status=400)

        if article_category != "manual":
            if article_type_field_slug_ids:
                article_type_field_slugs = article_type_field_slug_ids.split(",") 
                
            if not article_type_field_slug_ids:
                return JsonResponse({
                    "error": "article type field slug id are required.",
                    "success": False,
                }, status=400)

            try:
                article_type_field_objs = article_type_field.objects.filter(slug_id__in=article_type_field_slugs)
            except article_type_field.DoesNotExist:
                return JsonResponse({"error": "No matching Article Type Fields found.","success": False}, status=404)

        try:
            color_detail_obj = color_detail.objects.get(slug_id=color_detail_slug_id)
        except color_detail.DoesNotExist:
            return JsonResponse({"error": "Color Detail not found.","success": False}, status=404)


        # Include `color_detail_id` in the request data for the serializer
        data = request.data.copy()
        data['color_detail_id'] = color_detail_obj.id

        serialized_data = article_type_serializer(data=data)
        
        if serialized_data.is_valid():
            
            article_type_obj = serialized_data.save()
            if article_category != "manual":
                article_type_obj.article_type_field_id.set(article_type_field_objs)
                _, error = add_variables(supportive_variables_data, article_type_obj.slug_id)
            
                if error:
                    return JsonResponse({
                        "error": error,
                        "success": False,
                    }, status=400)
            
            def call_create_rabbitmq(slug_id):
                try:
                    rabbitmq_result, error = create_rabbitmq_queues_for_article_type(slug_id)
                    print(rabbitmq_result, 'rabbitmq_result')
                except Exception as ex:
                    print(ex)

            # Start both functions in separate threads
            threading.Thread(target=call_create_rabbitmq, args=(article_type_obj.slug_id,)).start()


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
        print("This error is add_article_type --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)

    
    
# update article type
@api_view(['PATCH'])
def update_article_type(request, slug_id):
    try:
        try:
            obj = article_type.objects.get(slug_id=slug_id)
        except article_type.DoesNotExist:
            return JsonResponse({
                "error": "article type not found.",
                "success": False,
            }, status=404)   
            
            
        status = request.data.get("status")
        if status is not None and status != "":
            serialized_data = article_type_serializer(instance=obj, data=request.data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return JsonResponse({
                    "message": "Status updated successfully.",
                    "success": True,
                    "data": serialized_data.data,
                }, status=200)
            else:
                return JsonResponse({
                    "error": "Invalid data.",
                    "errors": serialized_data.errors,
                    "success": False,
                }, status=400)
                
            
        color_detail_slug_id = request.data.get('color_detail_slug_id') 
        supportive_variables_data = request.data.get('supportive_variables_data') 
        article_category = request.data.get("article_category")

        article_type_field_slug_ids = request.data.get('article_type_field_slug_id') 
        
        if not color_detail_slug_id:
            return JsonResponse({
                "error": "color detail slug id are required.",
                "success": False,
            }, status=400)
        if article_category != "manual":
            if article_type_field_slug_ids:
                article_type_field_slugs = article_type_field_slug_ids.split(",") 
            if not article_type_field_slug_ids:
                return JsonResponse({
                    "error": "article type field slug id are required.",
                    "success": False,
                }, status=400)

            try:
                article_type_field_objs = article_type_field.objects.filter(slug_id__in=article_type_field_slugs)
            except article_type_field.DoesNotExist:
                return JsonResponse({"error": "No matching Article Type Fields found.","success": False}, status=404)
        try:
            color_detail_obj = color_detail.objects.get(slug_id=color_detail_slug_id)
        except color_detail.DoesNotExist:
            return JsonResponse({"error": "Color Detail not found.","success": False}, status=404)

        # Include `color_detail_id` in the request data for the serializer
        data = request.data.copy()
        data['color_detail_id'] = color_detail_obj.id

        serialized_data = article_type_serializer(instance=obj, data=data, partial=True)        
        
        if serialized_data.is_valid():
            article_type_obj = serialized_data.save()
            if article_category != "manual":

                article_type_obj.article_type_field_id.set(article_type_field_objs)
                _, error = update_variables(supportive_variables_data, article_type_obj.slug_id)

                if error:
                    return JsonResponse({
                        "error": error,
                        "success": False,
                    }, status=400)

            def call_update_rabbitmq(slug_id):
                try:
                    rabbitmq_result, error = update_rabbitmq_queues_for_article_type(slug_id)
                    print(rabbitmq_result, 'rabbitmq_result')
                except Exception as ex:
                    print(ex)

            # Start both functions in separate threads
            threading.Thread(target=call_update_rabbitmq, args=(article_type_obj.slug_id,)).start()


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
        print("This error is update_article_type --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# delete article type
@api_view(['DELETE'])
def delete_article_type(request, slug_id):
    try:
        try:
            obj = article_type.objects.get(slug_id=slug_id)
        except article_type.DoesNotExist:
            return JsonResponse({
                "error": "article type not found.",
                "success": False,
            }, status=404) 
            

        rabbitmq_delete_response, delete_error = delete_rabbitmq_queues_for_article_type(slug_id)
        if delete_error or not rabbitmq_delete_response:
            return JsonResponse({
                "error": f"Failed to delete queues for the article_type. {delete_error or rabbitmq_delete_response}",
                "success": False,
            }, status=400)

                
        obj.delete()
        
        return JsonResponse({
            "message": "Data Deleted successfully.",
            "success": True,
        }, status=200)

    except Exception as e:
        print("This error is delete_article_type --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)



# get article type
@api_view(['GET'])
def get_article_type_fields(request, slug_id):
    try:
        try:
            article_type_obj = article_type.objects.get(slug_id = slug_id)
        except article_type.DoesNotExist:
            return JsonResponse({
                "error": "article type not found.",
                "success": False,
            }, status=404) 
            
        fields = article_type_obj.article_type_field_id.filter(status=True)      
        
        serialized_data = article_type_field_serializer(fields, many=True)

        # return JsonResponse(list(fields), safe=False)
        return JsonResponse({
                "message": "successfully.",
                "data_field":serialized_data.data,
                "success": True,
            }, status=200)
    except Exception as e:
        print("This error in get_article_type_fields --->: ", e)
        return JsonResponse({"error": "Internal server error.","success": False}, status=500)
