import re
from urllib.parse import urlparse


def url_to_name(url: str) -> str:
    """Convert a URL to a filesystem-safe name."""
    parsed = urlparse(url)

    # Combine domain and path
    name_parts = [parsed.netloc]
    if parsed.path and parsed.path != '/':
        name_parts.append(parsed.path.strip('/'))

    name = '_'.join(name_parts)

    # Replace any non-alphanumeric characters (except underscore and hyphen) with underscore
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)

    # Remove consecutive underscores
    name = re.sub(r'_+', '_', name)

    # Remove leading/trailing underscores
    name = name.strip('_')

    return name
