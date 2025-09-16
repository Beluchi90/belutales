import json
import os
from pathlib import Path

def check_image_assets():
    """
    Check if all image files referenced in stories.json exist in the images folder.
    """
    
    # Get the current directory (belutales folder)
    current_dir = Path.cwd()
    images_folder = current_dir / "images"
    
    print(f"Checking image assets in: {images_folder}")
    print("=" * 60)
    
    # Check if images folder exists
    if not images_folder.exists():
        print(f"❌ Images folder not found: {images_folder}")
        return
    
    # Load stories.json
    stories_file = current_dir / "stories.json"
    if not stories_file.exists():
        print(f"❌ stories.json not found: {stories_file}")
        return
    
    try:
        with open(stories_file, 'r', encoding='utf-8') as f:
            stories = json.load(f)
    except Exception as e:
        print(f"❌ Error loading stories.json: {e}")
        return
    
    print(f"Loaded {len(stories)} stories from stories.json")
    print()
    
    # Track results
    stories_with_all_images = 0
    stories_with_missing_images = 0
    missing_files = []
    
    # Check each story's images
    for i, story in enumerate(stories, 1):
        title = story.get('title', f'Story {i}')
        cover_image = story.get('cover_image', '')
        mid_image = story.get('mid_image', '')
        end_image = story.get('end_image', '')
        
        # Check if all three image fields exist
        if not all([cover_image, mid_image, end_image]):
            print(f"❌ Story {i}: '{title}' - Missing image fields in JSON")
            stories_with_missing_images += 1
            continue
        
        # Check if image files exist
        cover_exists = (images_folder / cover_image).exists()
        mid_exists = (images_folder / mid_image).exists()
        end_exists = (images_folder / end_image).exists()
        
        if cover_exists and mid_exists and end_exists:
            print(f"✅ Story {i}: '{title}' - All images found")
            stories_with_all_images += 1
        else:
            print(f"❌ Story {i}: '{title}' - Missing images:")
            if not cover_exists:
                missing_file = f"images/{cover_image}"
                print(f"   - {missing_file}")
                missing_files.append(missing_file)
            if not mid_exists:
                missing_file = f"images/{mid_image}"
                print(f"   - {missing_file}")
                missing_files.append(missing_file)
            if not end_exists:
                missing_file = f"images/{end_image}"
                print(f"   - {missing_file}")
                missing_files.append(missing_file)
            stories_with_missing_images += 1
    
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total stories checked: {len(stories)}")
    print(f"✅ Stories with all images: {stories_with_all_images}")
    print(f"❌ Stories with missing images: {stories_with_missing_images}")
    
    if missing_files:
        print(f"\nMissing files ({len(missing_files)} total):")
        # Remove duplicates and sort
        unique_missing = sorted(list(set(missing_files)))
        for missing_file in unique_missing:
            print(f"  - {missing_file}")
    
    # Calculate percentage
    if len(stories) > 0:
        percentage = (stories_with_all_images / len(stories)) * 100
        print(f"\nAsset completion rate: {percentage:.1f}%")
    
    return {
        'total_stories': len(stories),
        'stories_with_all_images': stories_with_all_images,
        'stories_with_missing_images': stories_with_missing_images,
        'missing_files': list(set(missing_files))
    }

if __name__ == "__main__":
    check_image_assets()
