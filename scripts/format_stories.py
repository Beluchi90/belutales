from __future__ import annotations

import re
from pathlib import Path


def find_markdown_files(base_dirs: list[Path]) -> list[Path]:
    unique_paths: dict[Path, Path] = {}
    for base in base_dirs:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if path.is_file():
                unique_paths[path.resolve()] = path
    # Sort for stable processing order
    markdown_files = sorted(unique_paths.values(), key=lambda p: str(p).lower())
    return markdown_files


def extract_title_and_body_lines(lines: list[str]) -> tuple[str, int]:
    """
    Returns (title, title_line_index).

    Heuristics:
    - Use the first non-empty line as the title line
    - If it starts with '#', strip leading '#'s
    - If it looks like "Story xx: Title", strip the prefix and keep Title
    - Otherwise, use the line as-is
    """
    first_idx = 0
    while first_idx < len(lines) and lines[first_idx].strip() == "":
        first_idx += 1

    if first_idx >= len(lines):
        return ("", -1)

    raw = lines[first_idx].rstrip("\n")
    stripped = raw.strip()

    # Heading case: # Title or ## Title, etc.
    if stripped.startswith("#"):
        title = re.sub(r"^#+\s*", "", stripped).strip()
        return (title, first_idx)

    # Fallback: use the first non-empty line as the title
    return (stripped, first_idx)


def is_horizontal_rule(line: str) -> bool:
    s = line.strip()
    if len(s) < 3:
        return False
    return (
        all(ch == '-' for ch in s)
        or all(ch == '_' for ch in s)
        or all(ch == '*' for ch in s)
    )


def strip_wrapping_markers(paragraph: str) -> str:
    p = paragraph.strip()
    # Strip symmetric wrappers that encompass the entire paragraph
    # Only remove if they appear exactly as wrappers (not internal emphasis)
    # Handle **text** and *text*
    if p.startswith("**") and p.endswith("**") and p.count("**") == 2:
        return p[2:-2].strip()
    if p.startswith("*") and p.endswith("*") and p.count("*") == 2:
        return p[1:-1].strip()
    # Handle __text__ and _text_
    if p.startswith("__") and p.endswith("__") and p.count("__") == 2:
        return p[2:-2].strip()
    if p.startswith("_") and p.endswith("_") and p.count("_") == 2:
        return p[1:-1].strip()
    return paragraph


def normalize_paragraphs(body_lines: list[str]) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    inside_code_fence: bool = False

    def flush_current():
        nonlocal current
        if not current:
            return
        # Join lines into a single paragraph with spaces
        text = " ".join(part.strip() for part in current if part.strip() != "")
        text = strip_wrapping_markers(text)
        if text:
            paragraphs.append(text)
        current = []

    for line in body_lines:
        stripped = line.strip()

        # Toggle code fence state on ``` lines, but preserve inner content as plain text
        if stripped.startswith("```"):
            flush_current()
            inside_code_fence = not inside_code_fence
            continue

        if is_horizontal_rule(line):
            flush_current()
            continue

        if stripped == "":
            flush_current()
            continue

        # Convert headings to plain text by removing leading # markers
        if stripped.startswith("#"):
            stripped = re.sub(r"^#+\s*", "", stripped).strip()
            if stripped == "":
                # If it was only hashes, treat as separator
                flush_current()
                continue

        # Strip a single leading list marker while keeping wording
        m = re.match(r"^([\-*•])\s+(.*)$", stripped)
        if m:
            stripped = m.group(2)

        current.append(stripped)

    flush_current()
    return paragraphs


def clean_story_content(original: str) -> str:
    lines = original.splitlines()

    title, title_idx = extract_title_and_body_lines(lines)

    # Build body lines excluding the title line and any heading lines
    body_source_lines: list[str] = []

    for idx, line in enumerate(lines):
        if idx == title_idx:
            continue
        body_source_lines.append(line)

    paragraphs = normalize_paragraphs(body_source_lines)

    # Ensure a clean H1 title and two newlines before body
    header = f"# {title}" if title else ""
    if paragraphs:
        content = header + "\n\n" + "\n\n".join(paragraphs) + "\n"
    else:
        content = header + ("\n" if header else "")
    return content


def process_files(files: list[Path]) -> int:
    changed_count = 0
    for path in files:
        original_text = path.read_text(encoding="utf-8", errors="ignore")
        cleaned = clean_story_content(original_text)
        if cleaned != original_text:
            path.write_text(cleaned, encoding="utf-8")
        changed_count += 1
    return changed_count


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    stories_root = repo_root / "stories"
    stories_free = stories_root / "free"
    stories_premium = stories_root / "premium"

    files = find_markdown_files([stories_root, stories_free, stories_premium])

    # Exclude index/listing markdown files
    excluded = {
        (stories_root / "Stories.md").resolve(),
        (stories_free / "Free stories.md").resolve(),
        (stories_premium / "Prenium Stories.md").resolve(),
    }
    files = [f for f in files if f.resolve() not in excluded]
    count = process_files(files)
    print(f"Rewritten {count} story files.")


if __name__ == "__main__":
    main()


