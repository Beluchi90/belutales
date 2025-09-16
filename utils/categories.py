import json
from pathlib import Path
from collections import Counter

def load_stories_json(path="stories.json"):
    p = Path(path)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))

def category_counts(stories):
    raw_cats = [(s.get("category") or "General").strip() or "General" for s in stories]
    
    # Normalize categories - handle emoji prefixes and merge similar categories
    normalized = []
    for cat in raw_cats:
        if "Self-Discovery" in cat:
            normalized.append("Self-Discovery")
        elif "Dreams" in cat:
            normalized.append("Dreams")
        elif "Adventure" in cat:
            normalized.append("Adventure")
        elif "Family" in cat:
            normalized.append("Family")
        else:
            normalized.append("General")
    
    c = Counter(normalized)
    # Return a dict in a stable order
    order = ["Self-Discovery", "Dreams", "Adventure", "Family", "General"]
    return {k: c.get(k, 0) for k in order}
