import os
import json
import re

FREE_MD_PATH = os.path.join('stories', 'free', 'Free stories.md')
IMAGES_DIR = os.path.join('assets', 'images')
OUTPUT_JSON = 'stories.json'

def find_image(title):
    # Try to match image file by title (case-insensitive, ignore spaces and punctuation)
    base = title.lower().replace('**', '').replace(':', '').replace('-', ' ').replace('_', ' ').strip()
    for fname in os.listdir(IMAGES_DIR):
        if not fname.lower().endswith('.png'):
            continue
        img_base = os.path.splitext(fname)[0].lower().replace('-', ' ').replace('_', ' ').strip()
        if img_base == base:
            return os.path.join(IMAGES_DIR, fname)
    return None

def main():
    with open(FREE_MD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split on '**Story X:'
    story_blocks = re.split(r'\*\*Story \d+:', content)
    stories = []
    for block in story_blocks:
        block = block.strip()
        if not block:
            continue
        # First non-empty line is the title (ending with **)
        lines = block.split('\n')
        for i, line in enumerate(lines):
            if line.strip():
                raw_title = line.strip().strip('*').strip()
                break
        else:
            continue
        title = raw_title
        story_text = '\n'.join([l for l in lines[i+1:] if l.strip()])
        image_path = find_image(title)
        stories.append({
            'title': title,
            'content': story_text,
            'image': image_path if image_path else ''
        })
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(stories)} stories saved to {OUTPUT_JSON}")

if __name__ == '__main__':
    main() 