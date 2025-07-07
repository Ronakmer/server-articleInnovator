from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from competitorApp.serializers import competitor_serializer, competitor_domain_mapping_serializer, competitor_selected_url_serializer
from competitorApp.models import competitor, competitor_article_url, competitor_domain_mapping, competitor_selected_url
from django.db.models import Q
from loguru import logger
import json
from competitorApp.views.base.process_pagination.process_pagination import process_pagination
from competitorApp.views.competitor.supportive_methods.extract_clean_domain import extract_clean_domain
from django.utils import timezone

from competitorApp.views.cronjob.main_checker import send_article_url_to_create_article


@api_view(['GET'])
def list_competitor(request):
    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        status = request.GET.get('status', None)
        competitor_slug_id = request.GET.get('competitor_slug_id', None)
        competitor_domain_name = request.GET.get('competitor_domain_name', None)
        search = request.GET.get('search', '')
        order_by = request.GET.get('order_by', '-created_date')

        # Initialize filters
        filters = Q()
        
        # Apply filters based on provided parameters
        if status:
            filters &= Q(status=status)
        if competitor_slug_id:
            filters &= Q(slug_id=competitor_slug_id)
        if competitor_domain_name:
            filters &= Q(competitor_domain_name=competitor_domain_name)
        if search:
            filters &= (
                Q(slug_id__icontains=search) |
                Q(competitor_domain_name__icontains=search)
            )
            
        try:
            # Use select_related or prefetch_related to fetch domain mappings
            obj = competitor.objects.filter(filters).prefetch_related('competitor_domain_mapping_set').order_by(order_by)
            
        except competitor.DoesNotExist:
            return JsonResponse({
                "error": "competitor not found.",
                "success": False,
            }, status=404) 

        # Apply pagination
        obj, total_count, page, total_pages = process_pagination(obj, offset, limit)
        
        serialized_data = competitor_serializer(obj, many=True)

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
        print("Error in list_competitor:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)


@api_view(['POST'])
def add_competitor(request):
    try:
        data = request.data

        # Extract and clean the domain name
        raw_domain = data.get('competitor_domain_name')
        cleaned_domain = extract_clean_domain(raw_domain)

        # Check if competitor already exists
        existing_competitor = competitor.objects.filter(competitor_domain_name=cleaned_domain).first()

        if existing_competitor:
            # Use existing competitor ID
            competitor_obj = existing_competitor
        else:
            # Create new competitor
            competitor_data = {'competitor_domain_name': cleaned_domain}
            competitor_serialized = competitor_serializer(data=competitor_data)
            if competitor_serialized.is_valid():
                competitor_obj = competitor_serialized.save()
            else:
                return JsonResponse({
                    "error": "Invalid competitor data.",
                    "errors": competitor_serialized.errors,
                    "success": False
                }, status=400)
            
        
        wp_category = {"category_slug_id": data["category_slug_id_ai"]} if data.get("category_slug_id_ai") else ''
        wp_tag = {"tag_slug_id": data["tag_slug_id_ai"]} if data.get("tag_slug_id_ai") else ''
        prompt = {"prompt_slug_id": data["prompt_slug_id"]} if data.get("prompt_slug_id") else ''
        article_type = {"article_type_slug_id": data["article_type_slug_id"]} if data.get("article_type_slug_id") else ''
        wp_schedule_time = data.get('wp_schedule_time') if data.get('wp_status') == 'future' else None

        # Now create or update the domain mapping
        domain_mapping_data = {
            'competitor_id': competitor_obj.pk,
            'domain_id': data.get('domain_slug_id',''),
            'workspace_id': data.get('workspace_slug_id',''),
            'wp_status': data.get('wp_status',''),
            'article_status': data.get('article_status'),
            'wp_schedule_time': wp_schedule_time,
            'article_priority': data.get('article_priority', 0),
            'ai_content_flags': data.get('ai_content_flags', {}),
            'wp_author': data.get('author_slug_id_ai'),
            'wp_category': wp_category,
            'wp_tag': wp_tag,
            'prompt': prompt,
            'article_type': article_type,
            'competitor_type': data.get('competitor_type', 'sitemap'),
            'interval': data.get('interval', 30),
            'interval_unit': data.get('interval_unit', 'minute'),
            'created_by': data.get('created_by'),
            'workspace': data.get('workspace', {}),
            'domain': data.get('domain', {}),
        }
        print(domain_mapping_data['wp_author'],'domain_mapping_data')

        # Create new domain mapping
        domain_mapping_serialized = competitor_domain_mapping_serializer(data=domain_mapping_data)
        if domain_mapping_serialized.is_valid():
            domain_mapping_obj = domain_mapping_serialized.save()
            
            # Handle URLs if provided
            urls_data = data.get('selected_urls', '[]')
            # Parse JSON string if it's a string, otherwise use as is
            if isinstance(urls_data, str):
                try:
                    urls = json.loads(urls_data)
                except json.JSONDecodeError:
                    urls = []
            else:
                urls = urls_data if isinstance(urls_data, list) else []
            
            print(urls,'urls')
            if urls:
                # Get existing URLs for this competitor and domain mapping
                existing_urls = competitor_selected_url.objects.select_related('competitor_id', 'competitor_domain_mapping_id').filter(
                    competitor_id__slug_id=competitor_obj.slug_id,
                    competitor_domain_mapping_id__slug_id=domain_mapping_obj.slug_id
                ).values_list('selected_url', flat=True)

                existing_urls_set = set(existing_urls)
                new_urls_set = set(url['url'] for url in urls if isinstance(url, dict))

                # URLs to add (in new set but not in existing set)
                urls_to_add = new_urls_set - existing_urls_set

                # Add new URLs
                new_urls_data = []
                for url_obj in urls:
                    if not isinstance(url_obj, dict) or 'url' not in url_obj:
                        continue
                        
                    if url_obj['url'] in urls_to_add:
                        url_data = {
                            'competitor_id': competitor_obj.pk,
                            'competitor_domain_mapping_id': domain_mapping_obj.pk,
                            'selected_url': url_obj['url'],
                            'monitor_enabled': url_obj.get('monitor_enabled', True),
                            'start_time': url_obj.get('start_time') or timezone.now(),
                            'end_time': url_obj.get('end_time') or timezone.now(),
                            'proxy': url_obj.get('proxy', ''),
                            'created_by': data.get('created_by')
                        }
                        new_urls_data.append(url_data)

                # Bulk create new URLs
                if new_urls_data:
                    url_serializer = competitor_selected_url_serializer(data=new_urls_data, many=True)
                    if url_serializer.is_valid():
                        url_serializer.save()
                    else:
                        # If URL creation fails, continue without URLs
                        print("Error adding URLs:", url_serializer.errors)

        else:
            # If mapping creation fails and competitor was newly created, delete the competitor
            if not existing_competitor:
                competitor_obj.delete()
            return JsonResponse({
                "error": "Invalid domain mapping data.",
                "errors": domain_mapping_serialized.errors,
                "success": False
            }, status=400)

        serialized_competitor = competitor_serializer(competitor_obj)
        serialized_domain_mapping = competitor_domain_mapping_serializer(domain_mapping_obj)
        return JsonResponse({
            "message": "Competitor and domain mapping added successfully.",
            "data": {
                "competitor": serialized_competitor.data,
                "domain_mapping_data": serialized_domain_mapping.data
            },
            "success": True
        }, status=200)

    except Exception as e:
        print("Error in add_competitor:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)

@api_view(['PATCH'])
def update_competitor(request, competitor_slug_id):
    try:
        data = json.loads(request.body)

        # Fetch the competitor object
        try:
            competitor_obj = competitor.objects.get(slug_id=competitor_slug_id)
        except competitor.DoesNotExist:
            return JsonResponse({
                "error": "Competitor not found.",
                "success": False
            }, status=404)

        # Clean domain name
        raw_domain = data.get('competitor_domain_name')
        cleaned_domain = extract_clean_domain(raw_domain)

        # Update competitor data
        competitor_data = {
            'competitor_domain_name': cleaned_domain
        }
        competitor_serialized = competitor_serializer(competitor_obj, data=competitor_data, partial=True)
        if competitor_serialized.is_valid():
            competitor_serialized.save()
        else:
            return JsonResponse({
                "error": "Invalid competitor data.",
                "errors": competitor_serialized.errors,
                "success": False
            }, status=400)


        wp_category = {"category_slug_id": data["category_slug_id_ai"]} if data.get("category_slug_id_ai") else ''
        wp_tag = {"tag_slug_id": data["tag_slug_id_ai"]} if data.get("tag_slug_id_ai") else ''
        prompt = {"prompt_slug_id": data["prompt_slug_id"]} if data.get("prompt_slug_id") else ''
        article_type = {"article_type_slug_id": data["article_type_slug_id"]} if data.get("article_type_slug_id") else ''
        wp_schedule_time = data.get('wp_schedule_time') if data.get('wp_status') == 'future' else None


        # Now update or create domain mapping
        domain_mapping_data = {
            'competitor_id': competitor_obj.pk,
            'domain_id': data.get('domain_id',''),
            'workspace_id': data.get('workspace_id',''),
            'wp_status': data.get('wp_status'),
            'article_status': data.get('article_status'),
            'wp_schedule_time': wp_schedule_time,
            'article_priority': data.get('article_priority', 0),
            'ai_content_flags': data.get('ai_content_flags', {}),
            'wp_author': data.get('author_slug_id_ai'),
            'wp_category': wp_category,
            'wp_tag': wp_tag,
            'prompt': prompt,
            'article_type': article_type,
            'competitor_type': data.get('competitor_type', 'sitemap'),
            'interval': data.get('interval', 30),
            'interval_unit': data.get('interval_unit', 'minute'),
            'created_by': data.get('created_by'),
            'workspace': data.get('workspace', {}),
            'domain': data.get('domain', {}),

        }
        competitor_domain_mapping_slug_id = data.get('competitor_domain_mapping_slug_id')

        # Assuming there's only one mapping per competitor
        domain_mapping_obj = competitor_domain_mapping.objects.select_related('competitor_id').filter(slug_id=competitor_domain_mapping_slug_id).first()
        
        if domain_mapping_obj:
            domain_mapping_serialized = competitor_domain_mapping_serializer(domain_mapping_obj, data=domain_mapping_data, partial=True)
            if domain_mapping_serialized.is_valid():
                domain_mapping_obj = domain_mapping_serialized.save()

                # Handle URLs if provided
                urls_data = data.get('selected_urls', '[]')
                # Parse JSON string if it's a string, otherwise use as is
                if isinstance(urls_data, str):
                    try:
                        urls = json.loads(urls_data)
                    except json.JSONDecodeError:
                        urls = []
                else:
                    urls = urls_data if isinstance(urls_data, list) else []
                
                print(urls,'urls')
                if urls:
                    # Get existing URLs for this competitor and domain mapping
                    existing_urls = competitor_selected_url.objects.select_related('competitor_id', 'competitor_domain_mapping_id').filter(
                        competitor_id__slug_id=competitor_obj.slug_id,
                        competitor_domain_mapping_id__slug_id=domain_mapping_obj.slug_id
                    )

                    # Create a map of existing URLs to their objects
                    existing_urls_map = {url.selected_url: url for url in existing_urls}
                    new_urls_set = {url['url'] for url in urls if isinstance(url, dict)}

                    # URLs to add (in new set but not in existing set)
                    urls_to_add = new_urls_set - set(existing_urls_map.keys())

                    # URLs to delete (in existing set but not in new set)
                    urls_to_delete = set(existing_urls_map.keys()) - new_urls_set

                    # Add new URLs
                    new_urls_data = []
                    for url_obj in urls:
                        if not isinstance(url_obj, dict) or 'url' not in url_obj:
                            continue
                            
                        if url_obj['url'] in urls_to_add:
                            url_data = {
                                'competitor_id': competitor_obj.pk,
                                'competitor_domain_mapping_id': domain_mapping_obj.pk,
                                'selected_url': url_obj['url'],
                                'monitor_enabled': url_obj.get('monitor_enabled', True),
                                'start_time': url_obj.get('start_time') or timezone.now(),
                                'end_time': url_obj.get('end_time') or timezone.now(),
                                'proxy': url_obj.get('proxy', ''),
                                'created_by': data.get('created_by')
                            }
                            new_urls_data.append(url_data)
                        elif url_obj['url'] in existing_urls_map:
                            # Update existing URL
                            existing_url = existing_urls_map[url_obj['url']]
                            existing_url.monitor_enabled = url_obj.get('monitor_enabled', existing_url.monitor_enabled)
                            if url_obj.get('start_time'):
                                existing_url.start_time = url_obj['start_time']
                            if url_obj.get('end_time'):
                                existing_url.end_time = url_obj['end_time']
                            if 'proxy' in url_obj:
                                existing_url.proxy = url_obj['proxy']
                            existing_url.save()

                    # Bulk create new URLs
                    if new_urls_data:
                        url_serializer = competitor_selected_url_serializer(data=new_urls_data, many=True)
                        if url_serializer.is_valid():
                            url_serializer.save()
                        else:
                            # If URL creation fails, continue without URLs
                            print("Error adding URLs:", url_serializer.errors)

                    # Delete URLs not in the new list
                    if urls_to_delete:
                        competitor_selected_url.objects.filter(
                            competitor_id__slug_id=competitor_obj.slug_id,
                            competitor_domain_mapping_id__slug_id=domain_mapping_obj.slug_id,
                            selected_url__in=urls_to_delete
                        ).delete()

                serialized_competitor = competitor_serializer(competitor_obj)
                return JsonResponse({
                    "message": "Competitor and domain mapping updated successfully.",
                    "data": {
                        "competitor": serialized_competitor.data,
                        "domain_mapping_data": domain_mapping_serialized.data
                    },
                    "success": True,
                }, status=200)
            else:
                return JsonResponse({
                    "error": "Invalid domain mapping data.",
                    "errors": domain_mapping_serialized.errors,
                    "success": False
                }, status=400)
        else:
            return JsonResponse({
                "error": "Domain mapping not found.",
                "success": False
            }, status=404)

    except Exception as e:
        print("Error in update_competitor:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)

@api_view(['DELETE'])
def delete_competitor(request, competitor_slug_id):
    try:    
        obj = competitor.objects.get(slug_id=competitor_slug_id)
        if obj:
            competitor_domain_mapping.objects.select_related('competitor_id').filter(competitor_id=obj).delete()
            obj.delete()
        else:
            return JsonResponse({
                "error": "Competitor not found.",
                "success": False
            }, status=404)

        return JsonResponse({
            "message": "Data deleted successfully.",
            "success": True,
        }, status=200)
    except Exception as e:
        print("Error in delete_competitor:", e)
        return JsonResponse({"error": f"{str(e)}", "success": False}, status=500)
    

@api_view(['POST'])
def send_article_url_to_create_article_api(request):
    try:
        competitor_domain_mapping_slug_id = request.data.get('competitor_domain_mapping_slug_id')
        print(competitor_domain_mapping_slug_id,'competitor_domain_mapping_slug_id')
        if not competitor_domain_mapping_slug_id:
            return JsonResponse({"error": "Missing competitor_domain_mapping_slug_id", "success": False}, status=400)

        # Fetch domain mapping object
        try:
            competitor_domain_mapping_obj = competitor_domain_mapping.objects.get(slug_id=competitor_domain_mapping_slug_id)
        except competitor_domain_mapping.DoesNotExist:
            return JsonResponse({"error": "Invalid competitor_domain_mapping_id", "success": False}, status=404)

        # Fetch all unsent article URLs efficiently (just what's needed)
        unsent_urls = competitor_article_url.objects.filter(
            competitor_domain_mapping_id__slug_id=competitor_domain_mapping_slug_id
        ).exclude(delivery_status='sent').values_list('article_url', flat=True)

        success_count = 0
        fail_count = 0
        failed_urls = []

        for url in unsent_urls:
            result = send_article_url_to_create_article(competitor_domain_mapping_obj, url)
            if result:
                success_count += 1
            else:
                fail_count += 1
                failed_urls.append(url)

        if success_count > 0:
            return JsonResponse({
                "success": True,
                "total": len(unsent_urls),
                "message": "Article url sent to create article successfully.",
                "processed": success_count,
                "failed": fail_count,
                "failed_urls": failed_urls[:20]  # show max 20 failed for readability
            })
        else:
            return JsonResponse({
                "success": False,
                "error": "Article url not sent to create article.",
            })

    except Exception as e:
        print("This error is send_article_url_to_create_article_api --->:", e)
        return JsonResponse({"error": str(e), "success": False}, status=500)
