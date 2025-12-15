from bs4 import Tag

def get_string_attribute(tag: Tag, key: str) -> str | None:
    """
    Returns an attribute's value from a Tag only if it's a string, otherwise return None.

    In BeautifulSoup4 Tag objects, attribute values are not guaranteed to be strings.
    Attributes values have the union type '_AttributeValue', which includes lists.
    There is a reason for this: attributes can have lists as values (e.g. the 'class' attribute).

    I'm writing this utility just to avoid the headache of constantly type-checking.
    """
    value = tag.attrs.get(key)
    return value if isinstance(value, str) else None
