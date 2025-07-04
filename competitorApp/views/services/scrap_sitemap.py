from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from competitorApp.serializers import competitor_serializer, competitor_domain_mapping_serializer
from competitorApp.models import competitor, competitor_article_url, competitor_domain_mapping, competitor_selected_url
from django.db.models import Q
from loguru import logger
import json
import requests
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
from typing import List, Dict, Union
import re

def is_valid_url(url: str) -> bool:
    """Check if a URL is valid."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def normalize_url(url: str, base_url: str) -> str:
    """Normalize a URL by joining it with the base URL if necessary."""
    if not url.startswith(('http://', 'https://')):
        return urljoin(base_url, url)
    return url

def extract_sitemap_urls(xml_content: str) -> List[str]:
    """Extract sitemap URLs from XML content."""
    try:
        root = ET.fromstring(xml_content)
        urls = []
        namespaces = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Try with namespace first
        sitemap_locs = root.findall('.//sm:loc', namespaces)
        if not sitemap_locs:
            # Try without namespace
            sitemap_locs = root.findall('.//loc')
        
        for loc in sitemap_locs:
            if loc.text:
                urls.append(loc.text.strip())
        
        return urls
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return []

def get_sitemap_urls(domain: str) -> Dict[str, Union[List[str], List[Dict[str, str]]]]:
    """
    Get sitemap URLs from a domain.
    
    Args:
        domain (str): Domain name (e.g., 'example.com' or 'https://example.com')
    
    Returns:
        Dict containing:
            - sitemap_urls: List of found sitemap URLs
            - errors: List of any errors encountered
    """
    # Ensure domain has a protocol
    if not domain.startswith(('http://', 'https://')):
        domain = f'https://{domain}'
    
    sitemap_urls = set()
    errors = []
    
    # Common sitemap paths to check
    sitemap_paths = [
        '/sitemap.xml',
        '/sitemap_index.xml',
        '/sitemap/',
        '/sitemaps.xml',
        '/sitemap/sitemap.xml',
        '/sitemap1.xml',
        '/post-sitemap.xml'
    ]
    
    # Try robots.txt first
    try:
        robots_url = urljoin(domain, '/robots.txt')
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                if 'sitemap:' in line.lower():
                    sitemap_url = line.split(':', 1)[1].strip()
                    sitemap_urls.add(sitemap_url)
    except Exception as e:
        errors.append({
            'source': 'robots.txt',
            'error': str(e)
        })

    # Check common sitemap locations
    for path in sitemap_paths:
        try:
            url = urljoin(domain, path)
            response = requests.get(url, timeout=10)
            if response.status_code == 200 and 'xml' in response.headers.get('content-type', ''):
                # Try to parse XML and extract URLs
                found_urls = extract_sitemap_urls(response.text)
                sitemap_urls.update(found_urls)
                # If no nested sitemaps found, add the current URL
                if not found_urls:
                    sitemap_urls.add(url)
        except Exception as e:
            errors.append({
                'source': path,
                'error': str(e)
            })

    return {
        'sitemap_urls': list(sitemap_urls),
        'errors': errors
    }

@api_view(['GET'])
# @csrf_exempt
def scrap_sitemap(request) -> JsonResponse:
    """
    API endpoint to get sitemap URLs for a given domain via query param.

    Example:
    GET /api/sitemap?competitor_domain_name=example.com

    Returns:
    {
        "success": bool,
        "message": str,
        "data": {
            "domain": str,
            "sitemap_urls": List[str],
        },
        "pagination": {
            "total_count": int
        }
    }
    """
    try:
        domain = request.GET.get('competitor_domain_name', '').strip()
        
        if not domain:
            return JsonResponse({
                'success': False,
                'message': 'Domain is required as a query parameter',
                'data': None,
                'pagination': {
                    'total_count': 0
                }
            }, status=400)

        result = get_sitemap_urls(domain)
        sitemap_list = result['sitemap_urls']
        total_count = len(sitemap_list)
        
        return JsonResponse({
            'success': True,
            'message': 'Sitemap URLs found successfully' if sitemap_list else 'No sitemap URLs found',
            'data': {
                'domain': domain,
                'sitemap_urls': sitemap_list,
            },
            'pagination': {
                'total_count': total_count
            }
        })

    except Exception as e:
        print(f"Unexpected error in scrap_sitemap: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Internal server error: {str(e)}',
            'data': None,
            'pagination': {
                'total_count': 0
            }
        }, status=500)



