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
        # I prefer letting it raise here.
        res.raise_for_status()

        # Ensure we have actually received HTML.
        # 
        # In the real world, I would referrably look into using a proper parser
        # for Content-Type headers rather than simply string matching.
        content_type = res.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            return None
        return res.text

    except RequestException as e:
        # todo: proper error handling / logging
        return None
