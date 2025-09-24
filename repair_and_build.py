import re, json, unicodedata
from pathlib import Path

BASE = Path(".")
FREE = BASE/"stories"/"Free stories.md"
PREM = BASE/"stories"/"Premium Stories.md"

def read_big_md():
    txt = ""
    if FREE.exists():
        txt += FREE.read_text(encoding="utf-8", errors="ignore") + "\n"
    if PREM.exists():
        txt += PREM.read_text(encoding="utf-8", errors="ignore")
    if not txt.strip():
        raise SystemExit("No markdown found in stories/Free stories.md or stories/Premium Stories.md")
    return txt

def normalize_text(t: str) -> str:
    t = unicodedata.normalize("NFKC", t)
    # unescape \* -> * so **\*\*Story …\*\*** becomes **Story …**
    t = t.replace(r"\*", "*")
    # normalize quotes/dashes
    t = (t.replace("’","'").replace("‘","'")
           .replace("“",'"').replace("”",'"')
           .replace("–","-").replace("—","-"))
    # normalize newlines
    t = t.replace("\r\n","\n").replace("\r","\n")
    return t

# very forgiving heading recognizers
RXES = [
    re.compile(r"^\s*(?:\*\*|__)?\s*Story\s+(?P<num>\d{1,3})\s*[:\-.\)]\s*(?P<title>.+?)\s*(?:\*\*|__)?\s*$", re.I|re.M),
    re.compile(r"^\s*(?:\*\*|__)?\s*(?P<num>\d{1,3})\s*[:\-.\)]\s*(?P<title>.+?)\s*(?:\*\*|__)?\s*$", re.I|re.M),
    re.compile(r"^\s*(?:\*\*|__)?\s*Story\s+(?P<num>\d{1,3})\s+(?P<title>.+?)\s*(?:\*\*|__)?\s*$", re.I|re.M),
]

def standardize_headings(t: str) -> str:
    """Rewrite any recognized heading line to **Story N: Title** (exact)."""
    lines = t.split("\n")
    out = []
    for ln in lines:
        std = None
        for rx in RXES:
            m = rx.match(ln)
            if m:
                num = int(m.group("num"))
                title = m.group("title").strip()
                # guard against false positives like a naked number
                if title and not re.fullmatch(r"\d+", title):
                    std = f"**Story {num}: {title}**"
                    break
        out.append(std if std else ln)
    return "\n".join(out)

def parse_stories(t: str):
    # find headings again after standardization
    rx_head = re.compile(r"^\s*\*\*Story\s+(?P<num>\d{1,3})\s*:\s*(?P<title>.+?)\*\*\s*$", re.M)
    heads = [(m.start(), m.end(), int(m.group("num")), m.group("title").strip()) for m in rx_head.finditer(t)]
    if not heads:
        raise SystemExit("No standardized headings found after repair.")
    # keep first occurrence per number
    first = {}
    for h in heads:
        n = h[2]
        if n not in first:
            first[n] = h
    heads = [first[k] for k in sorted(first.keys())]

    stories = []
    for i,(s,e,num,title) in enumerate(heads):
        body_start = e
        body_end = heads[i+1][0] if i+1 < len(heads) else len(t)
        body = t[body_start:body_end].strip()
        # drop leading H1 echo if present
        bl = body.splitlines()
        if bl and bl[0].lstrip("# ").strip().lower() == title.lower():
            body = "\n".join(bl[1:]).lstrip()
        slug = re.sub(r"[^a-z0-9\s-]","",title.lower())
        slug = re.sub(r"\s+","-",slug).strip("-") or f"story-{num}"
        stories.append({
            "order": num,
            "title": title,
            "slug": slug,
            "language": "English",
            "category": "Bedtime",
            "favorite": False,
            "text": body if body.strip() else "(No text yet.)",
            "images": []
        })
    stories.sort(key=lambda s: s["order"])
    return stories

# ---- run
raw = read_big_md()
norm = normalize_text(raw)
fixed = standardize_headings(norm)
stories = parse_stories(fixed)

out = BASE/"stories.json"
if out.exists():
    (BASE/"stories.backup.json").write_text(out.read_text(encoding="utf-8"), encoding="utf-8")

out.write_text(json.dumps(stories, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"? Wrote stories.json with {len(stories)} stories.")
