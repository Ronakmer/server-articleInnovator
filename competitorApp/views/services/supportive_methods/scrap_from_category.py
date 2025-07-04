import requests
from urllib.parse import urljoin
from typing import List
from bs4 import BeautifulSoup
import time
from lxml import html
import re


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


def scrape_articles_from_category_page(url: str, article_selector: str, proxy: str = None) -> List[str]:
    """
    Scrape article URLs from a category page using the article selector (supports both XPath and CSS)
    
    Args:
        url: The category page URL to scrape
        article_selector: XPath or CSS selector to find article links
        proxy: Optional proxy string (e.g., http://user:pass@ip:port)
    
    Returns:
        List of article URLs found on the page
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        proxies = {}
        if proxy:
            proxies = {'http': proxy, 'https': proxy}
        
        response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        response.raise_for_status()
        
        # Create both parsers
        soup = BeautifulSoup(response.content, 'html.parser')
        tree = html.fromstring(response.content)
        
        
        # Find article URLs using the selector
        article_links = []
        if article_selector:
            # Use appropriate parser based on selector type
            if is_xpath_selector(article_selector):
                elements = find_elements_with_selector(tree, article_selector)
                
                for element in elements:
                    if element.tag == 'a' and element.get('href'):
                        link = element.get('href')
                        # Convert relative URLs to absolute
                        if link.startswith('/'):
                            link = urljoin(url, link)
                        elif not link.startswith(('http://', 'https://')):
                            link = urljoin(url, link)
                        article_links.append(link)
                    else:
                        # Look for 'a' elements within this element
                        sub_links = element.xpath('.//a[@href]')
                        for sub_link in sub_links:
                            href = sub_link.get('href')
                            if href.startswith('/'):
                                href = urljoin(url, href)
                            elif not href.startswith(('http://', 'https://')):
                                href = urljoin(url, href)
                            article_links.append(href)
            else:
                # CSS selector
                elements = find_elements_with_selector(soup, article_selector)
                
                for element in elements:
                    if element.name == 'a' and element.get('href'):
                        link = element.get('href')
                        # Convert relative URLs to absolute
                        if link.startswith('/'):
                            link = urljoin(url, link)
                        elif not link.startswith(('http://', 'https://')):
                            link = urljoin(url, link)
                        article_links.append(link)
                    elif element.find('a'):
                        # If the selector finds a container, look for links inside
                        links = element.find_all('a', href=True)
                        for link in links:
                            href = link.get('href')
                            if href.startswith('/'):
                                href = urljoin(url, href)
                            elif not href.startswith(('http://', 'https://')):
                                href = urljoin(url, href)
                            article_links.append(href)
        
        return list(set(article_links))  # Remove duplicates
        
    except Exception as e:
        print(f"Error scraping articles from {url}: {e}")
        
        return []


def get_next_page_url(url: str, next_btn_selector: str, proxy: str = None) -> str:
    """
    Get the next page URL using the next button selector (supports both XPath and CSS)
    
    Args:
        url: Current page URL
        next_btn_selector: XPath or CSS selector to find the next button
        proxy: Optional proxy string
        
    Returns:
        Next page URL if found, None otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        proxies = {}
        if proxy:
            proxies = {'http': proxy, 'https': proxy}
        
        response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        response.raise_for_status()
        
        # Create both parsers
        soup = BeautifulSoup(response.content, 'html.parser')
        tree = html.fromstring(response.content)
        
        # Find next button using the selector
        if is_xpath_selector(next_btn_selector):
            next_element = find_elements_with_selector(tree, next_btn_selector, single=True)
            
            if next_element is not None:
                if next_element.tag == 'a' and next_element.get('href'):
                    next_url = next_element.get('href')
                    # Convert relative URLs to absolute
                    if next_url.startswith('/'):
                        next_url = urljoin(url, next_url)
                    elif not next_url.startswith(('http://', 'https://')):
                        next_url = urljoin(url, next_url)
                    return next_url
                else:
                    # Look for 'a' element within this element
                    sub_links = next_element.xpath('.//a[@href]')
                    if sub_links:
                        href = sub_links[0].get('href')
                        if href.startswith('/'):
                            href = urljoin(url, href)
                        elif not href.startswith(('http://', 'https://')):
                            href = urljoin(url, href)
                        return href
        else:
            # CSS selector
            next_element = find_elements_with_selector(soup, next_btn_selector, single=True)
            
            if next_element:
                if next_element.name == 'a' and next_element.get('href'):
                    next_url = next_element.get('href')
                    # Convert relative URLs to absolute
                    if next_url.startswith('/'):
                        next_url = urljoin(url, next_url)
                    elif not next_url.startswith(('http://', 'https://')):
                        next_url = urljoin(url, next_url)
                    return next_url
                elif next_element.find('a'):
                    # If the selector finds a container, look for link inside
                    link = next_element.find('a', href=True)
                    if link:
                        href = link.get('href')
                        if href.startswith('/'):
                            href = urljoin(url, href)
                        elif not href.startswith(('http://', 'https://')):
                            href = urljoin(url, href)
                        return href
        
        return None
        
    except Exception as e:
        print(f"Error getting next page URL from {url}: {e}")
        
        return None


def scrape_all_articles_with_pagination(base_url: str, article_selector: str, next_btn_selector: str = None, proxy: str = None, max_pages: int = 10) -> List[str]:
    """
    Scrape articles from all pages using pagination
    
    Args:
        base_url: Starting category page URL
        article_selector: CSS selector to find article links
        next_btn_selector: CSS selector to find next page button (optional)
        proxy: Optional proxy string
        max_pages: Maximum number of pages to scrape
        
    Returns:
        List of all article URLs found across all pages
    """
    all_articles = []
    current_url = base_url
    page_count = 0
    
    while current_url and page_count < max_pages:
        print(f"Scraping page {page_count + 1}: {current_url}")
        
        # Get articles from current page
        articles = scrape_articles_from_category_page(current_url, article_selector, proxy)
        all_articles.extend(articles)
        
        # Get next page URL if next button selector is provided
        if next_btn_selector:
            next_url = get_next_page_url(current_url, next_btn_selector, proxy)
            if next_url and next_url != current_url:  # Avoid infinite loops
                current_url = next_url
                page_count += 1
                time.sleep(1)  # Be respectful to the server
            else:
                break
        else:
            break
    
    return list(set(all_articles))  # Remove duplicates 