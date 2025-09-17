import os, re, json, datetime

def slugify(title):
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s

JSON_PATH = "stories.json"
IMAGES_DIR = "images"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    stories = json.load(f)

backup = f"stories.backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(backup, "w", encoding="utf-8") as f:
    json.dump(stories, f, ensure_ascii=False, indent=2)

updated = 0
missing = []
for story in stories:
    if "thumbnail" not in story:
        slug = slugify(story.get("title","untitled"))
        candidate = os.path.join(IMAGES_DIR, f"{slug}_1.png")
        if os.path.exists(candidate):
            story["thumbnail"] = candidate.replace("\\","/")
            updated += 1
        else:
            missing.append(story.get("title", "Untitled"))

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(stories, f, ensure_ascii=False, indent=2)

print(f"Thumbnails added to {updated} stories. Backup saved as {backup}")
if missing:
    print("Missing thumbnails for:")
    for title in missing:
        print(f"  - {title}")
