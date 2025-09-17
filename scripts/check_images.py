# scripts/check_images.py
import os
import json
from PIL import Image, UnidentifiedImageError

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STORIES_JSON = os.path.join(ROOT, "stories.json")
IMAGES_DIR = os.path.join(ROOT, "images")
REPORT_PATH = os.path.join(ROOT, "image_check_report.json")

def read_stories(path):
    import json
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_open_image(path):
    try:
        with Image.open(path) as im:
            im.verify()  # verify catches many corrupts
        return True, None
    except UnidentifiedImageError as e:
        return False, f"UnidentifiedImageError: {e}"
    except Exception as e:
        return False, f"Exception: {type(e).__name__}: {e}"

def main():
    report = {
        "summary": {
            "stories_checked": 0,
            "total_image_paths_checked": 0,
            "missing_files": 0,
            "invalid_images": 0,
            "small_files": 0
        },
        "details": []
    }

    if not os.path.exists(STORIES_JSON):
        print(f"Could not find stories.json at {STORIES_JSON}")
        return

    stories = read_stories(STORIES_JSON)
    report['summary']['stories_checked'] = len(stories)

    # fields to check per story - update if your schema has different names
    image_fields = ["cover_image", "mid_image", "end_image", "thumbnail"]

    for sidx, story in enumerate(stories):
        story_id = story.get("id") or story.get("slug") or story.get("title") or f"index_{sidx}"
        entry = {"story_index": sidx, "story_id": story_id, "checked_images": []}
        for field in image_fields:
            img_name = story.get(field)
            if not img_name:
                # skip if not provided
                continue
            report['summary']['total_image_paths_checked'] += 1
            img_path = os.path.join(IMAGES_DIR, img_name) if not os.path.isabs(img_name) else img_name
            img_result = {"field": field, "img_name": img_name, "img_path": img_path}
            if not os.path.exists(img_path):
                img_result["status"] = "missing"
                report['summary']['missing_files'] += 1
            else:
                try:
                    size = os.path.getsize(img_path)
                    img_result["size_bytes"] = size
                    if size < 1024:  # less than 1KB probably invalid
                        img_result["status"] = "too_small"
                        report['summary']['small_files'] += 1
                    else:
                        ok, err = safe_open_image(img_path)
                        if ok:
                            img_result["status"] = "ok"
                        else:
                            img_result["status"] = "invalid_image"
                            img_result["error"] = err
                            report['summary']['invalid_images'] += 1
                except Exception as e:
                    img_result["status"] = "error_checking"
                    img_result["error"] = f"{type(e).__name__}: {e}"
                    report['summary']['invalid_images'] += 1
            entry["checked_images"].append(img_result)
        report["details"].append(entry)

    # extra: list all files that exist in images/ but not referenced in stories (optional)
    referenced = set()
    for d in report['details']:
        for c in d['checked_images']:
            referenced.add(c['img_name'])
    all_files = []
    if os.path.exists(IMAGES_DIR):
        all_files = [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(os.path.join(IMAGES_DIR, f))]
    unreferenced = [f for f in all_files if f not in referenced and f.lower() != "placeholder.png"]
    report['unreferenced_images'] = unreferenced

    # write report
    with open(REPORT_PATH, "w", encoding="utf-8") as rf:
        json.dump(report, rf, indent=2, ensure_ascii=False)

    print(f"Report written to {REPORT_PATH}")
    print("Summary:")
    print(json.dumps(report['summary'], indent=2))

if __name__ == "__main__":
    main()
