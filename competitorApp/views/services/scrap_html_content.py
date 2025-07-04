from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from competitorApp.serializers import competitor_serializer, competitor_domain_mapping_serializer
from competitorApp.models import competitor, competitor_article_url, competitor_domain_mapping
from django.db.models import Q
from loguru import logger
import json
from competitorApp.views.base.process_pagination.process_pagination import process_pagination
from competitorApp.serializers import competitor_selected_url_serializer
from competitorApp.models import competitor_selected_url
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re
from .scrap_selectors import extract_and_save_selectors


def clean_html_content(html_content):
    """
    Clean HTML content by removing all escape characters and formatting properly
    
    Args:
        html_content (str): Raw HTML content
    
    Returns:
        str: Clean, properly formatted HTML content
    """
    if not html_content:
        return html_content
    
    # Remove all types of escape characters and backslashes
    cleaned_html = html_content.replace('\\n', '').replace('\\t', '').replace('\\r', '')
    cleaned_html = cleaned_html.replace('\\"', '"').replace("\\'", "'").replace('\\/', '/')
    cleaned_html = cleaned_html.replace('\\\\', '\\')
    
    # Remove actual tab characters and replace with spaces
    cleaned_html = cleaned_html.replace('\t', ' ')
    
    # Remove excessive whitespace and normalize
    cleaned_html = re.sub(r' +', ' ', cleaned_html)  # Multiple spaces to single space
    
    # Remove newlines between HTML tags to make it more compact
    cleaned_html = re.sub(r'>\s*\n\s*<', '><', cleaned_html)
    
    # Remove excessive newlines
    cleaned_html = re.sub(r'\n\s*\n+', '\n', cleaned_html)
    
    # Parse with BeautifulSoup and prettify for proper formatting
    try:
        soup = BeautifulSoup(cleaned_html, 'html.parser')
        # Get prettified HTML with proper indentation
        cleaned_html = soup.prettify()
        
        # Remove excessive blank lines from prettified output
        lines = cleaned_html.split('\n')
        cleaned_lines = []
        for line in lines:
            # Keep line if it's not just whitespace or if it has content
            if line.strip():
                cleaned_lines.append(line)
        
        cleaned_html = '\n'.join(cleaned_lines)
        
    except Exception as e:
        print(f"Error during BeautifulSoup formatting: {e}")
        # Fallback: just clean up lines manually
        lines = cleaned_html.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        cleaned_html = '\n'.join(cleaned_lines)
    
    return cleaned_html


def scrape_html_from_url(url):
    """
    Use Selenium to scrape HTML content from a given URL with runtime driver installation
    
    Args:
        url (str): The URL to scrape
    
    Returns:
        dict: Dictionary containing scraped content and metadata
    """
    driver = None
    try:
        print(f"Starting to scrape URL with Selenium: {url}")
        
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User agent to mimic real browser
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Use webdriver manager to automatically download and install ChromeDriver
        service = Service(ChromeDriverManager().install())
        # service = Service('/usr/local/bin/chromedriver')  # Path to pre-installed ChromeDriver

        driver = webdriver.Chrome(service=service, options=options)
        
        # Set timeouts
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        # Navigate to the URL
        driver.get(url)
        
        # Wait for the page to be fully loaded
        wait = WebDriverWait(driver, 20)
        
        # Wait for body element to be present
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Wait for document ready state
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        
        # Optional: Wait for jQuery if it exists
        try:
            wait.until(lambda driver: driver.execute_script(
                'return typeof jQuery !== "undefined" ? jQuery.active == 0 : true'
            ))
        except:
            pass  # jQuery might not be present
        
        print(f"Page loaded successfully: {url}")
        
        # Get the page source (HTML content) after JS execution
        html_content = driver.page_source
        
        # Clean the HTML content by removing unwanted newlines and backslashes
        cleaned_html_content = clean_html_content(html_content)
        
        # Parse with BeautifulSoup for metadata extraction
        soup = BeautifulSoup(cleaned_html_content, 'html.parser')
        
        # Get some basic metadata
        title = soup.find('title')
        title_text = title.get_text().strip() if title else 'No title found'
        
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description.get('content', '') if meta_description else ''
        
        # Get text content (clean text without HTML tags)
        text_content = soup.get_text()
        text_content = ' '.join(text_content.split())
        
        print(f"Successfully scraped URL: {url}")
        
        return {
            'success': True,
            'html_content': cleaned_html_content,
            'text_content': text_content,
            'metadata': {
                'title': title_text,
                'description': description,
                'content_length': len(cleaned_html_content),
                'text_length': len(text_content),
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'method': 'selenium',
                'cleaned': True
            }
        }
        
    except Exception as e:
        print(f"Error while scraping with Selenium {url}: {str(e)}")
        return {
            'success': False,
            'error': f'Error during Selenium HTML scraping: {str(e)}'
        }
        
    finally:
        # Always close the driver
        if driver:
            try:
                driver.quit()
                print("Driver closed successfully")
            except:
                pass



@api_view(['GET'])
# @csrf_exempt
def scrap_html_content(request):
    """
    API to scrape HTML content based on competitor_domain_mapping id and type
    
    Takes competitor_domain_mapping id and type:
    - If type is 'category': scrapes from competitor_selected_url table
    - If type is 'article': scrapes from competitor_article_url table
    
    HTML content is automatically cleaned to remove unwanted newlines and backslashes
    
    Returns the scraped HTML content
    """
    try:
        # Get the request data
        # data = json.loads(request.body)
        competitor_domain_mapping_slug_id = request.GET.get('competitor_domain_mapping_slug_id')
        scrape_type = request.GET.get('type')  # Get type parameter from query params
        
        if not competitor_domain_mapping_slug_id:
            return JsonResponse({
                'status': 'error',
                'message': 'competitor_domain_mapping_slug_id is required'
            }, status=400)
            
        if not scrape_type:
            return JsonResponse({
                'status': 'error',
                'message': 'type is required (category or article)'
            }, status=400)
        
        # Get the competitor domain mapping
        try:
            domain_mapping = competitor_domain_mapping.objects.get(
                slug_id=competitor_domain_mapping_slug_id
            )
        except competitor_domain_mapping.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Competitor domain mapping not found'
            }, status=404)
        
        url_to_scrape = None
        url_source = None
        
        # Manual condition based on type parameter (not competitor_type from model)
        if scrape_type == 'category':
            # First check if the competitor_type is actually 'category'
            if domain_mapping.competitor_type != 'category':
                return JsonResponse({
                    'status': 'error',
                    'message': 'This is not a category type competitor domain mapping'
                }, status=400)
            
            # For category type, find URL from competitor_selected_url table
            try:
                selected_url = competitor_selected_url.objects.filter(
                    competitor_domain_mapping_id=domain_mapping
                ).first()
                
                if selected_url:
                    url_to_scrape = selected_url.selected_url
                    url_source = 'competitor_selected_url'
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'No selected URL found in competitor_selected_url table for this mapping'
                    }, status=404)
                    
            except Exception as e:
                print(f"Error finding selected URL for category: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error finding selected URL for category'
                }, status=500)
        
        elif scrape_type == 'article':
            # For article type, find URL from competitor_article_url table
            try:
                article_url = competitor_article_url.objects.filter(
                    competitor_domain_mapping_id=domain_mapping
                ).first()
                
                if article_url:
                    url_to_scrape = article_url.article_url
                    url_source = 'competitor_article_url'
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'No article URL found in competitor_article_url table for this mapping'
                    }, status=404)
                    
            except Exception as e:
                print(f"Error finding article URL: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error finding article URL'
                }, status=500)
        
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'Unsupported type: {scrape_type}. Must be "category" or "article"'
            }, status=400)
        
        if not url_to_scrape:
            return JsonResponse({
                'status': 'error',
                'message': 'No URL found to scrape'
            }, status=404)
        
        # Use the scraping function
        scrape_result = scrape_html_from_url(url_to_scrape)
        
        if scrape_result['success']:
            response_data = {
                'url': url_to_scrape,
                'url_source': url_source,
                'type': scrape_type,
                'competitor_domain_mapping_id': competitor_domain_mapping_slug_id,
                'html_content': scrape_result['html_content'],
            }
            
            # Add slug IDs based on scrape type
            if scrape_type == 'article' and article_url:
                response_data['competitor_article_url_slug_id'] = article_url.slug_id
                
                # Also check for selected URL for article type
                try:
                    selected_url_for_article = competitor_selected_url.objects.filter(
                        competitor_domain_mapping_id=domain_mapping
                    ).first()
                    if selected_url_for_article:
                        response_data['competitor_selected_url_slug_id'] = selected_url_for_article.slug_id
                except Exception as e:
                    print(f"Error finding selected URL for article: {str(e)}")
                    
            elif scrape_type == 'category' and selected_url:
                response_data['competitor_selected_url_slug_id'] = selected_url.slug_id
            
            # If type is article, also extract selectors
            if scrape_type == 'article':
                try:
                    print(f"Extracting selectors for article URL: {url_to_scrape}")
                    selector_result = extract_and_save_selectors(
                        article_url=url_to_scrape,
                        force_refresh=True,
                        competitor_article_url_slug_id=article_url.slug_id,
                        verified_by=''
                    )
                    print(f"Selector result: {selector_result}")
                    # Add selector results to response
                    response_data['selectors'] = {
                        'extraction_success': selector_result['success'],
                        'selectors_data': selector_result if selector_result['success'] else None,
                        'selector_error': selector_result.get('error') if not selector_result['success'] else None
                    }
                    
                    print(f"Selector extraction completed for URL: {url_to_scrape}")
                    
                except Exception as e:
                    print(f"Error extracting selectors for URL {url_to_scrape}: {str(e)}")
                    response_data['selectors'] = {
                        'extraction_success': False,
                        'selectors_data': None,
                        'selector_error': f'Error extracting selectors: {str(e)}'
                    }
            
            return JsonResponse({
                'status': 'success',
                'message': 'HTML content scraped and cleaned successfully' + (' with selector extraction' if scrape_type == 'article' else ''),
                'data': response_data
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': scrape_result['error'],
                'url': url_to_scrape
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON in request body'
        }, status=400)
        
    except Exception as e:
        print(f"Unexpected error in scrap_html_content_api: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred'
        }, status=500)


