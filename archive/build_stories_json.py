import os
import re
import json

FREE_MD = os.path.join("stories", "free", "Free stories.md")
PREMIUM_MD = os.path.join("stories", "premium", "Prenium Stories.md")
IMAGES_DIR = os.path.join("assets", "images")
OUTPUT_JSON = "stories.json"

def get_image_filename(title):
    base = title.lower()
    base = re.sub(r"[^a-z0-9 ]", "", base)
    base = base.replace("  ", " ").strip()
    for fname in os.listdir(IMAGES_DIR):
        name, ext = os.path.splitext(fname)
        if ext.lower() not in [".png", ".jpg", ".jpeg"]:
            continue
        img_base = name.lower()
        img_base = re.sub(r"[^a-z0-9 ]", "", img_base)
        img_base = img_base.replace("  ", " ").strip()
        if img_base == base:
            return os.path.join(IMAGES_DIR, fname).replace("\\", "/")
    return ""

def parse_stories(md_path, premium=False):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    story_blocks = re.split(r"\*\*Story \d+:|\*\*\\\*\\\*Story \d+: ", content)
    stories = []
    for block in story_blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        for i, line in enumerate(lines):
            if line.strip():
                raw_title = line.strip().strip("*").strip()
                break
        else:
            continue
        title = raw_title
        story_lines = []
        for l in lines[i+1:]:
            if l.strip() == "---":
                break
            story_lines.append(l)
        story_text = "\n".join(story_lines).strip()
        image_path = get_image_filename(title)
        stories.append({
            "title": title,
            "content": story_text,
            "image": image_path,
            "premium": premium
        })
    return stories

def main():
    free_stories = parse_stories(FREE_MD, premium=False)
    premium_stories = parse_stories(PREMIUM_MD, premium=True)
    all_stories = free_stories + premium_stories
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_stories, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(all_stories)} stories saved to {OUTPUT_JSON} ({len(free_stories)} free, {len(premium_stories)} premium)")

if __name__ == "__main__":
    main()