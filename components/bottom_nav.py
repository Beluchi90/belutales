# components/bottom_nav.py — sticky bottom dock (Home • Categories • Settings)
import html
import streamlit as st
from utils.state import set_qp
from utils.media import emoji_for_category

PASTELS = {
    "All":       {"bg1":"#2b7fff","bg2":"#6bd3ff","bd":"#6bd3ff","fg":"#06213f"},
    "Adventure": {"bg1":"#ffb84d","bg2":"#ffe38a","bd":"#ffdf7a","fg":"#3f2606"},
    "Bedtime":   {"bg1":"#89a2ff","bg2":"#c1d0ff","bd":"#b8c8ff","fg":"#0e1c5a"},
    "Friendship":{"bg1":"#ff7fb6","bg2":"#ffc1de","bd":"#ffb3d8","fg":"#3f0e2a"},
    "Nature":    {"bg1":"#28e3a5","bg2":"#7fffd3","bd":"#7fffd3","fg":"#063c2c"},
    "Fantasy":   {"bg1":"#a988ff","bg2":"#d6c2ff","bd":"#ccb7ff","fg":"#1f0e5a"},
    "Other":     {"bg1":"#a6ffe7","bg2":"#d3fff4","bd":"#c2fff0","fg":"#0b3f38"},
}

def render_bottom_nav(current_cat: str, categories: list, stories: list, favorites: set):
    st.markdown('<div class="bt-dock">', unsafe_allow_html=True)

    left, mid, right = st.columns([1,2,1])
    with left:
        if st.button("🏠 Home", key="dock_home", use_container_width=True):
            set_qp(cat=current_cat, pick=None, quiz=None, _merge=False)

    with mid:
        chips=[]
        for c in categories:
            pal=PASTELS.get(c,PASTELS["Other"])
            chips.append(
                f'<a class="bt-chip-link" href="?cat={html.escape(c)}" '
                f'style="--bg1:{pal["bg1"]};--bg2:{pal["bg2"]};--bd:{pal["bd"]};--fg:{pal["fg"]}">'
                f'{emoji_for_category(c)} {html.escape(c)}</a>'
            )
        st.markdown(f'<div style="display:flex;gap:.45rem;overflow-x:auto;padding:.2rem .1rem;">{"".join(chips)}</div>', unsafe_allow_html=True)

    with right:
        with st.popover("⚙️ Settings"):
            st.toggle("🔊 Click Sounds", key="sfx_enabled", value=st.session_state.get("sfx_enabled", True))
            st.caption("Local only; missing audio is OK.")

    st.markdown('</div>', unsafe_allow_html=True)
