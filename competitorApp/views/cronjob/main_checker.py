import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from lxml import html
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from urllib.parse import urljoin, urlparse
# from loguru import logger  # Removing this to fix logging issues

from apiApp.views.article.supportive_methods.add_ai_article import add_ai_article
from competitorApp.models import (
    competitor_selected_url, 
    competitor_article_url, 
    competitor_url_daily_stats,
    category_url_selector
)

# Simple logging function to replace logger
def log_info(message):
    print(f"[INFO] {timezone.now()}: {message}")

def log_error(message):
    print(f"[ERROR] {timezone.now()}: {message}")

# ============== SELECTOR HELPER FUNCTIONS ==============

def is_xpath_selector(selector: str) -> bool:
    """
    Check if a selector is XPath or CSS
    
    Args:
        selector: The selector string to check
        
    Returns:
        True if it's XPath, False if it's CSS
    """
    if not selector:
        return False
    
    # Common XPath indicators
    xpath_indicators = [
        selector.startswith('//'),
        selector.startswith('/'),
        '@' in selector,
        'text()' in selector,
        'contains(' in selector,
        'position()' in selector,
        'last()' in selector,
        'preceding-sibling' in selector,
        'following-sibling' in selector
    ]
    
    return any(xpath_indicators)


def find_elements_with_selector(tree_or_soup, selector: str, single=False):
    """
    Find elements using either XPath or CSS selector
    
    Args:
        tree_or_soup: lxml tree or BeautifulSoup object
        selector: XPath or CSS selector
        single: If True, return only first element
        
    Returns:
        List of elements or single element
    """
    if is_xpath_selector(selector):
        # Use lxml for XPath
        if hasattr(tree_or_soup, 'xpath'):
            elements = tree_or_soup.xpath(selector)
            return elements[0] if single and elements else elements
        else:
            return [] if not single else None
    else:
        # Use BeautifulSoup for CSS selectors
        if hasattr(tree_or_soup, 'select'):
            if single:
                return tree_or_soup.select_one(selector)
            else:
                return tree_or_soup.select(selector)
        else:
            return [] if not single else None

# ============== SIMPLE HELPER FUNCTIONS ==============

def get_next_check_time(url_obj):
    """Calculate when to check this URL next"""
    # Refresh the object to get latest interval settings
    url_obj.refresh_from_db()
    
    mapping = url_obj.competitor_domain_mapping_id
    if not mapping:
        return timezone.now() + timedelta(minutes=30)
    
    # Refresh mapping to get latest interval settings
    mapping.refresh_from_db()
    
    if mapping.interval_unit == 'minute':
        return timezone.now() + timedelta(minutes=mapping.interval)
    elif mapping.interval_unit == 'hour':
        return timezone.now() + timedelta(hours=mapping.interval)
    elif mapping.interval_unit == 'day':
        return timezone.now() + timedelta(days=mapping.interval)
    else:
        return timezone.now() + timedelta(minutes=30)


def update_daily_stats(url_obj, success=True, articles_found=0, new_articles=0):
    """Update daily statistics - one entry per day"""
    today = timezone.now().date()
    
    stats, created = competitor_url_daily_stats.objects.get_or_create(
        competitor_selected_url_id=url_obj,
        stat_date=today,
        defaults={
            'total_runs': 0, 'successful_runs': 0, 'failed_runs': 0,
            'total_articles_found': 0, 'new_articles_added': 0,
            'duplicate_articles_skipped': 0
        }
    )
    
    stats.total_runs += 1
    stats.last_run_at = timezone.now()
    
    if success:
        stats.successful_runs += 1
        stats.total_articles_found += articles_found
        stats.new_articles_added += new_articles
        stats.duplicate_articles_skipped += (articles_found - new_articles)
    else:
        stats.failed_runs += 1
    
    stats.save()

# ============== Send Article Url To Create Article ==============
def send_article_url_to_create_article(competitor_domain_mapping_obj,article_url):
    try:
        data = {
                "article_type_slug_id": competitor_domain_mapping_obj.article_type['article_type_slug_id'],
                "domain_slug_id": competitor_domain_mapping_obj.domain_slug_id,
                "workspace_slug_id": competitor_domain_mapping_obj.workspace_slug_id,
                "wp_status": competitor_domain_mapping_obj.wp_status,
                "prompt_slug_id": competitor_domain_mapping_obj.prompt['prompt_slug_id'],
                "article_priority": competitor_domain_mapping_obj.article_priority,
                "article_status": competitor_domain_mapping_obj.article_status,
                "wp_schedule_time": competitor_domain_mapping_obj.wp_schedule_time,
                "url": article_url,
                "keyword":None ,
                "wp_author": competitor_domain_mapping_obj.wp_author,
                "wp_category": competitor_domain_mapping_obj.wp_category['category_slug_id_ai'],
                "wp_tag": competitor_domain_mapping_obj.wp_tag['tag_slug_id_ai'],
                "ai_content_flags": competitor_domain_mapping_obj.ai_content_flags    
        }
        add_ai_article(data)

        return True
    except Exception as e:
        log_error(f"Error sending article url to create article: {e}")
        return False


# ============== SITEMAP PROCESSING ==============

def process_sitemap(url_obj):
    """Process sitemap URL - extract article URLs and save new ones"""
    sitemap_url = url_obj.selected_url
    log_info(f"Processing sitemap: {sitemap_url}")
    
    try:
        # 1. Fetch sitemap XML
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; SitemapBot/1.0)'}
        response = requests.get(sitemap_url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        
        # 2. Parse XML to get article URLs
        root = ET.fromstring(response.text)
        article_urls = []
        
        # Find all <loc> tags (these contain article URLs)
        for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            if loc.text:
                article_urls.append(loc.text.strip())
        
        # Also try without namespace (some sitemaps don't use it)
        for loc in root.findall('.//loc'):
            if loc.text:
                article_urls.append(loc.text.strip())
        
        # Remove duplicates
        article_urls = list(set(article_urls))
        
        log_info(f"Found {len(article_urls)} article URLs in sitemap")
        
        # 3. Save new article URLs
        new_count = 0
        for article_url in article_urls:
            # Check if already exists
            exists = competitor_article_url.objects.filter(
                article_url=article_url,
                competitor_domain_mapping_id=url_obj.competitor_domain_mapping_id
            ).exists()
            
            if not exists:
                response = send_article_url_to_create_article(url_obj.competitor_domain_mapping_id,article_url)
                # Save new article URL
                competitor_article_url.objects.create(
                    article_url=article_url,
                    competitor_selected_url_id=url_obj,
                    competitor_domain_mapping_id=url_obj.competitor_domain_mapping_id,
                    delivery_status='sent'
                )
                
                new_count += 1
        
        duplicate_count = len(article_urls) - new_count
        message = f"Sitemap: {len(article_urls)} found, {new_count} new, {duplicate_count} duplicates"
        
        log_info(message)
        return True, len(article_urls), new_count, message
        
    except Exception as e:
        error_msg = f"Sitemap error: {str(e)}"
        log_error(error_msg)
        return False, 0, 0, error_msg



# ============== CATEGORY PROCESSING ==============

def process_category(url_obj):
    """Process category URL - use selectors to find article URLs"""
    category_url = url_obj.selected_url
    log_info(f"Processing category: {category_url}")
    
    try:
        # 1. Get selectors from database
        selectors = category_url_selector.objects.filter(
            competitor_selected_url_id=url_obj
        )
        
        article_selector = None
        next_btn_selector = None
        
        for sel in selectors:
            if sel.selector_name.lower() == 'article':
                article_selector = sel.selector
            elif 'next' in sel.selector_name.lower():
                next_btn_selector = sel.selector
        
        if not article_selector:
            return False, 0, 0, "No article selector found"
        
        # 2. Fetch webpage
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(category_url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        
        # 3. Parse HTML with both parsers for CSS/XPath support
        soup = BeautifulSoup(response.text, 'html.parser')
        tree = html.fromstring(response.text)
        
        # 4. Find article links using appropriate parser based on selector type
        article_urls = []
        
        if is_xpath_selector(article_selector):
            log_info(f"Using XPath selector: {article_selector}")
            article_elements = find_elements_with_selector(tree, article_selector)
            
            for element in article_elements:
                # Find link in element
                link = None
                if element.tag == 'a' and element.get('href'):
                    link = element.get('href')
                else:
                    # Look for 'a' elements within this element
                    sub_links = element.xpath('.//a[@href]')
                    if sub_links:
                        link = sub_links[0].get('href')
                
                if link:
                    # Convert to absolute URL
                    absolute_url = urljoin(category_url, link)
                    if absolute_url.startswith(('http://', 'https://')):
                        article_urls.append(absolute_url)
        else:
            log_info(f"Using CSS selector: {article_selector}")
            article_elements = find_elements_with_selector(soup, article_selector)
            
            for element in article_elements:
                # Find link in element
                link = None
                if element.name == 'a':
                    link = element.get('href')
                else:
                    a_tag = element.find('a')
                    if a_tag:
                        link = a_tag.get('href')
                
                if link:
                    # Convert to absolute URL
                    absolute_url = urljoin(category_url, link)
                    if absolute_url.startswith(('http://', 'https://')):
                        article_urls.append(absolute_url)
        
        # Remove duplicates
        article_urls = list(set(article_urls))
        
        log_info(f"Found {len(article_urls)} article URLs on category page")
        
        # 4. Save new article URLs  
        new_count = 0
        for article_url in article_urls:
            # Check if already exists
            exists = competitor_article_url.objects.filter(
                article_url=article_url,
                competitor_domain_mapping_id=url_obj.competitor_domain_mapping_id
            ).exists()
            
            if not exists:
                response = send_article_url_to_create_article(url_obj.competitor_domain_mapping_id,article_url)
                # Save new article URL
                competitor_article_url.objects.create(
                    article_url=article_url,
                    competitor_selected_url_id=url_obj,
                    competitor_domain_mapping_id=url_obj.competitor_domain_mapping_id,
                    delivery_status='sent'
                )
               
                new_count += 1
        
        duplicate_count = len(article_urls) - new_count
        message = f"Category: {len(article_urls)} found, {new_count} new, {duplicate_count} duplicates"
        
        log_info(message)
        return True, len(article_urls), new_count, message
        
    except Exception as e:
        error_msg = f"Category error: {str(e)}"
        log_error(error_msg)
        return False, 0, 0, error_msg




# ============== MAIN CHECKER FUNCTION ==============

def check_single_url(url_id):
    """Main function to check a single URL"""
    try:
        # Get URL object
        url_obj = competitor_selected_url.objects.get(id=url_id)
        
        # Skip if monitoring disabled
        if not url_obj.monitor_enabled:
            
            return
        
        # Get competitor type
        competitor_type = 'sitemap'  # default
        if url_obj.competitor_domain_mapping_id:
            competitor_type = url_obj.competitor_domain_mapping_id.competitor_type
        
        log_info(f"Checking {competitor_type} URL: {url_obj.selected_url}")
        
        # Process based on type
        if competitor_type == 'sitemap':
            success, articles_found, new_articles, message = process_sitemap(url_obj)
        elif competitor_type == 'category':
            success, articles_found, new_articles, message = process_category(url_obj)
        else:
            success, articles_found, new_articles, message = False, 0, 0, f"Unknown type: {competitor_type}"
        
        # Update URL record
        with transaction.atomic():
            url_obj.last_api_call_at = timezone.now()
            url_obj.next_api_call_at = get_next_check_time(url_obj)
            url_obj.scrap_status = 'completed' if success else 'failed'
            url_obj.save()
            
            # Update daily stats
            update_daily_stats(url_obj, success, articles_found, new_articles)
        
        log_info(f" Completed: {message}")
        return success, message
        
    except competitor_selected_url.DoesNotExist:
        log_error(f"URL ID {url_id} not found")
        return False, "URL not found"
    except Exception as e:
        log_error(f"Error checking URL ID {url_id}: {e}")
        return False, str(e)


# ============== BATCH PROCESSING ==============

def get_due_urls(limit=50000):
    """Get URLs that need to be checked now"""
    now = timezone.now()
    return competitor_selected_url.objects.filter(
        next_api_call_at__lte=now,
        monitor_enabled=True
    ).order_by('next_api_call_at')[:limit]


