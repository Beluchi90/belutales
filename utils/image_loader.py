from pathlib import Path
from typing import Optional, Union
from PIL import Image, UnidentifiedImageError
import io
try:
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
