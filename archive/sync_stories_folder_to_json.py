import os
import json

STORIES_FOLDER = "stories"
STORIES_JSON_PATH = "stories.json"
BACKUP_PATH = "stories.json.backup"

# Step 1: Backup existing JSON
if os.path.exists(STORIES_JSON_PATH):
    with open(STORIES_JSON_PATH, "r", encoding="utf-8") as f:
        current_data = json.load(f)
    with open(BACKUP_PATH, "w", encoding="utf-8") as backup:
        json.dump(current_data, backup, ensure_ascii=False, indent=2)
    print("✅ Backup created as stories.json.backup")
else:
    current_data = []

# Step 2: Read .md files in stories folder
story_files = sorted(os.listdir(STORIES_FOLDER))

new_stories = []
for filename in story_files:
    if filename.endswith(".md"):
        filepath = os.path.join(STORIES_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Assume first line = title, rest = story
        lines = content.splitlines()
        title = lines[0].replace("Story ", "").strip() if lines else filename
        story_body = "\n".join(lines[1:]).strip()

        new_stories.append({
            "title": title,
            "content": story_body
        })

# Step 3: Save to JSON
with open(STORIES_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(new_stories, f, ensure_ascii=False, indent=2)

print(f"✅ {len(new_stories)} stories saved to {STORIES_JSON_PATH}")
