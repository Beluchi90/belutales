import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stories_file = os.path.join(BASE_DIR, "stories.json")
images_dir = os.path.join(BASE_DIR, "images")

with open(stories_file, "r", encoding="utf-8") as f:
    stories = json.load(f)

def normalize(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

available_images = os.listdir(images_dir)
available_set = {img.lower(): img for img in available_images}

fixed = []

for story in stories:
    title_norm = normalize(story["title"])
    expected = {
        "cover_image": f"{title_norm}_1.png",
        "mid_image": f"{title_norm}_mid.png",
        "end_image": f"{title_norm}_end.png"
    }
    for key, filename in expected.items():
        if filename in available_set:
            story[key] = available_set[filename]
            fixed.append((story["title"], key, filename))

with open(stories_file, "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=2, ensure_ascii=False)

print(f"✔ Updated {len(fixed)} image references")
for t, k, fimg in fixed:
    print(f"  {t} → {k} = {fimg}")