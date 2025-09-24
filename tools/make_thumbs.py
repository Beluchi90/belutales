# tools/make_thumbs.py
import os, io, sys, time
from pathlib import Path
from PIL import Image, ImageOps

TARGET_W = 400   # list view width; adjust if needed
QUALITY = 80
METHOD = 6

SRC_DIRS = [
    "images",  # main images directory
    "assets/covers",
    "assets/images",
    "stories",  # in case covers live near story folders
]

THUMBS_ROOT = Path("assets/thumbs")

def is_image(p: Path):
    return p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}

def thumb_path_for(src: Path) -> Path:
    rel = src.as_posix().replace("\\", "/")
    rel = rel.lstrip("./")
    return THUMBS_ROOT.joinpath(rel + ".webp")

def ensure_thumb(src: Path):
    dst = thumb_path_for(src)
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Skip if up-to-date
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            return False

        img = Image.open(src)
        img = ImageOps.exif_transpose(img).convert("RGB")
        img.thumbnail((TARGET_W, TARGET_W*3), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=QUALITY, method=METHOD)
        dst.write_bytes(buf.getvalue())
        # Preserve source timestamp reference
        os.utime(dst, (src.stat().st_atime, src.stat().st_mtime))
        print(f"thumb -> {dst}")
        return True
    except Exception as e:
        print(f"skip {src}: {e}")
        return False

def walk_sources():
    made = 0
    for base in SRC_DIRS:
        b = Path(base)
        if not b.exists():
            continue
        for p in b.rglob("*"):
            if p.is_file() and is_image(p) and "thumbs" not in p.parts:
                if ensure_thumb(p):
                    made += 1
    print(f"Done. Created/updated {made} thumbnails.")

if __name__ == "__main__":
    walk_sources()
