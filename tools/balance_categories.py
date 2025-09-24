import json, re, shutil
from pathlib import Path

CAT_ORDER = ["Self-Discovery", "Dreams", "Adventure", "Family", "General"]

# Lightweight keyword hints to bias round-robin for better fits (optional)
HINTS = {
    "Self-Discovery": [r"\b(brave|learn|believe|courage|grow|kind|discover|confiden|fear)\b"],
    "Dreams":         [r"\b(star|moon|night|dream|sleep|bedtime|sky|nightfall|twinkle)\b"],
    "Adventure":      [r"\b(quest|journey|forest|ocean|dragon|treasure|explore|map|pirate|mountain)\b"],
    "Family":         [r"\b(mama|papa|grandma|grandpa|sister|brother|home|family)\b"],
}

def choose_category(title: str, rr_idx: int):
    t = title.lower()
    # Try hints first (skip General)
    for cat in CAT_ORDER[:-1]:
        pats = HINTS.get(cat, [])
        for pat in pats:
            if re.search(pat, t):
                return cat
    # Fallback: round-robin (skip General until last)
    cat_cycle = CAT_ORDER[:-1]  # no "General" in the even spread
    return cat_cycle[rr_idx % len(cat_cycle)]

def balance(path: Path, dry_run=False):
    if not path.exists():
        raise FileNotFoundError(f"Stories JSON not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("stories.json must be a list of story objects")

    # Backup
    bkp = path.with_suffix(".backup.before_balance.json")
    shutil.copy2(path, bkp)

    # Keep counts for report
    before = {}
    for s in data:
        c = (s.get("category") or "General").strip() or "General"
        before[c] = before.get(c, 0) + 1

    # Collect candidates (currently General or missing)
    candidates = [s for s in data if (s.get("category") is None) or (s.get("category","").strip()=="" ) or (s.get("category")=="General")]
    fixed = [s for s in data if s not in candidates]  # already classified specifically

    rr_idx = 0
    reassigned = 0
    for s in candidates:
        title = s.get("title") or ""
        # If it already has a non-General category, keep it
        cat = (s.get("category") or "").strip()
        if cat and cat != "General":
            continue
        new_cat = choose_category(title, rr_idx)
        s["category"] = new_cat
        rr_idx += 1
        reassigned += 1

    after = {}
    for s in data:
        c = (s.get("category") or "General").strip() or "General"
        after[c] = after.get(c, 0) + 1

    report = {
        "file": str(path),
        "backup": str(bkp),
        "total": len(data),
        "before_counts": before,
        "reassigned_general": reassigned,
        "after_counts": after,
    }

    if not dry_run:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return report

if __name__ == "__main__":
    # Default path; update if your file lives elsewhere
    target = Path("stories.json")
    rep = balance(target, dry_run=False)
    print(json.dumps(rep, indent=2))
