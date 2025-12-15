from dataclasses import dataclass
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from functools import reduce
from .utils import get_string_attribute

# Priorities values below can (and should) be tweaked.
# I just sorta picked what I thought made sense.
# In the real world, we would have to actually test how well they perform.

ancestors: dict[str, int] = {
    'header': 4,
    'nav'   : 3,
    'a'     : 1,
}
"""Mapping of ancestor tags to their priority."""

keywords: dict[str, int] = {
    'logo'    : 4,
    'brand'   : 3,
    'branding': 3,
    'icon'    : 2,
    'name'    : 1,
}
"""Mapping of keywords to their priority."""

ancestor_list = list(ancestors.keys())
keyword_list  = list(keywords.keys())

def calculate_priority(keyword: int, ancestor: int) -> float:
    """
    Calculate a logo candidate's priority based on:
    - Its most relevant ancestor.
    - Its most relevant keyword (in the "alt" or "src" attribute).
    """
    return keyword * 1.5 + ancestor

# I adore dataclasses! A lot less boilerplate.
# This class is just a more descriptive tuple.
@dataclass(order=True)
class LogoCandidate:
    """A candidate for the website's logo."""
    priority: float
    src: str

@dataclass
class WebsiteInfo:
    """
    Relevant information about a website:
    - The URL.
    - The best candidate for a logo, if any.
    - The favicon, if any.
    """
    url: str
    logo: str | None = None
    favicon: str | None = None

# Parsing would be preferrable over a 'needle in haystack' search.
# As this is a small project, however, proper parsing is overkill.
def find_keywords(text: str) -> int:
    """Looks for keywords in a string. Returns highest keyword priority."""
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

        # Find keyword priority.
        alt = get_string_attribute(img, 'alt') or ''
        keyword = max(
            find_keywords(alt),
            find_keywords(src),
        )
        # Find ancestor priority.
        ancestor: int = reduce(
            lambda acc, e: max(acc, ancestors.get(e.name, 0)),
            img.find_parents(ancestor_list),
            0,
        )
        # Select the best logo candidate by ordering.
        priority  = calculate_priority(keyword, ancestor)
        candidate = LogoCandidate(priority, src)
        best      = max(best, candidate) if best is not None else candidate
    return best and best.src

def select_favicon(base_url: str, soup: BeautifulSoup) -> str | None:
    """Get a website's favicon, if any."""
    for link in soup.find_all('link'):
        # todo: can rel be a list??????
        rel  = get_string_attribute(link, 'rel')
        href = get_string_attribute(link, 'href')
        if not rel or not href:
            continue
        return urljoin(base_url, rel)
    return None

def parse(base_url: str, html: str) -> WebsiteInfo:
    """
    Parse HTML, extracting logo candidates.
    A favicon is also extracted as an extra consideration.
    """
    output = WebsiteInfo(base_url)
    try:
        # Parse HTML.
        soup = BeautifulSoup(html, 'html.parser')

        # Select best logo candidate + favicon.
        output.logo    = select_logo(base_url, soup)
        output.favicon = select_favicon(base_url, soup)
        return output
    except Exception as e:
        # todo: proper error handling
        return output 
