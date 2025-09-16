"""
tools/verify_images.py
Check every story's images and produce a CSV report.
Optionally auto-fill missing images[] when safe.

Usage:
  python tools/verify_images.py
  python tools/verify_images.py --report out/report.csv
  python tools/verify_images.py --report out/report.csv --autofill --write stories_autofilled.json

What it does:
- Loads stories.json from the project root (same folder as app.py)
- For each story:
    * Attempts to resolve up to 3 images via utils.media.story_images()
    * Reports if none/partial/all images resolve
    * Suggests guesses found by slug
- Outputs a CSV with columns:
    slug,title,category,provided_fields,found_count,found_paths,guessed_paths,needs_attention
- With --autofill: adds an "images" list for stories that have none but good guesses, and writes a new JSON.
"""

import argparse, csv, os, json
from pathlib import Path

# Import the same helpers your app uses
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.media import load_stories, story_images, _guess_by_slug, clean_title  # type: ignore

STORIES_PATH = ROOT / "stories.json"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default=str(ROOT / "image_check_report.csv"),
                        help="Path to write the CSV report.")
    parser.add_argument("--autofill", action="store_true",
                        help="If set, auto-fill images[] for stories that have none but valid guesses.")
    parser.add_argument("--write", default=str(ROOT / "stories_autofilled.json"),
                        help="Where to write the updated stories JSON when using --autofill.")
    args = parser.parse_args()

    if not STORIES_PATH.exists():
        print(f"[!] Cannot find {STORIES_PATH}")
        return

    stories = load_stories(str(STORIES_PATH))
    rows = []
    changes = 0

    for s in stories:
        title = clean_title(s.get("title","Untitled"))
        slug = s.get("slug") or ""
        cat  = s.get("category","")

        provided_fields = []
        for k in ("images","cover","image_1","image_2","image_3"):
            if s.get(k): provided_fields.append(k)

        found = story_images(s)  # uses robust resolver
        found_count = len([p for p in found if p])

        # independent guesses (without mutating story)
        guesses = _guess_by_slug(slug)

        needs_attention = "YES" if found_count == 0 else ("PARTIAL" if found_count < 3 else "OK")

        rows.append({
            "slug": slug,
            "title": title,
            "category": cat,
            "provided_fields": ";".join(provided_fields) if provided_fields else "",
            "found_count": found_count,
            "found_paths": ";".join(found),
            "guessed_paths": ";".join(guesses),
            "needs_attention": needs_attention,
        })

        # Optional autofill: only when no images provided and we have at least one valid guess
        if args.autofill:
            has_any_image_field = bool(s.get("images") or s.get("cover") or s.get("image_1") or s.get("image_2") or s.get("image_3"))
            if not has_any_image_field and guesses:
                s["images"] = guesses[:3]
                changes += 1

    # Write CSV report
    out_csv = Path(args.report)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"[✓] Wrote report: {out_csv}")
    ok = sum(1 for r in rows if r["needs_attention"] == "OK")
    partial = sum(1 for r in rows if r["needs_attention"] == "PARTIAL")
    bad = sum(1 for r in rows if r["needs_attention"] == "YES")
    print(f"    OK: {ok}   PARTIAL: {partial}   MISSING: {bad}")

    if args.autofill:
        out_json = Path(args.write)
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(stories, f, ensure_ascii=False, indent=2)
        print(f"[✓] Wrote autofilled JSON: {out_json}   (stories modified: {changes})")

if __name__ == "__main__":
    main()
