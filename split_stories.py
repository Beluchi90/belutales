from __future__ import annotations
import re
from pathlib import Path

BASE = Path(__file__).parent
STORIES_DIR = BASE / "stories"
FREE_MD = STORIES_DIR / "Free stories.md"
PREM_MD = STORIES_DIR / "Premium Stories.md"
OUT_FREE = STORIES_DIR / "free"
OUT_PREM = STORIES_DIR / "premium"

OUT_FREE.mkdir(parents=True, exist_ok=True)
OUT_PREM.mkdir(parents=True, exist_ok=True)

# Detect titles by lines starting with '#' (markdown headers) OR starting with 'Story'
TITLE_RX = re.compile(r"^(?:\s*#|\s*Story)\b", re.IGNORECASE)


def split_to_folder(source_md: Path, out_dir: Path) -> int:
    if not source_md.exists():
        return 0
    text = source_md.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    stories: list[list[str]] = []
    current: list[str] = []

    for ln in lines:
        if TITLE_RX.match(ln):
            # start of a new story
            if current:
                stories.append(current)
                current = []
        current.append(ln)
    if current:
        stories.append(current)

    # Write files Story_1.md, Story_2.md, ...
    count = 0
    for idx, block in enumerate(stories, start=1):
        content = "\n".join(block).strip() + "\n"
        (out_dir / f"Story_{idx}.md").write_text(content, encoding="utf-8")
        count += 1
    return count


def main() -> None:
    free_count = split_to_folder(FREE_MD, OUT_FREE)
    prem_count = split_to_folder(PREM_MD, OUT_PREM)
    print(f"Split {free_count} free stories and {prem_count} premium stories.")


if __name__ == "__main__":
    main()
