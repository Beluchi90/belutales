from __future__ import annotations
import json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STORIES_JSON = ROOT / "stories.json"
STORIES_MD = ROOT / "stories" / "Stories.md"   # optional source
DIR_FREE = ROOT / "stories" / "free"
DIR_PREM = ROOT / "stories" / "premium"
DIR_FREE.mkdir(parents=True, exist_ok=True)
DIR_PREM.mkdir(parents=True, exist_ok=True)

def normalize(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"')
    s = s.replace("–","-").replace("—","-")
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def find_title_pos(text: str, title: str, start_from: int = 0) -> int:
    key = normalize(title)
    for m in re.finditer(r"(?m)^.*$", text[start_from:]):
        line = m.group()
        if not line.strip():
            continue
        line_core = re.sub(r"^[#>\*\s-]*story\s*\d+\s*[:\-\.\)]\s*", "", line, flags=re.I)
        line_norm = normalize(line_core)
        if key and key in line_norm:
            return start_from + m.start()
    return -1

def slice_from_md(md: str, title: str) -> str | None:
    pos = find_title_pos(md, title, 0)
    if pos == -1:
        return None
    lines = md[pos:].splitlines()
    # drop heading line
    k = 0
    while k < len(lines) and not lines[k].strip():
        k += 1
    if k < len(lines):
        k += 1
    body = "\n".join(lines[k:]).strip()
    return body or None

def main():
    if not STORIES_JSON.exists():
        print(f"[X] Not found: {STORIES_JSON}")
        return

    md_text = STORIES_MD.read_text(encoding="utf-8") if STORIES_MD.exists() else ""

    data = json.loads(STORIES_JSON.read_text(encoding="utf-8"))

    # Existing slugs so we DON'T overwrite files you already have
    existing = {p.stem for p in DIR_FREE.glob("*.md")}
    existing |= {p.stem for p in DIR_PREM.glob("*.md")}

    made = 0
    tried = 0
    for s in data:
        title = (s.get("title") or "").strip()
        slug = (s.get("slug") or "").strip()
        premium = bool(s.get("premium", False))
        if not title or not slug:
            continue
        if slug in existing:
            continue

        tried += 1
        body = slice_from_md(md_text, title) if md_text else None
        if not body:
            body = "(No text yet.)"

        folder = DIR_PREM if premium else DIR_FREE
        out = folder / f"{slug}.md"
        out.write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
        print(f"Created: {out}")
        made += 1

    print(f"✅ Done. Created {made} missing files (checked {tried}).")

if __name__ == "__main__":
    main()

