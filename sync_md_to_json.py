# ---------- sync_md_to_json.py (start) ----------
import json, re, unicodedata, os, sys
from pathlib import Path

BASE = Path(__file__).parent
IMAGES_DIR = BASE / "images"
OUT_JSON = BASE / "stories.json"
BACKUP_JSON = BASE / "stories.json.backup"

# Include both root and subfolder variants
SOURCES = [
    (BASE / "stories" / "Free stories.md", "free"),
    (BASE / "stories" / "Premium Stories.md", "premium"),
    (BASE / "stories" / "free" / "Free stories.md", "free"),
    (BASE / "stories" / "premium" / "Premium Stories.md", "premium"),
    (BASE / "stories" / "Stories.md", "free"),
]

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return s

def slugify(title: str) -> str:
    s = norm(title).lower()
    s = s.replace("'","'").replace("'","'").replace(""", '"').replace(""", '"')
    s = s.replace("–","-").replace("—","-")
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s or "untitled"

# Multiple relaxed heading formats to catch all variations:
PATTERNS = [
    # **Story 12: Title** (standard format)
    r"""^[ \t]*(?:\*\*)?\s*Story\s+(?P<num>\d{1,3})[ \t]*[:\-\u2013\u2014\.\)]?[ \t]*(?P<title>[^*\n]+?)(?:\*\*)?\s*$""",
    
    # **\*\*Story 12: Title\*\*** (with literal backslashes)
    r"""^[ \t]*(?:\*\*)?\s*\\\*\*Story\s+(?P<num>\d{1,3})[ \t]*[:\-\u2013\u2014\.\)]?[ \t]*(?P<title>[^*\n]+?)\\\*\*\s*$""",
    
    # **12: Title** or **12 - Title** (just number, no "Story" word)
    r"""^[ \t]*(?:\*\*)?\s*(?P<num>\d{1,3})[ \t]*[:\-\u2013\u2014\.\)]?[ \t]*(?P<title>[^*\n]+?)(?:\*\*)?\s*$""",
    
    # # Title (markdown H1 headings)
    r"""^[ \t]*#\s+(?P<title>[^\n]+?)\s*$""",
    
    # ### Title (markdown H3 headings)
    r"""^[ \t]*###\s+(?P<title>[^\n]+?)\s*$""",
]

COMPILED = [re.compile(p, re.IGNORECASE|re.MULTILINE) for p in PATTERNS]

def find_headings_lines(lines):
    """Return list of (line_index, num:int, title:str)."""
    heads = []
    for i, ln in enumerate(lines):
        # Look for "Story" followed by a number
        if 'Story' in ln and any(char.isdigit() for char in ln):
            # Extract number and title using a simple approach
            match = re.search(r'Story\s+(\d+)[:\-\s]*(.+)', ln, re.IGNORECASE)
            if match:
                num_str = match.group(1)
                title = match.group(2).strip(' *\t\\')  # Remove asterisks, spaces, tabs, and backslashes
                try:
                    num = int(num_str)
                    if title and not re.match(r'^\d+\s*$', title):
                        heads.append((i, num, title))
                except:
                    continue
    
    # Keep first occurrence per number
    first_by_num = {}
    for i, n, t in heads:
        if n not in first_by_num:
            first_by_num[n] = (i, n, t)
    
    return [first_by_num[k] for k in sorted(first_by_num.keys())]

def split_stories_from_text(text: str):
    # Normalize and unescape common literal escapes like \*
    text = norm(text)
    text = text.replace(r"\*", "*")
    lines = text.splitlines()
    headings = find_headings_lines(lines)
    
    stories = []
    if not headings:
        return stories
    
    # Extract story bodies between headings
    for idx, (line_i, num, title) in enumerate(headings):
        start = line_i + 1
        end = headings[idx+1][0] if idx+1 < len(headings) else len(lines)
        body = "\n".join(lines[start:end]).strip()
        
        # Clean up the body text
        body = re.sub(r'---\s*', '', body)  # Remove separators
        body = body.strip()
        
        stories.append((num, title, body))
    
    return stories

def guess_images_by_title(story_title: str):
    """Find all images for a story that start with the story title or its slug version"""
    images = []
    
    if not story_title or not IMAGES_DIR.exists():
        return images
    
    # Normalize the story title for file matching
    # Remove special characters and normalize spaces
    normalized_title = re.sub(r'[^\w\s-]', '', story_title)
    normalized_title = re.sub(r'\s+', ' ', normalized_title).strip()
    
    # Convert title to slug format (like the image filenames)
    title_slug = slugify(story_title)
    
    # Search for various patterns
    search_patterns = [
        f"{normalized_title}*",           # Exact title match
        f"{normalized_title.replace(' ', '_')}*",  # Underscore version
        f"{title_slug}*",                 # Slug version (most important)
        f"{title_slug.replace('-', '_')}*"  # Slug with underscores
    ]
    
    # Add variations for common naming patterns
    # Handle singular/plural variations
    if title_slug.endswith('s'):
        # Try without the trailing 's' (common case like "spaces" -> "space")
        title_slug_singular = title_slug[:-1]
        search_patterns.extend([
            f"{title_slug_singular}*",    # Singular version
            f"{title_slug_singular.replace('-', '_')}*"  # Singular with underscores
        ])
    
    # Handle common variations like "the" prefix
    if title_slug.startswith('the-'):
        title_without_the = title_slug[4:]  # Remove "the-" prefix
        search_patterns.extend([
            f"{title_without_the}*",      # Without "the" prefix
            f"{title_without_the.replace('-', '_')}*"
        ])
    
    for pattern in search_patterns:
        found_files = list(IMAGES_DIR.glob(f"{pattern}"))
        for img_file in found_files:
            if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp', '.gif']:
                img_path = str(img_file)
                if img_path not in images:  # Avoid duplicates
                    images.append(img_path)
    
    # Sort images alphabetically for consistent order
    images.sort()
    
    return images

def build():
    all_items = []
    
    # Process each markdown file in the stories folder
    stories_dir = BASE / "stories"
    if stories_dir.exists():
        for md_file in stories_dir.rglob("*.md"):
            if md_file.is_file():
                print(f"Processing {md_file.name}...")
                try:
                    # Read the entire markdown file content
                    full_content = md_file.read_text(encoding="utf-8", errors="ignore")
                    
                    # Extract stories from the content
                    parts = split_stories_from_text(full_content)
                    print(f"  Found {len(parts)} stories in {md_file.name}")
                    
                    # Determine if this is a premium story based on folder structure or filename
                    # Check if file is in premium folder or has "Premium" in filename
                    is_premium = (
                        "premium" in md_file.parts or  # Check folder path
                        "Premium" in md_file.name or   # Check filename
                        md_file.parent.name == "premium"  # Explicit folder check
                    )
                    
                    for num, title, body in parts:
                        # Find images that match the story title
                        images = guess_images_by_title(title)
                        
                        item = {
                            "title": title.strip(),
                            "content": body.strip() or "",  # Store just the story content
                            "images": images,
                            "is_premium": is_premium
                        }
                        all_items.append(item)
                        
                except Exception as e:
                    print(f"  Error processing {md_file.name}: {e}")
                    continue
    
    # If no stories found in individual files, fall back to the original method
    if not all_items:
        print("No individual markdown files found, processing combined files...")
        for src, tier in SOURCES:
            if not src.exists():
                continue
            print(f"Processing {src.name}...")
            txt = src.read_text(encoding="utf-8", errors="ignore")
            parts = split_stories_from_text(txt)
            print(f"  Found {len(parts)} stories in {src.name}")
            
            for num, title, body in parts:
                # Find images that match the story title
                images = guess_images_by_title(title)
                
                item = {
                    "title": title.strip(),
                    "content": body.strip() or "",  # Store the story body
                    "images": images,
                    "is_premium": tier == "premium"
                }
                all_items.append(item)

    # Sort by title to maintain consistent order
    all_items.sort(key=lambda x: x["title"])

    # Backup existing JSON
    if OUT_JSON.exists():
        try:
            OUT_JSON.replace(BACKUP_JSON)
            print(f"Backed up existing {OUT_JSON.name} to {BACKUP_JSON.name}")
        except Exception as e:
            print(f"Warning: Could not backup existing file: {e}")

    # Write with proper UTF-8 encoding and indentation
    OUT_JSON.write_text(
        json.dumps(all_items, ensure_ascii=False, indent=2), 
        encoding="utf-8"
    )
    print(f"Wrote {len(all_items)} stories to {OUT_JSON.name}")
    
    # Show some stats
    print(f"  Total stories: {len(all_items)}")
    
    # Count stories with images
    with_images = len([item for item in all_items if item["images"]])
    total_images = sum(len(item["images"]) for item in all_items if item["images"])
    print(f"  Stories with images: {with_images}")
    print(f"  Total images found: {total_images}")
    
    # Show some examples of image counts
    if with_images > 0:
        image_counts = [len(item["images"]) for item in all_items if item["images"]]
        print(f"  Average images per story: {total_images / with_images:.1f}")
        print(f"  Stories with 1 image: {len([c for c in image_counts if c == 1])}")
        print(f"  Stories with 2+ images: {len([c for c in image_counts if c >= 2])}")
        
        # Show some examples of image matching
        print("\n  Image matching examples:")
        for item in all_items[:3]:  # Show first 3 stories
            if item["images"]:
                print(f"    '{item['title']}': {len(item['images'])} images")
                for img in item["images"][:2]:  # Show first 2 images
                    print(f"      - {img}")
            else:
                print(f"    '{item['title']}': No images found")
                # Debug: show what the script is looking for
                title_slug = slugify(item['title'])
                print(f"      Looking for: {title_slug}*")
                # Check if any files exist with that pattern
                if IMAGES_DIR.exists():
                    found_files = list(IMAGES_DIR.glob(f"{title_slug}*"))
                    if found_files:
                        print(f"      Found files: {[f.name for f in found_files]}")
                    else:
                        print(f"      No files found with pattern: {title_slug}*")

if __name__ == "__main__":
    build()
# ---------- sync_md_to_json.py (end) ----------


