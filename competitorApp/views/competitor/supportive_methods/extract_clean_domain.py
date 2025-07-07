import re


# helper function get clean domain
def extract_clean_domain(url):
    """
    Extracts domain name from a given URL or raw domain string.
    Removes http/https, www, paths, and query params.
    """
    if not url:
        return ""

    # Remove scheme (http, https) and www
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'^www\.', '', url)

    # Split by slash and get the domain part
    domain = url.split('/')[0]

    return domain

