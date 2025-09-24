#!/usr/bin/env python3
"""
Rebuilds ALL individual story .md files from the big collection markdowns,
using stories.json for titles/slugs and premium/free routing.

- Looks for:
    stories/premium/*Premium*Stories.md   (case-insensitive, any “premium/prenium” spelling)
    stories/free/*Free*Stories.md         (case-insensitive)
    stories/Stories.md                    (fallback source if needed)

- For each story in stories.json:
    * Finds its text in the matching collection file (approximate, forgiving match)
    * Writes/overwrites stories/premium/<slug>.md or stories/free/<slug>.md:
        # Title

        <body>

- Prints a summary + any stories not found.
"""

from __future__ import annotations

import json
import re
import unicodedata
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P_STORIES_JSON = ROOT / "stories.json"
DIR_STORIES = ROOT / "stories"
DIR_FREE = DIR_STORIES / "free"
DIR_PREM = DIR_STORIES / "premium"
DIR_FREE.mkdir(parents=True, exist_ok=True)
DIR_PREM.mkdir(parents=True, exist_ok=True)


def find_collection(patterns: list[str]) -> str | None:
    """Return text of the first existing file matching any of the glob patterns (case-insensitive)."""
    for pat in patterns:
        for p in DIR_STORIES.rglob(pat):
            try:
                return p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass
    return None


# try multiple spellings/placements
PREMIUM_MD = find_collection([
    "*Premium*Stories.md", "*Prenium*Stories.md", "*premium*stories.md", "*prenium*stories.md",
])
FREE_MD = find_collection([
    "*Free*Stories.md", "*free*stories.md",
])
FALLBACK_MD = (DIR_STORIES / "Stories.md")
FALLBACK_TEXT = FALLBACK_MD.read_text(encoding="utf-8", errors="ignore") if FALLBACK_MD.exists() else ""


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    # strip common prefixes like "story 12 -", "## story 5: "
    s = re.sub(r"^[#>\*\s\-]*story\s*\d+\s*[:\-\.\)]\s*", "", s, flags=re.I)
    # keep only letters/numbers/space
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def build_line_index(md_text: str) -> tuple[list[int], list[str]]:
    """Return (offsets, lines) with offsets[i] = start char index of line i."""
    if not md_text:
        return [], []
    lines = md_text.splitlines()
    offsets, pos = [], 0
    for ln in lines:
        offsets.append(pos)
        pos += len(ln) + 1  # \n
    return offsets, lines


def map_title_positions(md_text: str, titles: list[str]) -> dict[str, int]:
    """Find approximate positions for each title in md_text. Returns {title: start_index}."""
    if not md_text:
        return {}
    offsets, lines = build_line_index(md_text)
    wanted = {normalize(t): t for t in titles if t}
    found: dict[str, int] = {}

    # scan every line; if normalized line contains normalized title, record earliest match
    for i, ln in enumerate(lines):
        core = re.sub(r"^[#>\*\s\-]*story\s*\d+\s*[:\-\.\)]\s*", "", ln, flags=re.I)
        key_line = normalize(core)
        if not key_line:
            continue
        for k_norm, original in list(wanted.items()):
            if k_norm and k_norm in key_line and original not in found:
                found[original] = offsets[i]
        if len(found) == len(wanted):
            break
    return found


def slice_body(md_text: str, start_pos: int, next_pos: int | None) -> str:
    body_start = start_pos
    # skip the heading line itself
    # find first newline after start_pos
    nl = md_text.find("\n", start_pos)
    if nl != -1:
        body_start = nl + 1
    body_end = next_pos if next_pos is not None else len(md_text)
    body = md_text[body_start:body_end].strip()
    return body


def next_after(lst: list[tuple[int, str]], pos: int) -> int | None:
    for p, _ in lst:
        if p > pos:
            return p
    return None


def write_story(path: Path, title: str, body: str) -> None:
    content = f"# {title}\n\n{body.strip()}\n"
    path.write_text(content, encoding="utf-8")


def main() -> None:
    if not P_STORIES_JSON.exists():
        print("[X] Missing stories.json")
        sys.exit(1)

    data = json.loads(P_STORIES_JSON.read_text(encoding="utf-8"))

    # Partition titles by premium flag
    titles_prem = [s.get("title", "").strip() for s in data if s.get("premium")]
    titles_free = [s.get("title", "").strip() for s in data if not s.get("premium")]
    all_titles = [s.get("title", "").strip() for s in data]

    # Choose source text for each group
    prem_src = PREMIUM_MD or FALLBACK_TEXT
    free_src = FREE_MD or FALLBACK_TEXT

    # Build title position maps
    pos_prem = map_title_positions(prem_src or "", titles_prem)
    pos_free = map_title_positions(free_src or "", titles_free)
    pos_fallback = map_title_positions(FALLBACK_TEXT or "", all_titles) if FALLBACK_TEXT else {}

    # For slicing, we need the positions of all titles in each src to compute "next_pos"
    # Create sorted list of (pos, title)
    prem_pos_list = sorted([(p, t) for t, p in pos_prem.items()])
    free_pos_list = sorted([(p, t) for t, p in pos_free.items()])
    fallback_pos_list = sorted([(p, t) for t, p in pos_fallback.items()]) if pos_fallback else []

    made, missing = 0, []
    for s in data:
        title = (s.get("title") or "").strip()
        slug = (s.get("slug") or "").strip()
        premium = bool(s.get("premium", False))
        if not title or not slug:
            continue

        # Pick primary source group
        src_text = prem_src if premium else free_src
        pos_map = pos_prem if premium else pos_free
        pos_list = prem_pos_list if premium else free_pos_list

        start_pos = pos_map.get(title)
        nxt_pos = None
        if start_pos is not None:
            nxt_pos = next_after(pos_list, start_pos)
        else:
            # Try fallback source
            if title in pos_fallback:
                src_text = FALLBACK_TEXT
                start_pos = pos_fallback[title]
                nxt_pos = next_after(fallback_pos_list, start_pos)

        if start_pos is None:
            missing.append(title)
            continue

        body = slice_body(src_text or "", start_pos, nxt_pos)

        out_path = (DIR_PREM / f"{slug}.md") if premium else (DIR_FREE / f"{slug}.md")
        write_story(out_path, title, body)
        made += 1

    print(f"Wrote {made} stories.")
    if missing:
        print(f"Missing ({len(missing)}):")
        for t in missing:
            print(f" - {t}")


if __name__ == "__main__":
    main()



