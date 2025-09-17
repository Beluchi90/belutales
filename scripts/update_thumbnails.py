# scripts/update_thumbnails.py
import os, re, json, glob, copy, datetime
JSON_PATH = "stories.json"
IMAGES_DIR = "images"

def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)        # keep letters, numbers, spaces, hyphens
    s = re.sub(r"\s+", "-", s.strip())        # spaces -> hyphen
    s = re.sub(r"-+", "-", s)                 # collapse multiple hyphens
    return s

def find_thumbnail(title: str, filename_hint: str | None) -> str | None:
    # Prefer explicit filename if present
    if filename_hint:
        candidate = os.path.join(IMAGES_DIR, filename_hint)
        if os.path.exists(candidate):
            return filename_hint

    base = filename_hint or slugify(title)
    # Try common patterns using _1 with common extensions
    exts = ("png", "jpg", "jpeg", "webp")
    candidates = [os.path.join(IMAGES_DIR, f"{base}_1.{ext}") for ext in exts]

    # Also try any file that starts with the slug and ends with _1.*
    for ext in exts:
        candidates.extend(glob.glob(os.path.join(IMAGES_DIR, f"{base}*_1.{ext}")))

    for c in candidates:
        if os.path.exists(c):
            return os.path.basename(c)
    return None

def main():
    if not os.path.exists(JSON_PATH):
        raise SystemExit(f"stories.json not found at {JSON_PATH}")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        stories = json.load(f)

    # Backup ORIGINAL before we touch it
    backup_name = f"stories.backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_name, "w", encoding="utf-8") as b:
        json.dump(stories, b, ensure_ascii=False, indent=2)

    updated = 0
    missing = []

    for story in stories:
        # Use any existing helpful fields
        title = story.get("title") or story.get("name") or ""
        explicit_thumb = story.get("thumbnail")  # keep if valid
        filename_hint = explicit_thumb or story.get("filename") or story.get("id")

        thumb = find_thumbnail(title, filename_hint)
        if thumb:
            story["thumbnail"] = thumb
            updated += 1
        else:
            # leave story as-is but record missing
            if not story.get("thumbnail"):
                missing.append(title)

    with open(JSON_PATH, "w", encoding="utf-8") as out:
        json.dump(stories, out, ensure_ascii=False, indent=2)

    print(f"Thumbnails set/validated for {updated} stories.")
    if missing:
        print("No match for:")
        for t in missing:
            print(" -", t)

if __name__ == "__main__":
    main()
