import os
import json
import re
from datetime import datetime

# Paths
STORIES_FILE = "stories.json"
IMAGES_DIR = "images"

# Backup
backup_file = f"stories.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
os.rename(STORIES_FILE, backup_file)
print(f"📦 Backup created: {backup_file}")

# Load stories.json
with open(backup_file, "r", encoding="utf-8") as f:
    stories = json.load(f)

# Get all available image files in /images
available_images = set(os.listdir(IMAGES_DIR))

# Slugify helper
def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)  # replace non-alphanumeric with "-"
    slug = re.sub(r"-+", "-", slug)          # collapse multiple "-"
    return slug.strip("-")

# Fix references
updated_count = 0
for story in stories:
    title = story.get("title", "")
    slug = slugify(title)

    expected = {
        "cover_image": f"{slug}_1.png",
        "mid_image": f"{slug}_2.png",
        "end_image": f"{slug}_3.png",
        "thumbnail": f"{slug}_1.png",
    }

    fixed = {}
    for key, filename in expected.items():
        if filename in available_images:
            story[key] = filename
            fixed[key] = filename

    if fixed:
        updated_count += 1
        print(f"✅ {title} → {fixed}")

# Save fixed stories.json
with open(STORIES_FILE, "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=2, ensure_ascii=False)

print(f"\n🎉 Fixed image references for {updated_count} stories")
