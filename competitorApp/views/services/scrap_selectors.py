import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from competitorApp.serializers import competitor_serializer, competitor_domain_mapping_serializer
from competitorApp.models import (
    competitor, competitor_domain_mapping, competitor_selected_url, 
    category_url_selector, article_url_selector, competitor_article_url
)
from django.db.models import Q
from loguru import logger
import json
import requests
from typing import List, Dict, Union, Optional
import re
from urllib.parse import urlparse
from .supportive_methods.ai_provider import AIProvider


def get_domain_from_url(url: str) -> str:
    """Extract domain from URL"""
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc.lower()
    except Exception as e:
        print(f"Error extracting domain from URL {url}: {str(e)}")
        return ""


def scrape_html_content(url: str, timeout: int = 30) -> str:
    """
    Scrape HTML content from URL
    
    Args:
        url: The URL to scrape
        timeout: Request timeout in seconds
        
    Returns:
        HTML content as string
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        print(f"Successfully scraped HTML from {url}")
        return response.text
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping HTML from {url}: {str(e)}")
        raise Exception(f"Failed to scrape HTML: {str(e)}")


def extract_and_save_selectors(
    article_url: str,
    force_refresh: bool = False,
    competitor_article_url_slug_id: uuid.UUID = None,
    verified_by: str = ""
) -> Dict:
    """
    Extract selectors from article URL using AI and save to database
    
    Args:
        article_url: The article URL to analyze
        force_refresh: Whether to force refresh existing selectors
        verified_by: User who verified the selectors
        
    Returns:
        Dictionary containing selectors and metadata
    """
    try:
        domain = get_domain_from_url(article_url)
        
        # Find existing selectors by searching for the article URL in related tables
        existing_selector = None
        competitor_article_url_record = None
        competitor_selected_url_record = None
        
        # Search in competitor_article_url table first
        if competitor_article_url_slug_id:
            competitor_article_url_record = competitor_article_url.objects.filter(
                slug_id=competitor_article_url_slug_id
            ).first()
        else:
            competitor_article_url_record = competitor_article_url.objects.filter(
                article_url=article_url
            ).first()
        
        if competitor_article_url_record:
            existing_selector = article_url_selector.objects.filter(
                competitor_article_url_id=competitor_article_url_record
            ).first()
        
        # If not found, search in competitor_selected_url table
        if not existing_selector:
            competitor_selected_url_record = competitor_selected_url.objects.filter(
                selected_url=article_url
            ).first()
            
            if competitor_selected_url_record:
                existing_selector = article_url_selector.objects.filter(
                    competitor_selected_url_id=competitor_selected_url_record
                ).first()
        
        # If no existing record found, return error
        if not competitor_article_url_record and not competitor_selected_url_record:
            return {
                'success': False,
                'error': f'Article URL "{article_url}" not found in existing records. Please add this URL first.',
                'domain': domain,
                'article_url': article_url
            }
        
        # Return cached selectors if available and not forced refresh
        if existing_selector and not force_refresh:
            print(f"Using cached selectors for URL: {article_url}")
            return {
                'success': True,
                'domain': domain,
                'article_url': article_url,
                'selectors': {
                    'source_title': existing_selector.source_title,
                    'source_content': existing_selector.source_content,
                    'source_categories': existing_selector.source_categories,
                    'source_tags': existing_selector.source_tags,
                    'source_author': existing_selector.source_author,
                    'source_published_date': existing_selector.source_published_date,
                    'source_featured_image': existing_selector.source_featured_image,
                    'source_meta_title': existing_selector.source_meta_title,
                    'source_meta_description': existing_selector.source_meta_description,
                    'source_meta_keywords': existing_selector.source_meta_keywords,
                    'source_outline': existing_selector.source_outline,
                    'source_internal_links': existing_selector.source_internal_links,
                    'source_external_links': existing_selector.source_external_links,
                    'source_faqs': existing_selector.source_faqs,
                },
                'from_cache': True,
                'is_verified': existing_selector.is_verified
            }
        
        # Scrape HTML content
        print(f"Scraping HTML content from: {article_url}")
        html_content = scrape_html_content(article_url)
        
        if not html_content:
            raise Exception("Failed to retrieve HTML content")
        
        # Extract selectors using AI
        print(f"Extracting selectors using AI for domain: {domain}")
        ai_provider = AIProvider()
        selectors = ai_provider.extract_selectors(html_content, domain)
        
        if isinstance(selectors, str):
            selectors = json.loads(selectors)
        
        # Update or create selector config based on existing records
        if existing_selector:
            # Update existing
            existing_selector.source_title = selectors.get('source_title', {})
            existing_selector.source_content = selectors.get('source_content', {})
            existing_selector.source_categories = selectors.get('source_categories', {})
            existing_selector.source_tags = selectors.get('source_tags', {})
            existing_selector.source_author = selectors.get('source_author', {})
            existing_selector.source_published_date = selectors.get('source_published_date', {})
            existing_selector.source_featured_image = selectors.get('source_featured_image', {})
            existing_selector.source_meta_title = selectors.get('source_meta_title', {})
            existing_selector.source_meta_description = selectors.get('source_meta_description', {})
            existing_selector.source_meta_keywords = selectors.get('source_meta_keywords', {})
            existing_selector.source_outline = selectors.get('source_outline', [])
            existing_selector.source_internal_links = selectors.get('source_internal_links', [])
            existing_selector.source_external_links = selectors.get('source_external_links', [])
            existing_selector.source_faqs = selectors.get('source_faqs', [])
            existing_selector.verified_by = verified_by
            existing_selector.save()
            
            print(f"Updated existing selectors for URL: {article_url}")
            selector_instance = existing_selector
            
        else:
            # Create new selector record for existing article URL
            selector_instance = article_url_selector.objects.create(
                competitor_article_url_id=competitor_article_url_record,
                competitor_selected_url_id=competitor_article_url_record.competitor_selected_url_id,
                source_title=selectors.get('source_title', {}),
                source_content=selectors.get('source_content', {}),
                source_categories=selectors.get('source_categories', {}),
                source_tags=selectors.get('source_tags', {}),
                source_author=selectors.get('source_author', {}),
                source_published_date=selectors.get('source_published_date', {}),
                source_featured_image=selectors.get('source_featured_image', {}),
                source_meta_title=selectors.get('source_meta_title', {}),
                source_meta_description=selectors.get('source_meta_description', {}),
                source_meta_keywords=selectors.get('source_meta_keywords', {}),
                source_outline=selectors.get('source_outline', []),
                source_internal_links=selectors.get('source_internal_links', []),
                source_external_links=selectors.get('source_external_links', []),
                source_faqs=selectors.get('source_faqs', []),
                verified_by=verified_by
            )
            
            print(f"Created new selector record for existing URL: {article_url}")
        
        return {
            'success': True,
            'domain': domain,
            'article_url': article_url,
            'selectors': {
                'source_title': selector_instance.source_title,
                'source_content': selector_instance.source_content,
                'source_categories': selector_instance.source_categories,
                'source_tags': selector_instance.source_tags,
                'source_author': selector_instance.source_author,
                'source_published_date': selector_instance.source_published_date,
                'source_featured_image': selector_instance.source_featured_image,
                'source_meta_title': selector_instance.source_meta_title,
                'source_meta_description': selector_instance.source_meta_description,
                'source_meta_keywords': selector_instance.source_meta_keywords,
                'source_outline': selector_instance.source_outline,
                'source_internal_links': selector_instance.source_internal_links,
                'source_external_links': selector_instance.source_external_links,
                'source_faqs': selector_instance.source_faqs,
            },
            'from_cache': False,
            'is_verified': selector_instance.is_verified,
            'selector_id': selector_instance.id
        }
        
    except Exception as e:
        print(f"Error extracting selectors for URL {article_url}: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'domain': get_domain_from_url(article_url) if article_url else "",
            'article_url': article_url
        }


def get_selectors_by_id(selector_id: int) -> Dict:
    """
    Get selectors by article_url_selector ID
    
    Args:
        selector_id: The article_url_selector ID
        
    Returns:
        Dictionary containing selectors and metadata
    """
    try:
        selector_instance = article_url_selector.objects.get(id=selector_id)
        
        return {
            'success': True,
            'selector_id': selector_instance.id,
            'selectors': {
                'source_title': selector_instance.source_title,
                'source_content': selector_instance.source_content,
                'source_categories': selector_instance.source_categories,
                'source_tags': selector_instance.source_tags,
                'source_author': selector_instance.source_author,
                'source_published_date': selector_instance.source_published_date,
                'source_featured_image': selector_instance.source_featured_image,
                'source_meta_title': selector_instance.source_meta_title,
                'source_meta_description': selector_instance.source_meta_description,
                'source_meta_keywords': selector_instance.source_meta_keywords,
                'source_outline': selector_instance.source_outline,
                'source_internal_links': selector_instance.source_internal_links,
                'source_external_links': selector_instance.source_external_links,
                'source_faqs': selector_instance.source_faqs,
            },
            'is_verified': selector_instance.is_verified,
            'verified_by': selector_instance.verified_by,
            'created_date': selector_instance.created_date,
            'updated_date': selector_instance.updated_date
        }
        
    except article_url_selector.DoesNotExist:
        return {
            'success': False,
            'error': f'Selector with ID {selector_id} not found'
        }
    except Exception as e:
        print(f"Error getting selectors by ID {selector_id}: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@csrf_exempt
@api_view(['POST'])
def extract_article_selectors_api(request):
    """
    API endpoint to extract selectors from article URL
    
    Expected JSON payload:
    {
        "article_url": "https://example.com/article"
    }
    
    Returns:
    {
        "success": true/false,
        "data": {...} or "error": "error message"
    }
    """
    try:
        # Parse request data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        # Validate required fields
        article_url = data.get('article_url')
        if not article_url:
            return JsonResponse({
                'success': False,
                'error': 'article_url is required'
            }, status=400)
        
        # Validate URL format
        if not article_url.startswith(('http://', 'https://')):
            return JsonResponse({
                'success': False,
                'error': 'Invalid URL format. URL must start with http:// or https://'
            }, status=400)
        
        # Extract optional parameters
        force_refresh = data.get('force_refresh', False)
        verified_by = data.get('verified_by', '')
        
        print(f"Processing selector extraction request for URL: {article_url}")
        
        # Call the simplified extraction function
        result = extract_and_save_selectors(
            article_url=article_url,
            force_refresh=force_refresh,
            verified_by=verified_by
        )
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'data': result
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'error': result.get('error', 'Unknown error occurred')
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        print(f"Error in extract_article_selectors_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }, status=500)

