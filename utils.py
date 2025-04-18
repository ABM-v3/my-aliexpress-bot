import re
from urllib.parse import urlparse

def extract_aliexpress_url(text):
    # Simple regex to find AliExpress URLs (might need refinement)
    patterns = [
        r'(https?://[a-zA-Z0-9.-]*\.aliexpress\.com/item/[0-9]+\.html)',
        r'(https?://[a-zA-Z0-9.-]*\.aliexpress\.com/e/[_a-zA-Z0-9]+)', # Short links like /e/
        # Add more patterns if needed
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None

def is_valid_aliexpress_url(url):
     if not url:
         return False
     try:
         parsed = urlparse(url)
         # Check if domain ends with aliexpress.com and has a path component (item, e, etc.)
         return parsed.scheme in ['http', 'https'] and \
                parsed.netloc.endswith('aliexpress.com') and \
                (parsed.path.startswith('/item/') or parsed.path.startswith('/e/')) # Add other valid paths
     except:
         return False
