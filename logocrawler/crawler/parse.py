from dataclasses import dataclass
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .utils import get_string_attribute

# Priorities values below can (and should) be tweaked.
# I just sorta picked what I thought made sense.
# In the real world, we would have to actually test how well they perform.

ancestors: dict[str, int] = {
    'header': 5,
    'nav'   : 2,
    'a'     : 1,
}
"""Mapping of ancestor tags to their priority."""

keywords: dict[str, int] = {
    'logo'    : 5,
    'brand'   : 2,
    'branding': 1,
}
"""Mapping of keywords to their priority."""

ancestor_list = list(ancestors.keys())
keyword_list  = list(keywords.keys())

# I adore dataclasses! A lot less boilerplate.
# This class is just a more descriptive tuple.
@dataclass(order=True)
class LogoCandidate:
    """A candidate for the website's logo."""
    priority: int
    src     : str

@dataclass
class WebsiteInfo:
    """
    Relevant information about a website:
    - The URL.
    - The best candidate for a logo, if any.
    - The favicon, if any.
    """
    url    : str
    logo   : str | None = None
    favicon: str | None = None

# Parsing would be preferrable over a 'needle in haystack' search.
# As this is a small project, however, proper parsing is overkill.
def find_keyword(text: str) -> int:
    """Find highest priority keyword in string, if any."""
    low  = text.lower()
    best = 0
    for word in keyword_list:
        if word in low:
            best = max(best, keywords.get(word, 0))
    return best

# Select best logo candidate. For each <img> element in the DOM:
# - find all ancestors in the ['header', 'nav', 'a'] set
# - look at alt and src attributes for the 'logo' keyword
def select_logo(base_url: str, soup: BeautifulSoup) -> str | None:
    """
    Select best logo candidate in the DOM.
    """
    best: LogoCandidate | None = None
    for img in soup.find_all('img'):
        # Get src. If img has no 'src' attribute, it's useless.
        src = get_string_attribute(img, 'src')
        if src is None:
            continue
        src = urljoin(base_url, src)

        # Calculate priority.
        priority = 0

        # 1. Keywords.
        alt = get_string_attribute(img, 'alt') or ''
        for attribute in (src, alt):
            priority += find_keyword(attribute)

        # 2. Ancestors (stored as a set to ensure unique entries).
        ancs: set[str] = {e.name for e in img.find_parents(ancestor_list)}
        for ancestor in ancs:
            priority += ancestors.get(ancestor, 0)

        candidate = LogoCandidate(priority, src)
        best      = max(best, candidate) if best is not None else candidate
    return best and best.src

def select_favicon(base_url: str, soup: BeautifulSoup) -> str | None:
    """Get a website's favicon, if any."""
    for link in soup.find_all('link'):
        rel  = link.attrs.get('rel')
        href = get_string_attribute(link, 'href')
        if href and isinstance(rel, list) and 'icon' in rel:
            return urljoin(base_url, href)
    return None

def parse(base_url: str, html: str) -> WebsiteInfo:
    """
    Parse HTML, extracting logo candidates.
    A favicon is also extracted as an extra consideration.
    """
    # Parse HTML.
    soup = BeautifulSoup(html, 'html.parser')

    # Select best logo candidate + favicon.
    logo    = select_logo(base_url, soup)
    favicon = select_favicon(base_url, soup)
    return WebsiteInfo(base_url, logo, favicon)
