from .fetch import fetch_html
from .parse import parse, WebsiteInfo

def find_logo(url: str) -> WebsiteInfo:
    html = fetch_html(url)
    if html is None:
        # If no HTML could be fetched, simply return an empty info object.
        return WebsiteInfo(url)
    # Parse HTML.
    return parse(url, html)
