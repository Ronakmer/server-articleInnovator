from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from competitorApp.serializers import competitor_serializer, competitor_domain_mapping_serializer
from competitorApp.models import competitor, competitor_domain_mapping, competitor_selected_url, category_url_selector
from django.db.models import Q
import json
import requests
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
from typing import List, Dict, Union
import re
from competitorApp.views.services.supportive_methods.scrap_from_category import (

    scrape_all_articles_with_pagination
)
from competitorApp.views.services.supportive_methods.scrap_from_sitemap import (
    process_sitemap_url
)


@api_view(['GET'])
def scrap_articles(request):
    try:
        # Get competitor_domain_mapping id from request
        domain_mapping_id = request.GET.get('competitor_domain_mapping_slug_id')
        max_pages = int(request.GET.get('max_pages', 10))

        if not domain_mapping_id:
            return JsonResponse({"error": "competitor_domain_mapping_slug_id is required"}, status=400)
        
        # Find the competitor_domain_mapping record from database
        try:
            domain_mapping_record = competitor_domain_mapping.objects.get(slug_id=domain_mapping_id)
        except competitor_domain_mapping.DoesNotExist:
            return JsonResponse({"error": "competitor_domain_mapping not found"}, status=404)
        
        # Get all selected URLs based on domain mapping record
        selected_urls = competitor_selected_url.objects.filter(
            competitor_domain_mapping_id=domain_mapping_record
        )
        
        if not selected_urls.exists():
            return JsonResponse({"error": "No selected URLs found for this domain mapping"}, status=404)
        
        # Check competitor type
        if domain_mapping_record.competitor_type == 'category':
            # Handle category type competitor
            all_scraped_articles = []
            
            for selected_url_obj in selected_urls:
                # Get category selectors for this URL
                selectors = category_url_selector.objects.select_related('competitor_selected_url_id').filter(
                    competitor_selected_url_id=selected_url_obj
                )
                
                article_selector = None
                next_btn_selector = None
                
                # Find article and nxtbtn selectors
                for selector in selectors:
                    if selector.selector_name.lower() == 'article':
                        article_selector = selector.selector
                    elif selector.selector_name.lower() == 'nxtbtn':
                        next_btn_selector = selector.selector
                
                if not article_selector:
                    print(f"No article selector found for URL: {selected_url_obj.selected_url}")
                    continue
                
                # Scrape articles from this category URL
                scraped_articles = scrape_all_articles_with_pagination(
                    selected_url_obj.selected_url,
                    article_selector,
                    next_btn_selector,
                    selected_url_obj.proxy,
                    max_pages=max_pages
                )
                
                # Prepare article data for response (don't save to database)
                articles_from_url = []
                for article_url in scraped_articles:
                    articles_from_url.append({
                        'url': article_url,
                        'source_category_url': selected_url_obj.selected_url,
                        'competitor_selected_url_slug_id': selected_url_obj.slug_id,
                        'found_at': selected_url_obj.created_date.isoformat() if selected_url_obj.created_date else None
                    })
                
                all_scraped_articles.extend(articles_from_url)
            
            response_data = {
                'domain_mapping_id': domain_mapping_id,
                'competitor_type': domain_mapping_record.competitor_type,
                'total_articles_found': len(all_scraped_articles),
                'found_articles': all_scraped_articles,
                'selected_urls_processed': selected_urls.count(),
                'pagination': {
                        'total_count': len(all_scraped_articles)
                    },
                'success': True,
                'message': 'Articles found successfully'
            }
            
        else:
            # Handle sitemap type - process sitemap URLs to extract article URLs
            all_sitemap_articles = []
            
            for selected_url_obj in selected_urls:
                # selected_url should be a sitemap URL
                sitemap_url = selected_url_obj.selected_url
                
                # Process the sitemap to extract only article URLs
                article_urls = process_sitemap_url(sitemap_url, selected_url_obj.proxy)
                
                # Prepare article data for response (don't save to database)
                for article_url in article_urls:
                    all_sitemap_articles.append({
                        'url': article_url,
                        'source_sitemap_url': sitemap_url,
                        'competitor_selected_url_slug_id': selected_url_obj.slug_id,
                        'found_at': selected_url_obj.created_date.isoformat() if selected_url_obj.created_date else None
                    })
            
            response_data = {
                'domain_mapping_id': domain_mapping_id,
                'competitor_type': domain_mapping_record.competitor_type,
                'total_articles_found': len(all_sitemap_articles),
                'found_articles': all_sitemap_articles,
                'selected_urls_processed': selected_urls.count(),
                'pagination': {
                        'total_count': len(all_sitemap_articles)
                    },
                'success': True,
                'message': 'Articles extracted from sitemaps successfully'
            }
        
        return JsonResponse(response_data, status=200)
        
    except Exception as e:
        print(f"Error in scrap_articles: {e}")
        return JsonResponse({"error": str(e)}, status=500)






