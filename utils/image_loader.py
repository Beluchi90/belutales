import os
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"
PLACEHOLDER = IMAGES_DIR / "placeholder.png"

def safe_image(image_path: str, caption: str = "", **kwargs):
    """
    Try to load and display an image safely.
    Falls back to placeholder.png if anything fails.
    """
    try:
        if not image_path:
            raise ValueError("Empty image path")

        full_path = IMAGES_DIR / os.path.basename(image_path)

        if not full_path.exists():
            raise FileNotFoundError(f"Missing image: {full_path}")

        st.image(str(full_path), caption=caption, use_container_width=True, **kwargs)
    except Exception:
        st.image(str(PLACEHOLDER), caption="Image missing", use_container_width=True)
