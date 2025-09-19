import os
import json

def main():
    # Load stories.json
    stories_path = "stories.json"
    images_dir = "images"
    
    if not os.path.exists(stories_path):
        print(f"Error: {stories_path} not found")
        return
    
    if not os.path.exists(images_dir):
        print(f"Error: {images_dir} directory not found")
        return
    
    with open(stories_path, 'r', encoding='utf-8') as f:
        stories = json.load(f)
    
    print("🔍 Checking image references in stories.json...")
    print("=" * 60)
    
    total_references = 0
    missing_count = 0
    existing_count = 0
    
    # Check each story
    for story in stories:
        title = story.get("title", "Untitled")
        
        # Collect all image field values
        image_fields = {
            "cover_image": story.get("cover_image", ""),
            "mid_image": story.get("mid_image", ""),
            "end_image": story.get("end_image", ""),
            "thumbnail": story.get("thumbnail", "")
        }
        
        story_has_issues = False
        
        # Check each image field
        for field_name, filename in image_fields.items():
            if filename:  # Only check if field has a value
                total_references += 1
                image_path = os.path.join(images_dir, filename)
                
                if os.path.exists(image_path):
                    existing_count += 1
                    if not story_has_issues:
                        # Only print story title once if there are issues
                        pass
                else:
                    if not story_has_issues:
                        print(f"\n📖 Story: {title}")
                        story_has_issues = True
                    print(f"   ❌ Missing {field_name}: {filename}")
                    missing_count += 1
    
    # Print summary report
    print("\n" + "=" * 60)
    print("📊 SUMMARY REPORT")
    print("=" * 60)
    print(f"Total image references checked: {total_references}")
    print(f"✅ Existing images: {existing_count}")
    print(f"❌ Missing images: {missing_count}")
    
    if missing_count == 0:
        print("\n🎉 All image references are valid!")
    else:
        print(f"\n⚠️  Found {missing_count} missing image files")
        print("💡 Run scripts/fix_image_references.py to fix mismatches")

if __name__ == "__main__":
    main()
