import json, unicodedata, re
from pathlib import Path

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"')
    s = s.replace("–","-").replace("—","-")
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

base = Path(".")
stories = json.loads((base/"stories.json").read_text(encoding="utf-8"))
expected = {norm(s["title"]) for s in stories}

txt = ""
free_md = base/"stories"/"Free stories.md"
prem_md = base/"stories"/"Premium Stories.md"
if free_md.exists():
    txt += free_md.read_text(encoding="utf-8", errors="ignore") + "\n"
if prem_md.exists():
    txt += prem_md.read_text(encoding="utf-8", errors="ignore")

txt = unicodedata.normalize("NFKC", txt).replace(r"\*", "*")

rx = re.compile(r'(?im)^\s*["\']?\s*\**\s*story\s+(\d{1,3})\s*[:\-\u2013\u2014\)]\s*(.+?)\s*\**\s*["\']?\s*$')
found = {norm(m.group(2)) for m in rx.finditer(txt)}

missing = expected - found
print("Expected:", len(expected), "Found:", len(found), "Missing:", len(missing))
print("Missing examples:", sorted(list(missing))[:15])
