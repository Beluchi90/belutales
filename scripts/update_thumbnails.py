# scripts/update_thumbnails.py
import os, json, datetime

JSON_PATH = "stories.json"
IMAGES_DIR = "images"

def find_thumbnail_for_slug(slug: str) -> str:
    """Find thumbnail for a story slug with fallback logic"""
    
    # Rule 1: Try {slug}_1.png first (always the first cover image)
    primary = os.path.join(IMAGES_DIR, f"{slug}_1.png")
    if os.path.exists(primary):
        return f"images/{slug}_1.png"
    
    # Rule 2: Try {slug}.png
    secondary = os.path.join(IMAGES_DIR, f"{slug}.png")
    if os.path.exists(secondary):
        return f"images/{slug}.png"
    
    # Rule 3: Try {slug}_mid.png
    tertiary = os.path.join(IMAGES_DIR, f"{slug}_mid.png")
    if os.path.exists(tertiary):
        return f"images/{slug}_mid.png"
    
    # Rule 4: Fallback to logo.png
    return "images/logo.png"

def main():
    if not os.path.exists(JSON_PATH):
        raise SystemExit(f"stories.json not found at {JSON_PATH}")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        stories = json.load(f)

    # Rule 5: Make a backup before writing
    backup_name = f"stories.backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_name, "w", encoding="utf-8") as b:
        json.dump(stories, b, ensure_ascii=False, indent=2)

    updated = 0
    fallback_count = 0

    for story in stories:
        # Get the slug for this story
        slug = story.get("slug", "")
        if not slug:
            # Generate slug from title if missing
            title = story.get("title", "")
            if title:
                slug = title.lower().replace(" ", "-")
                slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        if slug:
            # Rule 6: Do not change any other story fields, only add thumbnail
            thumbnail_path = find_thumbnail_for_slug(slug)
            story["thumbnail"] = thumbnail_path
            updated += 1
            
            if thumbnail_path == "images/logo.png":
                fallback_count += 1

    # Rule 4: Overwrite stories.json with the updated data
    with open(JSON_PATH, "w", encoding="utf-8") as out:
        json.dump(stories, out, ensure_ascii=False, indent=2)

    print(f"Updated {updated} stories with thumbnails.")
    print(f"Used fallback logo.png for {fallback_count} stories.")
    print(f"Backup saved as {backup_name}")

if __name__ == "__main__":
    main()
