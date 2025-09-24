# build_clean_stories_json.py
import json, re, unicodedata
from pathlib import Path

BASE = Path(__file__).parent
IMAGES_DIR = BASE / "images"
FREE_MD = BASE / "stories" / "Free stories.md"
PREM_MD = BASE / "stories" / "Premium Stories.md"
OUTPUT_JSON = BASE / "stories.json"

def norm_text(s: str) -> str:
    if not s: return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\r\n", "\n")
    return s

def normalize_title(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"')
    s = s.replace("–","-").replace("—","-")
    return s.strip()

def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[’‘]", "'", s)
    s = s.replace("—","-").replace("–","-")
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s or "untitled"

# Robust heading matcher:
# Handles:
#  **Story 12: Title**
#  ### Story 12 - Title
#  Story 12 – Title
#  12. Title
#  12) Title
#  Story 12 Title   (no punctuation)
HEADING_RX = re.compile(
    r"(?im)^[ \t]*(?:\*{0,2})\s*(?:#{0,6}\s*)?"
    r"(?:Story\s+)?(?P<num>\d{1,3})"
    r"(?:[ \t]*[:\-\u2013\u2014\.\)])?"
    r"[ \t]*(?P<title>.+?)\s*(?:\*{0,2})\s*$"
)

def parse_markdown(md_text: str):
    md_text = norm_text(md_text)
    heads = []
    # collect heading line positions
    for m in HEADING_RX.finditer(md_text):
        num = int(m.group("num"))
        title = normalize_title(m.group("title"))
        # filter obviously bad "titles" that are just numbers or empty
        if not title or re.fullmatch(r"\d+", title):
            continue
        heads.append((m.start(), m.end(), num, title))
    heads.sort(key=lambda t: t[0])

    stories = []
    for i, (start, end, num, title) in enumerate(heads):
        body_start = end
        body_end = heads[i+1][0] if i+1 < len(heads) else len(md_text)
        body = md_text[body_start:body_end].strip()
        stories.append({"num": num, "title": title, "text": body})
    # If nothing matched, treat entire file as one story?
    return stories

def pick_images_for_slug(slug: str):
    if not IMAGES_DIR.exists():
        return []
    # strategy:
    # 1) look for exact prefixes: slug_1.png, slug_2.png, slug_3.png
    numbered = []
    for n in (1,2,3):
        for ext in ("png","jpg","jpeg","webp"):
            p = IMAGES_DIR / f"{slug}_{n}.{ext}"
            if p.exists():
                numbered.append(str(p.name))
                break
    if numbered:
        return numbered[:3]
    # 2) fallback: any image that contains the slug token
    cands = [p.name for p in IMAGES_DIR.iterdir() if p.is_file() and slug in p.stem.lower()]
    # prefer sorted stable order
    cands.sort()
    return cands[:3]

def build():
    all_entries = []
    for src_path, premium_flag in [(FREE_MD, False), (PREM_MD, True)]:
        if not src_path.exists():
            continue
        stories = parse_markdown(src_path.read_text(encoding="utf-8", errors="ignore"))
        for s in stories:
            title = s["title"].strip("* ").strip()
            slug = slugify(title)
            images = pick_images_for_slug(slug)
            entry = {
                "slug": slug,
                "title": title,
                "text": s["text"] or "",
                "language": "English",
                "category": "Bedtime",
                "premium": premium_flag,
                "images": images,   # cover/mid/end if available
            }
            all_entries.append(entry)

    # Deduplicate by slug keeping the first with non-empty text
    seen = {}
    for e in all_entries:
        key = e["slug"]
        if key not in seen:
            seen[key] = e
        else:
            if not seen[key]["text"] and e["text"]:
                seen[key] = e
            # merge images if missing
            if not seen[key]["images"] and e["images"]:
                seen[key]["images"] = e["images"]

    # Stable order by title
    final_list = sorted(seen.values(), key=lambda x: x["title"].lower())

    OUTPUT_JSON.write_text(json.dumps(final_list, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Wrote {len(final_list)} stories to {OUTPUT_JSON}")

if __name__ == "__main__":
    build()


