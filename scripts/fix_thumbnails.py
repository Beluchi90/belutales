import os, re, json, datetime

JSON_PATH = "stories.json"
IMAGES_DIR = "images"

def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s

def main():
    if not os.path.exists(JSON_PATH):
        raise SystemExit(f"{JSON_PATH} not found")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        stories = json.load(f)

    backup = f"stories.backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)

    updated = 0
    for story in stories:
        if "thumbnail" not in story:
            slug = slugify(story.get("title","untitled"))
            story["thumbnail"] = f"{slug}_1.png"
            updated += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)

    print(f"Added thumbnails to {updated} stories.")
    print(f"Backup saved as {backup}")

if __name__ == "__main__":
    main()
