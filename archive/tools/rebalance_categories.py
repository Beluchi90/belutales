"""
tools/rebalance_categories.py
Rebalance categories for BeluTales so your gallery isn’t 95% “Bedtime”.

USAGE (from your project root, next to app.py):
  python tools/rebalance_categories.py
  python tools/rebalance_categories.py --write stories_rebalanced.json
  python tools/rebalance_categories.py --overrides category_overrides.json --write stories_rebalanced.json

What it does:
- Loads stories.json, creates a backup stories.backup.json (first run only).
- Assigns categories using a richer taxonomy + keyword rules.
- Applies optional slug-based overrides from category_overrides.json.
- Writes new JSON (default: stories_rebalanced.json) and prints a summary.

Taxonomy used (7 buckets):
  "Bedtime"                🌙
  "Animal Adventures"      🐾
  "Magic & Fantasy"        ✨
  "Friendship & Kindness"  ❤️
  "Exploration & Discovery"🚀
  "Nature & Seasons"       🌳
  "Life Lessons"           🎯

Tip:
- You can create 'category_overrides.json' like: { "slug-of-a-story": "Animal Adventures", ... }
- Slug = kebab-case of title. This tool preserves existing slugs or generates if missing.
"""

import json, re, unicodedata, argparse, shutil
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
STORIES = ROOT / "stories.json"
BACKUP = ROOT / "stories.backup.json"

TARGETS = [
    "Bedtime", "Animal Adventures", "Magic & Fantasy", "Friendship & Kindness",
    "Exploration & Discovery", "Nature & Seasons", "Life Lessons"
]

# ---------- helpers ----------
def nfkd(s:str)->str:
    return unicodedata.normalize("NFKD", s or "")

def slugify(text: str) -> str:
    t = nfkd((text or "").strip().lower())
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "untitled"

def normalize(s:str)->str:
    return "".join(ch for ch in nfkd((s or "").lower()) if not unicodedata.combining(ch))

def kw_in(txt:str, *words)->bool:
    return any(w in txt for w in words)

# Keyword rules (ordered by priority)
def classify(title:str, content:str, tags:list[str])->str:
    t = normalize(f"{title} {' '.join(tags or [])} {content}")
    # 1) Bedtime (keep small but meaningful)
    if kw_in(t, "sleep", "sleepy", "bedtime", "yawn", "pajama", "night-night", "lights out", "lullaby"):
        return "Bedtime"
    # 2) Magic & Fantasy
    if kw_in(t, "magic", "magical", "fairy", "dragon", "unicorn", "wizard", "spell", "castle", "mermaid"):
        return "Magic & Fantasy"
    # 3) Animal Adventures
    if kw_in(t, "lion", "tiger", "bear", "owl", "bird", "bunny", "cat", "dog", "fox", "wolf",
                "whale", "dolphin", "frog", "giraffe", "elephant", "zebra", "monkey", "penguin"):
        return "Animal Adventures"
    # 4) Friendship & Kindness
    if kw_in(t, "friend", "friends", "kind", "share", "help", "team", "together", "bully", "include", "caring"):
        return "Friendship & Kindness"
    # 5) Exploration & Discovery (space, travel, “first time”, learning something new)
    if kw_in(t, "adventure", "explore", "journey", "quest", "discover", "invention", "museum", "map", "rocket", "space", "planet"):
        return "Exploration & Discovery"
    # 6) Nature & Seasons
    if kw_in(t, "forest", "tree", "river", "leaf", "mountain", "ocean", "sea", "rain", "wind", "snow",
                "spring", "summer", "autumn", "fall", "winter", "garden", "flower", "sunshine", "storm"):
        return "Nature & Seasons"
    # 7) Life Lessons (habits, emotions, chores, growth)
    if kw_in(t, "learn", "lesson", "brave", "fear", "worry", "patience", "practice", "tidy", "homework", "apologize", "promise"):
        return "Life Lessons"
    # Fallback: try to keep balance by nudging generic “night/star/moon” away from Bedtime when no sleep words
    if kw_in(t, "night", "moon", "star", "starlight", "twilight"):
        return "Magic & Fantasy"
    # Final fallback
    return "Exploration & Discovery"

def load_overrides(path: Path|None)->dict[str,str]:
    if not path or not path.exists(): return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Only allow valid target categories
    cleaned = {}
    for slug, cat in data.items():
        if cat in TARGETS:
            cleaned[str(slug)] = cat
    return cleaned

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", default=str(ROOT / "stories_rebalanced.json"),
                    help="Output JSON (won't overwrite original unless you point it to stories.json).")
    ap.add_argument("--overrides", default="",
                    help="Optional JSON {slug: category} to force placement.")
    args = ap.parse_args()

    if not STORIES.exists():
        print(f"[!] stories.json not found at {STORIES}")
        return

    # First run backup
    if not BACKUP.exists():
        shutil.copyfile(STORIES, BACKUP)
        print(f"[✓] Backed up original to {BACKUP}")

    with open(STORIES, "r", encoding="utf-8") as f:
        stories = json.load(f)

    overrides = load_overrides(Path(args.overrides)) if args.overrides else {}

    before = Counter()
    after  = Counter()
    changes = 0

    # Pass 1 — ensure slug & count before
    for s in stories:
        s["title"] = s.get("title") or "Untitled"
        s["slug"]  = s.get("slug") or slugify(s["title"])
        s["category"] = s.get("category") or ""
        before[s["category"] or "Uncategorized"] += 1

    # Pass 2 — assign categories
    for s in stories:
        slug = s["slug"]
        if slug in overrides:
            new_cat = overrides[slug]
        else:
            new_cat = classify(s.get("title",""), s.get("content",""), s.get("tags",[]))
        if s.get("category") != new_cat:
            changes += 1
        s["category"] = new_cat
        after[new_cat] += 1

    # Write new file
    out_path = Path(args.write)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    print(f"[✓] Wrote {out_path}")

    # Print summary
    print("\n--- BEFORE ---")
    for k,v in sorted(before.items(), key=lambda x:(-x[1], x[0])):
        print(f"{k:24s} {v:4d}")
    print("\n--- AFTER ---")
    for k in TARGETS:
        print(f"{k:24s} {after[k]:4d}")
    print(f"\nReassigned: {changes} / {len(stories)} stories")

    # Balance hint
    total = sum(after.values())
    print("\nGoal mix guide (approximate % of total):")
    mix = {
        "Bedtime": 10, "Animal Adventures": 18, "Magic & Fantasy": 18,
        "Friendship & Kindness": 14, "Exploration & Discovery": 18,
        "Nature & Seasons": 12, "Life Lessons": 10
    }
    for k,p in mix.items():
        target = round(total * p/100)
        print(f"  {k:24s} ~{p:2d}%  (~{target} stories)")

    print("\nTip: If you want to force placements for a few slugs, create a 'category_overrides.json' like:")
    print('{\n  "nina-and-the-night-sky": "Magic & Fantasy",\n  "ruby-and-the-glow-worms": "Nature & Seasons"\n}')
    print("Then re-run with:  python tools/rebalance_categories.py --overrides category_overrides.json --write stories_rebalanced.json")
    print("\nFinally, point your app to stories_rebalanced.json (or replace stories.json when you’re happy).")

if __name__ == "__main__":
    main()
