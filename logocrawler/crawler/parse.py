from dataclasses import dataclass
from enum import IntEnum
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Tag
from functools import reduce
from .utils import get_string_attribute

ancestor_tags: list[str] = ['header', 'nav', 'a']
"""List of relevant ancestor tags we want to look for."""

class Ancestor(IntEnum):
    """
    Relevant ancestors an <img> element can have, and their priority when selecting.
    Higher priority is better.
    When an <img> has more than one relevant ancestor, select the one with the highest priority.
    """
    HEADER = 3
    NAV    = 2
    ANCHOR = 1
    OTHER  = 0
    @classmethod
    def from_tag(cls, tag: str):
        match tag:
            case 'header': return cls.HEADER
            case 'nav'   : return cls.NAV
            case 'a'     : return cls.ANCHOR
            case _       : return cls.OTHER

class KeywordPlacement(IntEnum):
    """
    Places where the 'logo' keyword could be found, and their associated priority.
    Higher priority is better.
    If the keyword was found in more than once place, select the one with the highest priority.
    """
    ALT  = 2
    SRC  = 1
    NONE = 0

# Dataclasses are one of my favorite things about Python. I'm using them here for a few reasons:
# - less boilerplate, implicit constructor
# - free __hash__() implementation based on class fields
# - free __eq__() and __le__() implementation based on class fields, *in order*.
@dataclass(order=True)
class LogoCandidate:
    """A candidate for the website's logo."""
    keyword: KeywordPlacement
    ancestor: Ancestor
    src: str

@dataclass
class LogoData:
    """
    Logo information for a website:
    - the best logo candidate
    - the favicon, if any
    """
    logo: LogoCandidate | None
    favicon: str | None

# In the real world, we would have more keywords to match against.
# I would also do proper parsing instead of a 'needle in haystack' search.
# However, as this is a small test assignment, I think this is just enough.
def find_keyword(img: Tag) -> KeywordPlacement:
    """Try to find the 'logo' keyword in the image's attributes."""
    alt = get_string_attribute(img, 'src') or ''
    src = get_string_attribute(img, 'alt') or ''

    if 'logo' in alt.lower():
        return KeywordPlacement.ALT

    if 'logo' in src.lower():
        return KeywordPlacement.SRC

    return KeywordPlacement.NONE

# Select best logo candidate. For each <img> element in the DOM:
# - find all ancestors in the ['header', 'nav', 'a'] set
# - look at alt and src attributes for the 'logo' keyword
def select_logo(base_url: str, soup: BeautifulSoup) -> LogoCandidate | None:
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

        # Find most relevant ancestor.
        ancestor: Ancestor = reduce(
            lambda acc, e: max(acc, Ancestor.from_tag(e.name)),
            img.find_parents(ancestor_tags),
            Ancestor.OTHER,
        )
        # Find relevant keyword placement.
        keyword = find_keyword(img)

        # Select the best logo candidate by ordering.
        candidate = LogoCandidate(keyword, ancestor, src)
        best = max(best, candidate) if best is not None else candidate
    return best

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

def parse(base_url: str, html: str) -> LogoData | None:
    """
    Parse HTML, extracting logo candidates.
    A favicon is also extracted as an extra consideration.
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Select best logo candidate + favicon.
        logo = select_logo(base_url, soup)
        favi = select_favicon(base_url, soup)
        return LogoData(logo, favi)
    except Exception as e:
        # todo: proper error handling
        return None
