from .fetch import fetch_html
from .parse import parse, WebsiteInfo
from urllib.parse import urlparse, urlunparse

# A bit of a hackaround to ensure netloc is properly parsed.
# This is because urlparse will *only* parse netloc if it's preceded by '//':
# https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
def normalize(address: str) -> str:
    return '//' + address if '//' not in address else address

def find_logo(website: str) -> WebsiteInfo:
    """Fetches a website's logo. Normalizes the URL before doing so."""
    parts = urlparse(normalize(website))
    for scheme in ('https', 'http'):
        url  = urlunparse(parts._replace(scheme=scheme))
        html = fetch_html(url)
        if html is not None:
            return parse(url, html)
    return WebsiteInfo(website)
