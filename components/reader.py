# components/reader.py — reader card + sticky mobile controls
import os, html
import streamlit as st
from utils.state import set_qp
from utils.media import audio_tag_b64

def _safe_img(src: str):
    if src and os.path.exists(src):
        try: st.image(src, use_container_width=True); return
        except Exception: pass
    st.markdown('<div style="width:100%;aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;background:#0c1f45;border-radius:16px;font-size:40px;">✨</div>', unsafe_allow_html=True)

def render_reader(story: dict, parts: list, images: list, on_play_audio, ambient_src: str,
                  prev_slug: str|None, next_slug: str|None, current_cat: str):
    st.markdown('<div class="bt-card">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="text-align:center;margin:.1rem 0 .35rem;font-family:Fredoka;font-weight:900;background:var(--rainbow);-webkit-background-clip:text;color:transparent;">{html.escape(story["title"])}</h2>', unsafe_allow_html=True)
    st.markdown(f'<div style="display:flex;gap:.4rem;justify-content:center;flex-wrap:wrap;margin:.1rem 0 .55rem;">'
                f'<span class="bt-chip">📚 {html.escape(story["category"])}</span>'
                f'<span class="bt-chip">👶 {html.escape(story.get("age","4+"))}</span>'
                f'<span class="bt-chip">⏱️ {html.escape(story.get("readingTime","3 min"))}</span></div>', unsafe_allow_html=True)

    for i, p in enumerate(parts):
        if i==0 and len(images)>=1: _safe_img(images[0])
        st.markdown(f'<div style="font-size:1.08rem;line-height:1.78;font-family:Quicksand;">{p}</div>', unsafe_allow_html=True)
        if i==0 and len(images)>=2: _safe_img(images[1])
        if i==1 and len(images)>=3: _safe_img(images[2])

    c1,c2=st.columns(2)
    with c1:
        if st.button("🎧 Play Audio", use_container_width=True):
            on_play_audio()
    with c2:
        if ambient_src and os.path.exists(ambient_src):
            with open(ambient_src,"rb") as f:
                st.write("🫧 Ambient")
                st.markdown(audio_tag_b64(f.read(), controls=True, loop=True), unsafe_allow_html=True)
        else:
            st.write("🫧 Ambient (none)")

    st.markdown('<div class="bt-reader-sticky">', unsafe_allow_html=True)
    r1,r2,r3 = st.columns([1,1,1])
    with r1:
        if prev_slug and st.button("⬅️ Previous", use_container_width=True, key="reader_prev"):
            set_qp(cat=current_cat, pick=prev_slug, _merge=False)
    with r2:
        if st.button("🏠 Home", use_container_width=True, key="reader_home"):
            set_qp(cat=current_cat, pick=None, quiz=None, _merge=False)
    with r3:
        if next_slug and st.button("➡️ Next", use_container_width=True, key="reader_next"):
            set_qp(cat=current_cat, pick=next_slug, _merge=False)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
