"""
services/scraper.py — Backend Enrichment Service.

Responsible for:
1. Fetching HTML content from a given URL via httpx.
2. Parsing OpenGraph/meta tags and page title via BeautifulSoup4.
3. Inferring the content type (article, video, tool, etc.) from the URL domain.

This runs as a FastAPI BackgroundTask after an item is created,
updating the item's fields once metadata has been extracted.
"""

import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# ── User-Agent Spoofing ───────────────────────────────────────────────────────
# Many sites block default Python user agents. We mimic a browser.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ── Domain-to-Type Mapping ────────────────────────────────────────────────────
# Maps known domains to deterministic item types.
DOMAIN_TYPE_MAP = {
    # Video
    "youtube.com": "video",
    "youtu.be": "video",
    "vimeo.com": "video",
    "twitch.tv": "video",
    # Dev Tools
    "github.com": "tool",
    "gitlab.com": "tool",
    "npmjs.com": "tool",
    "pypi.org": "tool",
    "hub.docker.com": "tool",
    # Docs / Reference
    "docs.python.org": "article",
    "developer.mozilla.org": "article",
    "stackoverflow.com": "article",
    "medium.com": "article",
    "dev.to": "article",
    "substack.com": "article",
    "hashnode.com": "article",
    "notion.so": "note",
    # Social
    "twitter.com": "link",
    "x.com": "link",
    "reddit.com": "link",
    "linkedin.com": "link",
    # Shopping / Products
    "amazon.com": "link",
    "producthunt.com": "link",
}


# ── Core Functions ────────────────────────────────────────────────────────────

def fetch_html(url: str, timeout: int = 10) -> Optional[str]:
    """
    Fetches the HTML content of a URL using httpx.
    Returns the HTML string, or None if the request fails.
    """
    try:
        with httpx.Client(headers=HEADERS, timeout=timeout, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.text
    except httpx.TimeoutException:
        logger.warning(f"Scraper timeout fetching URL: {url}")
        return None
    except httpx.HTTPStatusError as e:
        logger.warning(f"Scraper HTTP error {e.response.status_code} for URL: {url}")
        return None
    except Exception as e:
        logger.error(f"Scraper unexpected error for URL {url}: {e}")
        return None


def parse_metadata(html: str) -> dict:
    """
    Parses OpenGraph tags, Twitter Card tags, and page title from HTML.

    Returns a dict with keys:
        title, description, image (thumbnail URL), og_type, site_name
    """
    soup = BeautifulSoup(html, "html.parser")

    def get_meta(property: str = None, name: str = None) -> Optional[str]:
        """Helper to extract content from meta tags."""
        if property:
            tag = soup.find("meta", property=property)
        elif name:
            tag = soup.find("meta", attrs={"name": name})
        else:
            return None
        return tag.get("content") if tag else None

    # Priority: OpenGraph > Twitter Card > Standard HTML tags
    title = (
        get_meta(property="og:title")
        or get_meta(name="twitter:title")
        or (soup.title.string.strip() if soup.title and soup.title.string else None)
    )

    description = (
        get_meta(property="og:description")
        or get_meta(name="twitter:description")
        or get_meta(name="description")
    )

    image = (
        get_meta(property="og:image")
        or get_meta(name="twitter:image")
    )

    og_type = get_meta(property="og:type")
    site_name = get_meta(property="og:site_name")

    return {
        "title": title,
        "description": description,
        "image": image,
        "og_type": og_type,
        "site_name": site_name,
    }


def infer_type(url: str, metadata: dict) -> str:
    """
    Infers item_type from the domain or OpenGraph type.

    Priority: domain map > og:type > fallback 'link'
    """
    try:
        parsed = urlparse(url)
        # Strip 'www.' prefix for matching
        domain = parsed.netloc.lower().replace("www.", "")
        if domain in DOMAIN_TYPE_MAP:
            return DOMAIN_TYPE_MAP[domain]
    except Exception:
        pass

    # Fallback: use og:type
    og_type = metadata.get("og_type", "")
    if og_type:
        if "video" in og_type:
            return "video"
        if "article" in og_type:
            return "article"

    return "link"


# ── Main Enrichment Function ──────────────────────────────────────────────────

def enrich_url(url: str) -> dict:
    """
    Full enrichment pipeline for a single URL.

    Steps:
    1. Fetch HTML.
    2. Parse metadata (title, description, image).
    3. Infer item type.

    Returns a dict of fields to update on the Item record.
    Returns status='failed' if fetch fails.
    """
    html = fetch_html(url)

    if not html:
        return {
            "processing_status": "failed",
            "metadata_json": {"error": "Failed to fetch URL content"},
        }

    metadata = parse_metadata(html)
    item_type = infer_type(url, metadata)

    # Build the source domain label
    try:
        parsed = urlparse(url)
        source = parsed.netloc.lower().replace("www.", "")
    except Exception:
        source = None

    return {
        "title": metadata.get("title"),
        "description": metadata.get("description"),
        "thumbnail": metadata.get("image"),
        "source": source,
        "item_type": item_type,
        "processing_status": "completed",
        "metadata_json": metadata,
    }
