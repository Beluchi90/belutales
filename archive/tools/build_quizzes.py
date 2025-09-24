# tools/build_quizzes.py
# Auto-build quizzes.json from stories.json for BeluTales
# - 2–3 MCQs per story
# - Uses title/category/tags/content heuristics
# - Overwrites quizzes.json each run (idempotent)
#
# Run:
#   python tools/build_quizzes.py
#
# Output:
#   quizzes.json in project root

import json, re, unicodedata, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORIES = ROOT / "stories.json"
QUIZZES = ROOT / "quizzes.json"

CATEGORIES = ["Adventure","Bedtime","Friendship","Nature","Fantasy","Other"]

# Setting detectors (simple, child-friendly heuristics)
SETTINGS = {
    "Forest / Nature": ["forest","tree","river","leaf","birds","flower","mountain","wind","woods","meadow","valley","lake","stream"],
    "City / Village":  ["street","market","village","city","shop","school","bus","house","home","town","road","park"],
    "Space":           ["space","planet","rocket","star","moon","astronaut","comet","galaxy","cosmos"],
    "Sea / Ocean":     ["ocean","sea","beach","waves","shell","fish","boat","island","sail"],
    "Castle / Fantasy": ["castle","dragon","fairy","wizard","magic","king","queen","crown","forest of spells","enchant"]
}

def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").lower()
    return "".join(ch for ch in s if not unicodedata.combining(ch))

def _first_name_guess(title: str) -> str:
    """
    Try to pick a kid-friendly 'main character' from the title:
    - first capitalized word not at sentence start punctuation
    - fallback: first non-stopword token
    """
    if not title: return "The hero"
    # Look for capitalized tokens (allow hyphen, apostrophe)
    tokens = re.findall(r"[A-Z][a-zA-Z'\-]{2,}", title)
    if tokens:
        return tokens[0]
    # Fallback: first long token
    parts = re.findall(r"[A-Za-z]{3,}", title)
    return parts[0].title() if parts else "The hero"

def _infer_setting(text: str) -> str:
    t = _norm(text)
    best, best_hits = None, 0
    for setting, keys in SETTINGS.items():
        hits = sum(1 for k in keys if k in t)
        if hits > best_hits:
            best, best_hits = setting, hits
    return best or "City / Village"

def _distractors_theme(correct: str) -> list:
    pool = [c for c in CATEGORIES if c != correct]
    random.shuffle(pool)
    return pool[:2]

def _distractors_names(correct: str) -> list:
    # make playful, child-safe distractors
    bank = ["Milo","Zara","Timo","Luna","Aria","Kofi","Ada","Nala","Ravi","Nora","Kai","Sami","Imani","Zuri"]
    # avoid duplicates and the correct name
    picks = []
    for n in bank:
        if n != correct and n not in picks:
            picks.append(n)
        if len(picks) == 2: break
    return picks or ["Milo","Zara"]

def _distractors_setting(correct: str) -> list:
    pool = [s for s in SETTINGS.keys() if s != correct]
    random.shuffle(pool)
    return pool[:2]

def _kid_lesson_guess(text: str) -> str:
    t = _norm(text)
    if any(w in t for w in ["share","help","kind","care","friend","together","team"]):
        return "Kindness"
    if any(w in t for w in ["brave","courage","fear","scared","bold"]):
        return "Bravery"
    if any(w in t for w in ["learn","listen","practice","try","patience","calm"]):
        return "Learning"
    if any(w in t for w in ["dream","imagine","magic","wonder"]):
        return "Imagination"
    return "Kindness"

def build_quiz_for_story(s: dict) -> list:
    title = (s.get("title") or "Untitled").strip()
    slug = s.get("slug") or _norm(title).replace(" ","-")
    category = (s.get("category") or "Other").title()
    content = (s.get("content") or "")
    tags = s.get("tags") or []
    bag = " ".join([title, category, " ".join(tags), content])

    # Q1: Theme (Category)
    theme_correct = category if category in CATEGORIES else "Other"
    t_d1, t_d2 = _distractors_theme(theme_correct)
    q1_options = [theme_correct, t_d1, t_d2]
    random.shuffle(q1_options)
    q1 = {
        "question": "What is this story mostly about?",
        "options": q1_options,
        "answer": theme_correct,
        "explanation": f"The main theme matches “{theme_correct}”."
    }

    # Q2: Character (from title)
    name = _first_name_guess(title)
    n_d1, n_d2 = _distractors_names(name)
    q2_options = [name, n_d1, n_d2]
    random.shuffle(q2_options)
    q2 = {
        "question": "Who seems to be the main character?",
        "options": q2_options,
        "answer": name,
        "explanation": f"The title hints that {name} is the main character."
    }

    # Q3: Setting (optional but we’ll include it for better engagement)
    setting = _infer_setting(bag)
    s_d1, s_d2 = _distractors_setting(setting)
    q3_options = [setting, s_d1, s_d2]
    random.shuffle(q3_options)
    q3 = {
        "question": "Where does most of the story happen?",
        "options": q3_options,
        "answer": setting,
        "explanation": f"Words in the story point to a {setting.lower()} setting."
    }

    # (Optional) Q4: Lesson (keep it simple and positive)
    lesson = _kid_lesson_guess(bag)
    l_distractors = [x for x in ["Speed","Robots","Treasure"] if x != lesson]
    q4_options = [lesson] + l_distractors[:2]
    random.shuffle(q4_options)
    q4 = {
        "question": "What is an important lesson in this story?",
        "options": q4_options,
        "answer": lesson,
        "explanation": f"The story encourages {lesson.lower()}."
    }

    # Keep 2–3 questions to match your UI spec
    # (Choose 3 for stronger engagement)
    return [q1, q2, q3]  # or [q1, q2, q3, q4] if you want 4

def main():
    if not STORIES.exists():
        raise SystemExit("stories.json not found. Place it in the project root.")
    stories = json.loads(STORIES.read_text(encoding="utf-8"))
    out = {}

    # Stable randomness per run
    random.seed(1337)

    count = 0
    for s in stories:
        slug = s.get("slug")
        if not slug:
            # build a slug fallback if missing
            title = (s.get("title") or "untitled").strip().lower()
            slug = re.sub(r"[^a-z0-9]+","-", title).strip("-") or "untitled"
        out[slug] = build_quiz_for_story(s)
        count += 1

    QUIZZES.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✔ Built quizzes for {count} stories → {QUIZZES}")

if __name__ == "__main__":
    main()
