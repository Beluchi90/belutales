import json, random
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="BeluTales (Simple)", page_icon="✨", layout="wide")

# -------- Load stories only from stories.json --------
def load_stories():
    with open("stories.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for s in data:
        # defaults + normalized slug
        title = s.get("title", "Untitled").strip()
        slug = s.get("slug") or title.lower().replace(" ", "-")
        s["title"] = title
        s["slug"] = slug
        s.setdefault("language", "English")
        s.setdefault("category", "")
        s.setdefault("text", "(No text yet.)")
        s.setdefault("quiz", [])
    return data

stories = load_stories()

# -------- Session index (which story to show) --------
if "story_idx" not in st.session_state:
    st.session_state.story_idx = 0

def clamp_idx():
    if stories:
        st.session_state.story_idx = max(0, min(st.session_state.story_idx, len(stories)-1))
    else:
        st.session_state.story_idx = 0

clamp_idx()

# -------- UI: render exactly ONE story --------
def render_current_story(stories, idx):
    n = len(stories)
    if n == 0:
        st.warning("No stories found in stories.json")
        return
    idx = max(0, min(idx, n-1))
    s = stories[idx]

    # Header
    st.markdown(f"## Story {idx+1} of {n} — {s.get('title','Untitled')}")
    cap = f"BeluTales • {s.get('language','English')}"
    if s.get("category"):
        cap += f" • {s['category']}"
    st.caption(cap)

    # Images (cover, mid, end)
    def img(slug, i):
        p = Path("images") / f"{slug}_{i}.png"
        return str(p) if p.exists() else None

    cols = st.columns(3)
    labels = ["Cover", "Mid", "End"]
    for i, (c, label) in enumerate(zip(cols, labels), start=1):
        with c:
            p = img(s["slug"], i)
            if p:
                st.image(p, use_container_width=True)
            else:
                st.markdown("*(missing)*")
            st.caption(label)

    # Text (safe formatting)
    st.markdown("### Story")
    text = s.get("text","(No text yet.)").replace("\n","<br>")
    st.markdown(f"<div class='story-text'>{text}</div>", unsafe_allow_html=True)

render_current_story(stories, st.session_state.story_idx)

# -------- Navigation (only updates index) --------
col_prev, col_rand, col_next = st.columns([1,1,1])
with col_prev:
    if st.button("◀ Previous"):
        st.session_state.story_idx = (st.session_state.story_idx - 1) % len(stories)
with col_rand:
    if st.button("🔀 Random"):
        st.session_state.story_idx = random.randrange(len(stories)) if stories else 0
with col_next:
    if st.button("Next ▶"):
        st.session_state.story_idx = (st.session_state.story_idx + 1) % len(stories)
