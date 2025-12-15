import requests
from requests.exceptions import RequestException

# I chose to use an honest user agent, despite knowing that
# using a browser UA will lead to better results,
headers = {'User-Agent': 'logocrawler/0.1', 'Accept': 'text-html'}
timeout = 5

def fetch_html(url: str) -> str | None:
    """Fetches a page's HTML content as a string."""
    try:
        res = requests.get(url, headers=headers, timeout=timeout)
        res.raise_for_status() # I prefer raising.

        # In the real world, I would use a proper parser for Content-Type headers.
        # As this is just a small project, though, string comparison is fine.
        content_type = res.headers.get('Content-Type', '')
        if 'text/html' not in content_type.lower():
            return None
        return res.text
    except RequestException:
        # todo: Add proper error handling / logging.
        return None
