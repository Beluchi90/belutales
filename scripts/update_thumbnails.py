import os
import json
import datetime

def main():
    JSON_PATH = "stories.json"
    IMAGES_DIR = "images"
    
    # Load stories.json
    if not os.path.exists(JSON_PATH):
        print(f"Error: {JSON_PATH} not found")
        return
    
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        stories = json.load(f)
    
    # Save backup before writing
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"stories.backup.{timestamp}.json"
    
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    
    # Process each story
    updated_count = 0
    fallback_count = 0
    
    for story in stories:
        # Check if it already has a "thumbnail" field
        if "thumbnail" in story:
            continue
        
        # Get the slug for this story
        slug = story.get("slug", "")
        if not slug:
            # Generate slug from title if missing
            title = story.get("title", "")
            if title:
                slug = title.lower().replace(" ", "-")
                slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        if not slug:
            continue
        
        # Generate thumbnail automatically with fallback logic
        thumbnail_path = None
        
        # Preferred: "images/{slug}_1.png"
        preferred = os.path.join(IMAGES_DIR, f"{slug}_1.png")
        if os.path.exists(preferred):
            thumbnail_path = f"images/{slug}_1.png"
        else:
            # If not found: "images/{slug}.png"
            secondary = os.path.join(IMAGES_DIR, f"{slug}.png")
            if os.path.exists(secondary):
                thumbnail_path = f"images/{slug}.png"
            else:
                # If not found: "images/{slug}_mid.png"
                tertiary = os.path.join(IMAGES_DIR, f"{slug}_mid.png")
                if os.path.exists(tertiary):
                    thumbnail_path = f"images/{slug}_mid.png"
                else:
                    # If none exist: fallback to "images/logo.png"
                    thumbnail_path = "images/logo.png"
                    fallback_count += 1
        
        # Set the thumbnail field (do not touch other fields)
        story["thumbnail"] = thumbnail_path
        updated_count += 1
    
    # Write the updated stories.json back to disk
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    
    # Print summary
    print(f"✅ Thumbnails set for {updated_count} stories ({fallback_count} fallback used).")

if __name__ == "__main__":
    main()