from __future__ import annotations
import json
from pathlib import Path

BASE = Path(__file__).parent
STORIES_DIR = BASE / "stories"
OUT_JSON = BASE / "stories.json"

FREE_DIR = STORIES_DIR / "free"
PREM_DIR = STORIES_DIR / "premium"


def read_story_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def scan_folder(folder: Path, premium: bool) -> list[dict]:
    items: list[dict] = []
    if not folder.exists():
        return items
    for md in sorted(folder.glob("*.md")):
        txt = read_story_file(md).strip()
        # Title: first non-empty line; strip leading '# '
        title = ""
        for ln in txt.splitlines():
            if not ln.strip():
                continue
            if ln.lstrip().startswith("# "):
                title = ln.lstrip()[2:].strip()
            else:
                title = ln.strip()
            break
        # Body: everything after the title line
        body = txt
        if title:
            lines = txt.splitlines()
            body_start = 0
            for i, ln in enumerate(lines):
                if ln.lstrip().startswith("# ") and ln.lstrip()[2:].strip() == title:
                    body_start = i + 1
                    break
                if ln.strip() and not ln.lstrip().startswith("# "):
                    body_start = i + 1
                    break
            body = "\n".join(lines[body_start:]).strip()

        items.append({
            "slug": md.stem,
            "title": title or md.stem,
            "text": body,
            "language": "English",
            "category": "",
            "premium": premium,
            "images": [],
        })
    return items


def main() -> None:
    stories = []
    stories += scan_folder(FREE_DIR, premium=False)
    stories += scan_folder(PREM_DIR, premium=True)

    OUT_JSON.write_text(json.dumps(stories, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(stories)} stories to {OUT_JSON}")


if __name__ == "__main__":
    main()
