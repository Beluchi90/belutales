#!/usr/bin/env python3
from __future__ import annotations

"""
Normalize collection files using stories.json as the source of truth for titles.

For every story in stories.json:
 - If premium: ensure it appears in Premium/Prenium collection as
       # Title

       <body>
   ending right before the next '# ' heading.
 - If free: ensure it appears in Free Stories.md, or Stories.md if Free is absent.

Existing headings like '**Story 12 - Title**' or '### Story 12: Title' are converted to '# Title'.
Body text is preserved.
"""

import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P_STORIES_JSON = ROOT / "stories.json"
DIR_STORIES = ROOT / "stories"


def _normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"')
    s = s.replace("–","-").replace("—","-")
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def read_story_from_collection(title: str, premium: bool) -> tuple[Path | None, str | None, int | None, int | None]:
    base = DIR_STORIES
    candidates: list[Path] = []
    if premium:
        for name in ["Premium Stories.md", "Prenium Stories.md"]:
            p = base / name
            if p.exists():
                candidates.append(p)
        for p in base.rglob("*Premium*Stories.md"):
            candidates.append(p)
        for p in base.rglob("*Prenium*Stories.md"):
            candidates.append(p)
    else:
        p = base / "Free Stories.md"
        if p.exists():
            candidates.append(p)
        for p in base.rglob("*Free*Stories.md"):
            candidates.append(p)
    if not candidates:
        p = base / "Stories.md"
        if p.exists():
            candidates.append(p)
    if not candidates:
        return None, None, None, None

    norm_title = _normalize_text(title)
    for p in candidates:
        txt = p.read_text(encoding="utf-8", errors="ignore")
        lines = txt.splitlines()
        offs, pos = [], 0
        for ln in lines:
            offs.append(pos)
            pos += len(ln) + 1

        m = re.search(rf"(?m)^#\s*{re.escape(title)}\s*$", txt)
        start_idx = m.start() if m else None
        if start_idx is None:
            for i, ln in enumerate(lines):
                if ln.strip().startswith("#"):
                    core = _normalize_text(re.sub(r"^#+\s*", "", ln).strip())
                    if norm_title and norm_title in core:
                        start_idx = offs[i]
                        break
        if start_idx is None:
            for i, ln in enumerate(lines):
                if norm_title and norm_title in _normalize_text(ln):
                    start_idx = offs[i]
                    break
        if start_idx is None:
            continue

        nl = txt.find("\n", start_idx)
        body_start = nl + 1 if nl != -1 else start_idx
        m2 = re.search(r"(?m)^#\s+", txt[body_start:])
        body_end = body_start + (m2.start() if m2 else len(txt) - body_start)
        body = txt[body_start:body_end]
        return p, body, start_idx, body_end

    return None, None, None, None


def ensure_heading_and_body(file_path: Path, title: str, body: str) -> None:
    desired = f"# {title}\n\n{body.strip()}\n"
    if not file_path.exists():
        file_path.write_text(desired, encoding="utf-8")
        return
    txt = file_path.read_text(encoding="utf-8", errors="ignore")

    # Try to locate any existing block for this title
    norm_title = _normalize_text(title)
    lines = txt.splitlines()
    offs, pos = [], 0
    for ln in lines:
        offs.append(pos)
        pos += len(ln) + 1

    # exact heading
    m = re.search(rf"(?m)^#\s*{re.escape(title)}\s*$", txt)
    start_idx = m.start() if m else None
    if start_idx is None:
        # fuzzy heading variants
        for i, ln in enumerate(lines):
            if ln.strip().startswith("#"):
                core = _normalize_text(re.sub(r"^#+\s*", "", ln))
                # also strip common prefixes like 'story 12: '
                core = re.sub(r"^(?:story|chapter)\s*\d+\s*[:\-\.\)]\s*", "", core)
                if norm_title and norm_title in core:
                    start_idx = offs[i]
                    break

    if start_idx is None:
        # append new block
        new_txt = (txt.rstrip() + "\n\n" + desired) if txt.strip() else desired
        file_path.write_text(new_txt, encoding="utf-8")
        return

    # Replace the block: from heading to next H1
    nl = txt.find("\n", start_idx)
    body_start = nl + 1 if nl != -1 else start_idx
    m2 = re.search(r"(?m)^#\s+", txt[body_start:])
    body_end = body_start + (m2.start() if m2 else len(txt) - body_start)
    new_txt = txt[:start_idx] + desired + txt[body_end:]
    file_path.write_text(new_txt, encoding="utf-8")


def main() -> None:
    if not P_STORIES_JSON.exists():
        print("Missing stories.json")
        return
    data = json.loads(P_STORIES_JSON.read_text(encoding="utf-8"))

    # Load or select destination files
    premium_dest = DIR_STORIES / "Premium Stories.md"
    if not premium_dest.exists():
        p_alt = DIR_STORIES / "Prenium Stories.md"
        premium_dest = p_alt if p_alt.exists() else premium_dest
    free_dest = DIR_STORIES / "Free Stories.md"
    if not free_dest.exists():
        fallback = DIR_STORIES / "Stories.md"
        free_dest = fallback if fallback.exists() else free_dest

    made = 0
    for s in data:
        title = (s.get("title") or "").strip()
        if not title:
            continue
        premium = bool(s.get("premium", False))
        src_file, body, _, _ = read_story_from_collection(title, premium)
        if body is None:
            # If not found anywhere, keep empty body placeholder
            body = ""
        dest = premium_dest if premium else free_dest
        dest.parent.mkdir(parents=True, exist_ok=True)
        ensure_heading_and_body(dest, title, body)
        made += 1

    print(f"Normalized {made} stories into collections.")


if __name__ == "__main__":
    main()


