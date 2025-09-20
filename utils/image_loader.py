import os
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"
PLACEHOLDER = IMAGES_DIR / "placeholder.png"

def safe_image(image_path: str, caption: str = "", **kwargs):
    """
    Always loads a valid image - either the real image or placeholder.
    
    1. If image_path is None, empty, or does not exist → show PLACEHOLDER
    2. If image_path exists → load it with st.image
    3. Never crashes - always displays something
    """
    try:
        # Check if we have a valid image path that exists
        if not image_path or not Path(image_path).exists():
            # Use PLACEHOLDER
            st.image(str(PLACEHOLDER), caption=caption or "Image missing", use_container_width=True, **kwargs)
        else:
            # Show the real image
            st.image(image_path, caption=caption, use_container_width=True, **kwargs)
    except Exception:
        # Ultimate fallback - always show placeholder if anything goes wrong
        st.image(str(PLACEHOLDER), caption="Image missing", use_container_width=True)
