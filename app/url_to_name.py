import re
from urllib.parse import urlparse


def url_to_name(url: str) -> str:
    """Convert a URL to a filesystem-safe name using hyphen-case."""
    parsed = urlparse(url)

    # Combine domain and path
    name_parts = [parsed.netloc]
    if parsed.path and parsed.path != '/':
        name_parts.append(parsed.path.strip('/'))

    name = '-'.join(name_parts)

    # Replace any non-alphanumeric characters (except hyphen) with hyphen
    name = re.sub(r'[^a-zA-Z0-9-]', '-', name)

    # Convert to lowercase for consistency
    name = name.lower()

    # Remove consecutive hyphens
    name = re.sub(r'-+', '-', name)

    # Remove leading/trailing hyphens
    name = name.strip('-')

    return name
