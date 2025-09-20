import os
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"
PLACEHOLDER = IMAGES_DIR / "placeholder.png"

def safe_image(image_path: str, caption: str = "", **kwargs):
    """
    Never crashes - always displays either the real image or placeholder.
    
    1. If image_path is None or empty → use PLACEHOLDER
    2. If image_path is relative name → join with IMAGES_DIR  
    3. If file exists → display it with st.image
    4. If file does not exist → display PLACEHOLDER
    """
    try:
        # Handle None or empty image_path
        if not image_path:
            st.image(str(PLACEHOLDER), caption=caption, use_container_width=True, **kwargs)
            return
        
        # If image_path is a relative name, join with IMAGES_DIR
        if not os.path.isabs(image_path):
            full_path = IMAGES_DIR / image_path
        else:
            full_path = Path(image_path)
        
        # Check if file exists
        if full_path.exists():
            # Display the real image
            st.image(str(full_path), caption=caption, use_container_width=True, **kwargs)
        else:
            # Display PLACEHOLDER
            st.image(str(PLACEHOLDER), caption=caption, use_container_width=True, **kwargs)
            
    except Exception:
        # Always fallback to PLACEHOLDER instead of raising errors
        st.image(str(PLACEHOLDER), caption=caption, use_container_width=True, **kwargs)
