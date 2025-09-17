import os
import json
import datetime
import glob

def main():
    JSON_PATH = "stories.json"
    IMAGES_DIR = "images"
    
    # Load stories.json
    if not os.path.exists(JSON_PATH):
        print(f"Error: {JSON_PATH} not found")
        return
    
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        stories = json.load(f)
    
    # Create backup with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"stories.backup.{timestamp}.json"
    
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    print(f"Backup created: {backup_path}")
    
    # Process each story
    updated_count = 0
    skipped_count = 0
    
    for story in stories:
        # Get the slug from the story
        slug = story.get("slug", "")
        if not slug:
            # Try to get from title if no slug
            title = story.get("title", "")
            if title:
                # Simple slugify: lowercase, replace spaces with hyphens
                slug = title.lower().replace(" ", "-")
                # Remove special characters, keep only alphanumeric and hyphens
                slug = ''.join(c for c in slug if c.isalnum() or c == '-')
            else:
                skipped_count += 1
                continue
        
        # Look for thumbnail files
        thumbnail_path = None
        
        # First try: look for <slug>_1.png
        candidate1 = os.path.join(IMAGES_DIR, f"{slug}_1.png")
        if os.path.exists(candidate1):
            thumbnail_path = candidate1
        else:
            # Second try: look for <slug>_mid.png
            candidate2 = os.path.join(IMAGES_DIR, f"{slug}_mid.png")
            if os.path.exists(candidate2):
                thumbnail_path = candidate2
        
        # If we found a thumbnail, add it to the story
        if thumbnail_path:
            # Convert backslashes to forward slashes for consistency
            story["thumbnail"] = thumbnail_path.replace("\\", "/")
            updated_count += 1
        else:
            # Skip but leave story unchanged
            skipped_count += 1
    
    # Save the updated JSON
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    
    print(f"Processing complete:")
    print(f"  - Updated {updated_count} stories with thumbnails")
    print(f"  - Skipped {skipped_count} stories (no matching image found)")
    print(f"  - Backup saved as {backup_path}")

if __name__ == "__main__":
    main()