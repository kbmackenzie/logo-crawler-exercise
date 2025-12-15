from .fetch import fetch_html
from .parse import parse, LogoData

def find_logo(url: str) -> LogoData | None:
    html = fetch_html(url)
    return parse(url, html) if html is not None else None
