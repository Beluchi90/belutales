from pathlib import Path
from typing import Optional, Union
from PIL import Image, UnidentifiedImageError
import io
import os
try:
    import streamlit as st
    import pillow_avif  # noqa: F401  # enables AVIF support if installed
except Exception:
    pass

SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tiff", ".avif"}

def load_image_safe(src: Union[str, Path, bytes, io.BytesIO]) -> Optional[Image.Image]:
    """
    Attempts to open an image robustly:
    - Accepts path, bytes, or BytesIO.
    - Normalizes WEBP/AVIF if Pillow supports it.
    - Returns a PIL Image or None if it can't be opened.
    """
    try:
        if isinstance(src, (bytes, io.BytesIO)):
            data = src if isinstance(src, bytes) else src.getvalue()
            return Image.open(io.BytesIO(data)).convert("RGBA")

        p = Path(src)
        if not p.exists() or not p.is_file():
            return None

        # Quick extension sanity check (helps catch mislabeled files)
        if p.suffix.lower() not in SUPPORTED_EXTS:
            # Still try to open—extension might be wrong but bytes valid
            img = Image.open(p)
            return img.convert("RGBA")

        img = Image.open(p)
        img.load()  # force decode to surface errors early
        return img.convert("RGBA")
    except (UnidentifiedImageError, OSError, ValueError):
        return None

def safe_image(path, **kwargs):
    """
    Safely display an image with automatic fallback to placeholder.png.
    
    Args:
        path: Path to the image file
        **kwargs: Additional arguments to pass to st.image()
    """
    # Set default use_container_width if not provided
    if 'use_container_width' not in kwargs:
        kwargs['use_container_width'] = True
    
    # Try to load the requested image
    img = load_image_safe(path) if path else None
    if img:
        st.image(img, **kwargs)
        return
    
    # Fallback to placeholder
    # Get the base directory (assuming this is called from the main app directory)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    placeholder_path = os.path.join(base_dir, "images", "placeholder.png")
    placeholder = load_image_safe(placeholder_path)
    
    if placeholder:
        # Preserve caption but indicate it's a placeholder
        if 'caption' in kwargs:
            original_caption = kwargs['caption']
            kwargs['caption'] = f"{original_caption} (placeholder)"
        else:
            kwargs['caption'] = "🖼 Illustration coming soon"
        st.image(placeholder, **kwargs)
    else:
        st.warning("🖼 Illustration coming soon")
