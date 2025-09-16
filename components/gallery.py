# components/gallery.py — colorful category bar + gallery tiles
import html
import streamlit as st
from collections import Counter

from utils.media import (
    emoji_for_category, slugify, first_cover, clean_title, image_src_for_html
)

# Pastel swatches for each category (tweak freely)
PASTELS = {
    "All":                    {"bg1":"#66d3ff","bg2":"#b6e7ff","bd":"#b6e7ff","fg":"#063a5a"},
    "Bedtime":                {"bg1":"#d8e2ff","bg2":"#f0f4ff","bd":"#e6ecff","fg":"#0e2466"},
    "Animal Adventures":      {"bg1":"#ffecd1","bg2":"#ffe1b0","bd":"#ffe5bd","fg":"#5a3100"},
    "Magic & Fantasy":        {"bg1":"#ffd6f0","bg2":"#ffe9f8","bd":"#ffe0f5","fg":"#4a1641"},
    "Friendship & Kindness":  {"bg1":"#ffd1e8","bg2":"#ffe3f1","bd":"#ffd8ee","fg":"#45122f"},
    "Exploration & Discovery":{"bg1":"#d6f8ff","bg2":"#e9fbff","bd":"#dcf7ff","fg":"#0a2f4a"},
    "Nature & Seasons":       {"bg1":"#c9ffe9","bg2":"#eafff6","bd":"#d6fff1","fg":"#083d2c"},
    "Life Lessons":           {"bg1":"#fff3c4","bg2":"#fff7dc","bd":"#fff0b8","fg":"#4a3b00"},
    "Other":                  {"bg1":"#aaf7ff","bg2":"#dcfbff","bd":"#dcfbff","fg":"#0a3d44"},
}

def _chip_html(cat: str, active: bool, count: int|None=None) -> str:
    pal = PASTELS.get(cat, PASTELS["Other"])
    cls = "bt-chip-link active" if active else "bt-chip-link"
    badge = f'<span class="bt-chip-count">{count}</span>' if count is not None else ""
    return (
        f'<a class="{cls}" href="?cat={html.escape(cat)}" '
        f'style="--bg1:{pal["bg1"]};--bg2:{pal["bg2"]};--bd:{pal["bd"]};--fg:{pal["fg"]}">'
        f'<span class="em">{emoji_for_category(cat)}</span> {html.escape(cat)} {badge}</a>'
    )

def render_search_and_chips(current_cat: str, categories: list, *, story_list_for_counts: list|None=None) -> str:
    """Search bar + colorful category chips.
    Pass story_list_for_counts (list of all stories after search filter) to show counts per category.
    """
    st.markdown('<div class="bt-search-caption">Find a story:</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="bt-search-wrap">', unsafe_allow_html=True)
        s1, s2 = st.columns([7.2, 2.8])
        out = {"txt": ""}
        def _on_change(): out["txt"]=st.session_state.get("bt_search","")
        with s1:
            st.text_input("Search", key="bt_search", value=st.session_state.get("bt_search",""),
                          placeholder="Search by title, author, or tag…",
                          label_visibility="collapsed", on_change=_on_change)
        with s2:
            if st.button("Search", use_container_width=True):
                out["txt"]=st.session_state.get("bt_search","")
        st.markdown("</div>", unsafe_allow_html=True)

    # Build counts per category if we were given a filtered story list
    counts: dict[str,int] = {}
    if story_list_for_counts is not None:
        c = Counter([s.get("category","Other") for s in story_list_for_counts])
        counts = {"All": len(story_list_for_counts)}
        for cat in categories:
            if cat == "All": continue
            counts[cat] = c.get(cat, 0)

    # Render colorful chip row
    chips=[]
    ordered = ["All"] + [c for c in categories if c != "All"]
    for cat in ordered:
        is_active = (cat == current_cat)
        chips.append(_chip_html(cat, is_active, counts.get(cat) if counts else None))
    st.markdown(f'<div class="bt-catbar">{"".join(chips)}</div>', unsafe_allow_html=True)
    return out["txt"]

def render_gallery(stories: list, all_categories: list, current_cat: str, favorites: set):
    st.caption(f"📚 {current_cat} • {len(stories)} stor{'y' if len(stories)==1 else 'ies'}")
    st.markdown('<div class="bt-grid">', unsafe_allow_html=True)
    for s in stories:
        title = clean_title(s.get("title","Untitled"))
        slug = s.get("slug") or slugify(title)
        href=f'?cat={current_cat}&pick={slug}'
        cover_path = first_cover(s)
        src = image_src_for_html(cover_path) if cover_path else ""

        st.markdown(f'<a class="bt-tile" href="{href}">', unsafe_allow_html=True)
        if src:
            st.markdown(f'<img class="bt-cover" alt="" src="{src}"/>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="bt-cover-emoji">✨</div>', unsafe_allow_html=True)
        st.markdown('<div class="bt-meta">', unsafe_allow_html=True)
        st.markdown(f'<div class="bt-title">{html.escape(title)}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bt-chip">{emoji_for_category(s.get("category","Other"))} {html.escape(s.get("category","Other"))}</div>', unsafe_allow_html=True)
        st.markdown('</div></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
