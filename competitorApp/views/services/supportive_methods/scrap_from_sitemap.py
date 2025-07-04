import requests
import xml.etree.ElementTree as ET
from typing import List, Dict



def process_sitemap_url(sitemap_url: str, proxy: str = None) -> List[str]:
    """
    Process a single sitemap URL and extract all article URLs from it.
    
    Args:
        sitemap_url: URL of the sitemap to process
        proxy: Optional proxy string (e.g., http://user:pass@ip:port)
        
    Returns:
        List of article URLs found in the sitemap
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SitemapBot/1.0; +http://example.com/bot)'
        }
        
        proxies = {}
        if proxy:
            proxies = {'http': proxy, 'https': proxy}
        
        print(f"Processing sitemap: {sitemap_url}")
        
        # Fetch sitemap XML
        response = requests.get(sitemap_url, headers=headers, proxies=proxies, timeout=30)
        response.raise_for_status()
        
        # Parse XML to get article URLs
        root = ET.fromstring(response.text)
        article_urls = []
        
        # Define namespace
        namespaces = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Find all <url> elements first, then get <loc> from each
        url_elements = root.findall('.//sm:url', namespaces)
        if not url_elements:
            # Try without namespace
            url_elements = root.findall('.//url')
        
        for url_element in url_elements:
            # Get the <loc> tag from each <url> element
            loc = url_element.find('sm:loc', namespaces)
            if loc is None:
                loc = url_element.find('loc')
            
            if loc is not None and loc.text:
                clean_url = loc.text.strip()
                if clean_url and clean_url.startswith(('http://', 'https://')):
                    article_urls.append(clean_url)
        
        # If no <url> elements found, try direct <loc> search (fallback)
        if not article_urls:
            loc_elements = root.findall('.//sm:loc', namespaces)
            if not loc_elements:
                loc_elements = root.findall('.//loc')
            
            for loc in loc_elements:
                if loc.text:
                    clean_url = loc.text.strip()
                    if clean_url and clean_url.startswith(('http://', 'https://')):
                        article_urls.append(clean_url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in article_urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        print(f"Found {len(unique_urls)} article URLs in sitemap: {sitemap_url}")
        return unique_urls
        
    except Exception as e:
        print(f"Error processing sitemap {sitemap_url}: {e}")
        return []




def process_sitemap_url_with_metadata(sitemap_url: str, proxy: str = None) -> List[Dict[str, str]]:
    """
    Process a single sitemap URL and extract article URLs with metadata.
    
    Args:
        sitemap_url: URL of the sitemap to process
        proxy: Optional proxy string
        
    Returns:
        List of dictionaries containing article URL and metadata
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SitemapBot/1.0; +http://example.com/bot)'
        }
        
        proxies = {}
        if proxy:
            proxies = {'http': proxy, 'https': proxy}
        
        print(f"Processing sitemap with metadata: {sitemap_url}")
        
        # Fetch sitemap XML
        response = requests.get(sitemap_url, headers=headers, proxies=proxies, timeout=30)
        response.raise_for_status()
        
        # Parse XML to get article URLs with metadata
        root = ET.fromstring(response.text)
        articles = []
        
        # Define namespace
        namespaces = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Find all <url> elements
        url_elements = root.findall('.//sm:url', namespaces)
        if not url_elements:
            url_elements = root.findall('.//url')
        
        for url_element in url_elements:
            article_data = {}
            
            # Get the <loc> tag
            loc = url_element.find('sm:loc', namespaces)
            if loc is None:
                loc = url_element.find('loc')
            
            if loc is not None and loc.text:
                clean_url = loc.text.strip()
                if clean_url and clean_url.startswith(('http://', 'https://')):
                    article_data['url'] = clean_url
                    
                    # Get last modified date
                    lastmod = url_element.find('sm:lastmod', namespaces)
                    if lastmod is None:
                        lastmod = url_element.find('lastmod')
                    if lastmod is not None and lastmod.text:
                        article_data['last_modified'] = lastmod.text.strip()
                    
                    # Get priority
                    priority = url_element.find('sm:priority', namespaces)
                    if priority is None:
                        priority = url_element.find('priority')
                    if priority is not None and priority.text:
                        article_data['priority'] = priority.text.strip()
                    
                    # Get change frequency
                    changefreq = url_element.find('sm:changefreq', namespaces)
                    if changefreq is None:
                        changefreq = url_element.find('changefreq')
                    if changefreq is not None and changefreq.text:
                        article_data['change_frequency'] = changefreq.text.strip()
                    
                    articles.append(article_data)
        
        print(f"Found {len(articles)} articles with metadata in sitemap: {sitemap_url}")
        return articles
        
    except Exception as e:
        print(f"Error processing sitemap with metadata {sitemap_url}: {e}")
        return []


 