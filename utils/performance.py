"""
Performance optimization utilities for BeluTales.
Implements caching, lazy loading, thumbnails, and pagination.
"""

import streamlit as st
import json
import orjson
import math
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from PIL import Image, ImageOps
import io
import hashlib
from collections import Counter

# Constants
PAGE_SIZE = 10
THUMBNAIL_SIZE = (400, 400)
THUMBNAIL_CACHE_DIR = Path(".cache/thumbnails")
THUMBNAIL_CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Try to import orjson, fallback to json
try:
    import orjson
    def load_json_fast(path: str) -> dict:
        """Fast JSON loading with orjson"""
        with open(path, "rb") as f:
            return orjson.loads(f.read())
except ImportError:
    def load_json_fast(path: str) -> dict:
        """Fallback JSON loading"""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

@st.cache_data(show_spinner=False, ttl=3600)
def load_story_index() -> List[Dict]:
    """
    Load lightweight story index with only essential fields for list view.
    Returns list of dicts with: id, title, category, cover_path, premium flag, snippet
    """
    stories_file = Path("stories.json")
    if not stories_file.exists():
        return []
    
    try:
        data = load_json_fast(str(stories_file))
        stories = data if isinstance(data, list) else data.get("stories", [])
        
        # Create lightweight index with only essential fields
        index = []
        for story in stories:
            # Generate unique ID from title
            story_id = hashlib.md5(story.get("title", "").encode()).hexdigest()[:8]
            
            # Extract essential fields only
            index_entry = {
                "id": story_id,
                "title": story.get("title", "Untitled"),
                "category": story.get("category", "General"),
                "cover_path": story.get("cover_image", ""),
                "is_premium": story.get("is_premium", False),
                "snippet": story.get("text", story.get("content", ""))[:200] + "..." if len(story.get("text", story.get("content", ""))) > 200 else story.get("text", story.get("content", "")),
                "original_index": len(index)  # Store original index for full loading
            }
            index.append(index_entry)
        
        return index
    except Exception as e:
        st.error(f"Error loading story index: {e}")
        return []

@st.cache_data(show_spinner=False, ttl=3600)
def load_story_full(story_id: str) -> Optional[Dict]:
    """
    Load full story content by ID. Only called when viewing story details.
    Returns complete story data including full text, images, audio paths.
    """
    stories_file = Path("stories.json")
    if not stories_file.exists():
        return None
    
    try:
        data = load_json_fast(str(stories_file))
        stories = data if isinstance(data, list) else data.get("stories", [])
        
        # Find story by ID
        for story in stories:
            story_id_check = hashlib.md5(story.get("title", "").encode()).hexdigest()[:8]
            if story_id_check == story_id:
                return story
        
        return None
    except Exception as e:
        st.error(f"Error loading full story: {e}")
        return None

@st.cache_data(show_spinner=False)
def get_thumbnail(path: str, max_w: int = 400, **_ignored) -> bytes:
    """
    Returns a WebP thumbnail (bytes) for the image at `path`.
    Accepts `max_w` and ignores any unexpected keyword args to stay backward-compatible.
    Prefers pre-generated assets/thumbs/* if available,
    otherwise generates a cached in-memory thumb on the fly.
    Safe, cached, and tolerant of bad files or missing paths.
    """
    try:
        if not path:
            return b""

        src = Path(path)
        # Prefer pre-generated thumbnail if present (assets/thumbs/<original>.webp)
        thumb_candidate = Path("assets/thumbs") / (src.as_posix().replace("\\", "/").lstrip("./") + ".webp")
        if thumb_candidate.exists():
            try:
                return thumb_candidate.read_bytes()
            except Exception:
                pass

        if not src.exists():
            return b""

        img = Image.open(src)
        img = ImageOps.exif_transpose(img).convert("RGB")
        img.thumbnail((max_w, max_w * 3), Image.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=80, method=6)
        return buf.getvalue()
    except Exception:
        return b""

@st.cache_resource(show_spinner=False)
def get_clients():
    """
    Cache long-lived clients (TTS, PayPal, etc.) to avoid recreation.
    Returns dict of cached clients.
    """
    clients = {}
    
    # TTS client
    try:
        from gtts import gTTS
        clients['tts'] = gTTS
    except ImportError:
        clients['tts'] = None
    
    # PayPal client (if available)
    try:
        from paypal_integration import init_paypal_session
        clients['paypal'] = init_paypal_session()
    except ImportError:
        clients['paypal'] = None
    
    return clients

def debounce_search(key: str = "search_query", delay: float = 0.3) -> str:
    """
    Debounced search input that only processes after user stops typing.
    Returns the current search query.
    """
    # Initialize search state
    if f"{key}_last_update" not in st.session_state:
        st.session_state[f"{key}_last_update"] = 0
    if f"{key}_value" not in st.session_state:
        st.session_state[f"{key}_value"] = ""
    
    # Get current time
    current_time = time.time()
    
    # Check if enough time has passed since last update
    if current_time - st.session_state[f"{key}_last_update"] > delay:
        # Process the search query
        query = st.session_state[f"{key}_value"]
        return query
    
    return st.session_state[f"{key}_value"]

def get_pagination_info(total_items: int, page: int = 1) -> Tuple[int, int, int, int]:
    """
    Calculate pagination info.
    Returns: (current_page, total_pages, start_idx, end_idx)
    """
    total_pages = max(1, math.ceil(total_items / PAGE_SIZE))
    current_page = max(1, min(page, total_pages))
    start_idx = (current_page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    
    return current_page, total_pages, start_idx, end_idx

def apply_filters_optimized(stories: List[Dict], filters: Dict) -> List[Dict]:
    """
    Optimized filtering that works on lightweight story index.
    Much faster than processing full story content.
    """
    filtered = []
    
    for story in stories:
        # Text search (only on title, category, snippet)
        if filters.get("search_text"):
            searchable = f"{story.get('title', '')} {story.get('category', '')} {story.get('snippet', '')}".lower()
            if filters["search_text"].lower() not in searchable:
                continue
        
        # Category filter
        if filters.get("category") and filters["category"] != "All":
            # Handle "Favorites" as a special category
            if filters["category"] == "Favorites":
                if story.get("title") not in filters.get("favorite_ids", set()):
                    continue
            else:
                if story.get("category") != filters["category"]:
                    continue
        
        # Premium filter
        if filters.get("story_type") == "Free" and story.get("is_premium", False):
            continue
        if filters.get("story_type") == "Premium" and not story.get("is_premium", False):
            continue
        
        # Favorites filter
        if filters.get("favorites_only") and story.get("title") not in filters.get("favorite_ids", set()):
            continue
        
        filtered.append(story)
    
    return filtered

@st.cache_data(show_spinner=False, ttl=300)
def get_categories_optimized(stories: List[Dict]) -> Dict[str, int]:
    """
    Get categories with counts from lightweight story index.
    Much faster than processing full stories.
    Normalizes categories to prevent duplicates.
    """
    # Import normalize_category from app.py
    import sys
    if 'app' in sys.modules:
        from app import normalize_category
    else:
        # Fallback normalize function if app not imported
        def normalize_category(s: str) -> str:
            if not s:
                return "General"
            return s.strip().title()
    
    # Normalize all categories to prevent duplicates
    categories = [normalize_category(story.get("category", "General")) for story in stories]
    counts = Counter(categories)
    counts = dict(sorted(counts.items()))
    counts = {"All": len(stories), **counts}
    return counts

def render_pagination_controls(current_page: int, total_pages: int, key_prefix: str = "page"):
    """
    Render pagination controls with Next/Previous buttons.
    Updates st.query_params for URL-based pagination.
    """
    if total_pages <= 1:
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Previous", disabled=current_page <= 1, key=f"{key_prefix}_prev"):
            st.query_params["page"] = str(current_page - 1)
            st.rerun()
    
    with col2:
        st.write(f"**Page {current_page} of {total_pages}**")
    
    with col3:
        if st.button("Next ➡️", disabled=current_page >= total_pages, key=f"{key_prefix}_next"):
            st.query_params["page"] = str(current_page + 1)
            st.rerun()

def get_current_page() -> int:
    """
    Get current page from query params with validation.
    """
    page_str = st.query_params.get("page", "1")
    try:
        page = max(1, int(page_str))
        return page
    except (ValueError, TypeError):
        return 1

def clear_cache():
    """
    Clear all performance caches.
    Useful for development or when data changes.
    """
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("Performance caches cleared!")
