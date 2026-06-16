import re
import unicodedata

def generate_slug(text: str) -> str:
    """
    Generate a URL-friendly slug from a string.
    """
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text
