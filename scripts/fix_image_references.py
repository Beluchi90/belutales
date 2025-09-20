import json, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"
STORIES_JSON = BASE_DIR / "stories.json"

with open(STORIES_JSON, "r", encoding="utf-8") as f:
    stories = json.load(f)

for story in stories:
    thumb = story.get("thumbnail", "")
    if not thumb or not (IMAGES_DIR / os.path.basename(thumb)).exists():
        story["thumbnail"] = f"images/{story['id']}.png"

with open(STORIES_JSON, "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=2, ensure_ascii=False)

print("✅ Fixed all story thumbnails to point to images/")