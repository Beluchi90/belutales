# app.py — BeluTales (Premium Magical Theme • Always-On • Compact Mobile UI)
# Keeps: click sounds, category chip SFX, search, i18n, quizzes, favorites, splash, bedtime override,
#        interleaved images, ambient SFX, sticky header/clouds, URL ?cat= anchors.
# Adds:  - Always-on Magical Theme (fonts, colors, glassy cards, twinkles, animated rainbow title)
#        - Gentle parallax drift for header clouds
#        - English-only "sparkle" highlights for magical keywords in story text (safe; non-destructive)

import json, re, base64, unicodedata, random, os, time, hashlib
from io import BytesIO
from typing import List

import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
from gtts.lang import tts_langs
from googletrans import Translator

# Helpers you already own
from utils.media import get_story_images, split_story_into_parts, slugify, clean_title

# ------------------------------------------------------------
# Page + Frame
# ------------------------------------------------------------
st.set_page_config(page_title="BeluTales", page_icon="🦉", layout="wide")

# Base layout & components styling
st.markdown("""
<style>
  #MainMenu, footer, header [data-testid="stToolbar"] {visibility:hidden}
  .block-container { max-width: 430px !important; padding: .5rem .7rem 5.5rem !important; margin: 0 auto !important; }
  section[data-testid="stSidebar"] {display:none}
  div[data-testid="stVerticalBlock"] > div:has(> label) { margin-bottom: .45rem !important; }
  .stMarkdown, .stButton, .stSelectbox, .stTextInput, .stToggle, .stRadio { margin-bottom: .35rem !important; }

  .stButton>button, .stSelectbox, .stTextInput, .stToggle { font-size: 1rem !important; }
  .stButton>button { border-radius: 12px !important; padding: .64rem .9rem !important; }
  .stTextInput input { border-radius: 16px !important; padding: .6rem .8rem !important; }
  .stSelectbox div[data-baseweb="select"] { border-radius: 12px !important; }

  /* Header (clouds) */
  .bt-hero{ position: sticky; top: 0; z-index: 50; border-radius:20px; padding:14px;
    background: linear-gradient(180deg, #ffe9c6, #ffdfb0); box-shadow: 0 16px 40px rgba(255,165,66,.22);
    margin: 0 0 8px 0; overflow:hidden; isolation:isolate;}
  @keyframes driftSlow{0%{transform:translateX(-25%)}50%{transform:translateX(25%)}100%{transform:translateX(-25%)}}
  @keyframes driftMedium{0%{transform:translateX(-35%)}50%{transform:translateX(35%)}100%{transform:translateX(-35%)}}
  @keyframes driftFast{0%{transform:translateX(-45%)}50%{transform:translateX(45%)}100%{transform:translateX(-45%)}}
  .cloud{position:absolute;background:#fff;border-radius:50%;opacity:.85;
         box-shadow:30px 15px 0 -5px #fff,60px 8px 0 -8px #fff,90px 18px 0 -10px #fff;z-index:1}
  .cloud.s{width:28px;height:28px}.cloud.m{width:58px;height:58px}.cloud.l{width:92px;height:92px}
  .c1{top:6px;left:6%; animation:driftSlow 18s ease-in-out infinite}
  .c2{top:16px;left:24%;animation:driftMedium 14s ease-in-out infinite}
  .c3{top:2px; left:48%;animation:driftFast 10s ease-in-out infinite}
  .c4{top:28px;left:70%;animation:driftMedium 16s ease-in-out infinite}
  .c5{top:10px;left:86%;animation:driftSlow 20s ease-in-out infinite}
  .bt-row{ display:flex; gap:10px; align-items:center; position:relative; z-index:2;}
  .bt-owl{ width:48px; height:48px; border-radius:14px;
    background: radial-gradient(circle at 40% 35%, #ffd7a1, #ffa955);
    box-shadow: inset 0 0 0 4px #fff8ee, 0 8px 22px rgba(255,170,80,.35);
    display:flex; align-items:center; justify-content:center; font-size:28px;}
  .bt-title{ margin:0; font-size:32px; line-height:1.05; font-weight:900;
    font-family:'Baloo 2', system-ui, sans-serif;
    background: linear-gradient(90deg, #ff6f91, #ff9671, #ffc75f);
    -webkit-background-clip:text; background-clip:text; color:transparent; text-shadow:0 2px 0 rgba(255,255,255,.9);}
  .bt-tag{ margin:.05rem 0 0; font-size:13px; color:#493f34; opacity:.9; font-family:'Quicksand', system-ui, sans-serif;}

  /* Search */
  .search-wrap { background:#fff; border:2px solid #ffe3b8; border-radius:16px; padding:.3rem .4rem;
    box-shadow: 0 10px 22px #00000010; }
  .search-caption { color:#6b5846; font-size:.82rem; margin:.15rem 0 .3rem }
  .search-wrap .stTextInput input{
    font-size:.95rem !important; padding:.5rem .68rem !important;
    border-radius:16px !important; border:2px solid #f8dcb7 !important; background:#fffaf5 !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,.03);
    transition: box-shadow .15s ease, border-color .15s ease;
  }
  .search-wrap .stTextInput input:focus{
    outline:none !important; border-color:#ffd8a0 !important;
    box-shadow: 0 0 0 3px rgba(255, 200, 120, .25), inset 0 2px 4px rgba(0,0,0,.03);
  }
  .search-wrap .stButton>button{
    font-size:.9rem !important; padding:.5rem .95rem !important; border-radius:999px !important;
    border:1px solid #d2eafa !important; box-shadow:0 3px 8px rgba(0,0,0,.08);
    transition: transform .12s ease, filter .12s ease; white-space:nowrap !important; min-width:112px !important;
    background: linear-gradient(135deg, #bfe1ff, #8ccaff) !important; color:#103a57 !important;
  }
  .search-wrap .stButton>button:hover{ transform:translateY(-1px) scale(1.02); filter:brightness(.98) }

  /* CATEGORY BAR (HTML anchors) */
  #catbar { display:block; overflow-x:auto; white-space:nowrap; padding:6px 2px 2px; margin:6px 0 2px; }
  #catbar::-webkit-scrollbar{ height:6px } #catbar::-webkit-scrollbar-thumb{ background:#f1d9bb; border-radius:8px }
  #catbar .cat-btn{
    display:inline-flex; align-items:center; gap:.4rem; margin:0 10px 8px 0; text-decoration:none !important;
    background: linear-gradient(135deg, var(--bg1), var(--bg2));
    color: var(--fg); border: 2px solid var(--bd);
    border-radius: 999px; padding: .56rem .98rem; font-weight: 800;
    font-size: .98rem; font-family: 'Baloo 2', system-ui, sans-serif;
    box-shadow: 0 4px 10px rgba(0,0,0,.10), inset 0 1px 0 rgba(255,255,255,.85);
    transition: transform .12s ease, box-shadow .12s ease, filter .12s ease;
    pointer-events: auto;
  }
  #catbar .cat-btn:hover{ transform: translateY(-1px) scale(1.03); box-shadow: 0 8px 16px rgba(0,0,0,.14); filter: brightness(.98); }
  #catbar .cat-emoji{ font-size: 1.1rem; }

  /* Card & text */
  .story-card { background:#fff9f2; border-radius:18px; padding:.8rem .8rem .75rem;
    box-shadow: 8px 8px 18px #e5d8cc, -8px -8px 18px #ffffff; border:1px solid #00000010; margin-bottom:.7rem; }
  .story-title { font-size:1.6rem; text-align:center; margin:.2rem 0 .4rem 0; color:#ff7f50; font-family:'Baloo 2', system-ui, sans-serif; }
  .story-card img{ border-radius:16px !important; border:5px solid #fff !important;
    box-shadow: 0 12px 28px rgba(0,0,0,.09), 0 2px 0 rgba(255,255,255,.9) inset !important; }
  .story-text { font-size:1.04rem; line-height:1.6; color:#3a2a1d; font-family:'Quicksand', system-ui, sans-serif; }

  .meta-row{ display:flex; gap:.4rem; justify-content:center; flex-wrap:wrap; margin:.1rem 0 .45rem; }
  .chip-mini{ background:#fff; border:1px solid #f3e2c6; border-radius:999px; padding:.18rem .5rem; font-weight:700;
              font-size:.8rem; color:#5b4634; box-shadow:0 4px 10px #0000000d; font-family:'Quicksand', system-ui, sans-serif; }

  .quiz-card{ background:#fff9f2; border-radius:16px; padding:12px;
    box-shadow:8px 8px 18px #e5d8cc, -8px -8px 18px #ffffff; border:1px solid #00000010; margin:6px 0 10px; }
  /* Quiz: colored question badges */
  .q-badge { display:inline-flex; align-items:center; gap:.4rem; font-weight:900; font-family:'Baloo 2';
    border-radius:999px; padding:.2rem .6rem; font-size:.9rem; }
  .q-badge.mc { background:#ffe0f0; color:#4a1c35; border:1px solid #ffc5e6; }
  .q-badge.tf { background:#e0f7ff; color:#08324a; border:1px solid #bfe9ff; }
  .q-badge.seq { background:#e8ffe5; color:#153d21; border:1px solid #c7f7c3; }

  .sticky-bottom { position: sticky; bottom: 8px; z-index: 60;
    background: linear-gradient(180deg, rgba(255,242,230,0), rgba(255,242,230,.96) 35%);
    padding-top: .3rem; }

  /* Splash */
  .splash-wrap{ height:100vh; display:flex; align-items:center; justify-content:center; flex-direction:column;
    gap:10px; text-align:center; animation:splashFade .95s ease-out forwards;}
  .splash-card{ background: linear-gradient(180deg, #ffe9c6, #ffdfb0); border-radius: 24px; padding: 24px 18px; width: 86%;
    box-shadow: 0 24px 60px rgba(255,165,66,.25); position:relative; overflow:hidden;}
  .s-owl{ width:88px; height:88px; border-radius:22px; margin:0 auto 8px auto;
    background: radial-gradient(circle at 40% 35%, #ffd7a1, #ffa955);
    box-shadow: inset 0 0 0 6px #fff8ee, 0 12px 30px rgba(255,170,80,.35);
    font-size:52px; display:flex; align-items:center; justify-content:center; animation:blink 2.6s infinite; }
  @keyframes blink{0%,90%,100%{filter:none}95%{filter:brightness(.92)}}
  .s-title{ font-family:'Baloo 2'; font-weight:900; font-size:36px;
    background: linear-gradient(90deg, #ff6f91, #ff9671, #ffc75f);
    -webkit-background-clip:text; background-clip:text; color:transparent; margin:2px 0 4px 0; }
  .s-tag{ font-family:'Quicksand'; color:#493f34; opacity:.9; }
  @keyframes splashFade{ from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:translateY(0)} }

  @media (max-width: 480px){ .story-title { font-size: 1.5rem !important; } }
</style>
""", unsafe_allow_html=True)

# Always-on fun fonts
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;700;900&family=Quicksand:wght@400;600;700&family=Fredoka:wght@400;600;700&family=Sniglet:wght@400;800&display=swap" rel="stylesheet">
<style>:root{ --bg:#fff2e6; --surf:#fff9f2; --ink:#3d2a1a; } .stApp{ background:var(--bg); color:var(--ink); }</style>
""", unsafe_allow_html=True)

def header_clouds():
    st.markdown("""
    <section class="bt-hero">
      <div class="cloud l c1"></div><div class="cloud m c2"></div><div class="cloud s c3"></div>
      <div class="cloud m c4"></div><div class="cloud l c5"></div>
      <div class="bt-row">
        <div class="bt-owl">🦉</div>
        <div>
          <h1 class="bt-title">BeluTales</h1>
          <div class="bt-tag">Bedtime stories, gentle lessons, and cozy adventures.</div>
        </div>
      </div>
    </section>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# Splash
# ------------------------------------------------------------
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

def render_splash():
    st.markdown("""
    <div class="splash-wrap">
      <div class="splash-card">
        <div class="s-owl">🦉</div>
        <div class="s-title">BeluTales</div>
        <div class="s-tag">Cozy stories for bright hearts ✨</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

if not st.session_state.splash_done:
    render_splash(); time.sleep(1.0); st.session_state.splash_done = True; st.rerun()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
header_clouds()

# Gentle parallax for header clouds (safe, no blocking)
components.html("""
<script>
(function(){
  function run(){
    const doc = window.parent.document;
    const hero = doc.querySelector('.bt-hero'); if(!hero){ setTimeout(run,120); return; }
    if(hero.dataset._parallax) return; hero.dataset._parallax = '1';
    const clouds = hero.querySelectorAll('.cloud');
    doc.addEventListener('scroll', () => {
      const y = doc.scrollingElement.scrollTop || 0;
      clouds.forEach((c,i)=>{ c.style.transform = `translateX(${Math.sin((y/200)+(i*0.7))*12}px)`; });
    }, {passive:true});
  }
  run();
})();
</script>
""", height=0)

# ------------------------------------------------------------
# Load click sound globally (so all hooks can use it)
# ------------------------------------------------------------
audio_data_uri = ""
try:
    path = "assets/audio/click.mp3"  # keep in assets/audio/click.mp3
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        audio_data_uri = f"data:audio/mp3;base64,{b64}"
except Exception:
    audio_data_uri = ""

st.markdown(
    f'<audio id="click-snd" preload="auto" src="{audio_data_uri}" style="display:none"></audio>',
    unsafe_allow_html=True
)

# Global button SFX
components.html("""
  <script>
    (function(){
      function start(){
        const doc = window.parent.document;
        const audio = doc.getElementById('click-snd');
        if(!audio){ setTimeout(start, 120); return; }
        if(doc.body.dataset._btnsfx) return; doc.body.dataset._btnsfx = '1';
        doc.addEventListener('pointerdown', function(e){
          const btn = e.target.closest('button');
          if(!btn) return;
          if(btn.closest('[data-testid="stAudio"]')) return;
          if(btn.getAttribute('disabled') !== null) return;
          try{ audio.volume = 0.75; audio.currentTime = 0; audio.play(); }catch(_){}
        }, {capture:true, passive:true});
      }
      start();
    })();
  </script>
""", height=0)

# ------------------------------------------------------------
# Data
# ------------------------------------------------------------
with open("stories.json", "r", encoding="utf-8") as f:
    stories = json.load(f)

KEYWORDS_TO_CATEGORY = [
    (["night","moon","star","sleep","dream"], "Bedtime"),
    (["forest","glow","river","tree","wind"], "Nature"),
    (["friend","kind","share","help"], "Friendship"),
    (["magic","sparkle","fairy","dragon"], "Fantasy"),
    (["adventure","journey","explore","quest","space"], "Adventure"),
]
def infer_category(title: str, content: str) -> str:
    text = f"{title} {content}".lower()
    for words, cat in KEYWORDS_TO_CATEGORY:
        if any(w in text for w in words): return cat
    return "Other"
for s in stories:
    if not s.get("category"): s["category"] = infer_category(s.get("title",""), s.get("content",""))

categories = sorted({s.get("category","Other") for s in stories})
CATEGORY_EMOJI = {"All":"🌈","Bedtime":"🌙","Nature":"🌲","Friendship":"🤝","Fantasy":"🧚","Adventure":"🗺️","Other":"✨"}

# ------------------------------------------------------------
# i18n + search helpers
# ------------------------------------------------------------
translator = Translator()
def translate_text(text: str, dest: str) -> str:
    if not text or dest == "en": return text
    try: return translator.translate(text, dest=dest).text
    except Exception: return text
def normalize(s: str) -> str:
    s = s or ""; s = unicodedata.normalize("NFKD", s.lower())
    return "".join(ch for ch in s if not unicodedata.combining(ch))
def matches_query(story: dict, q: str, q_lang: str) -> bool:
    if not q: return True
    qn = normalize(q)
    if q_lang != "en":
        try: qn = normalize(translator.translate(qn, dest="en").text)
        except Exception: pass
    hay = normalize(" ".join([ str(story.get("title","")), str(story.get("content","")), str(story.get("category","")) ]))
    tokens = [t for t in qn.split() if t]
    return all(t in hay for t in tokens)

# ------------------------------------------------------------
# Session defaults
# ------------------------------------------------------------
languages = {
    "English 🇬🇧":"en", "French 🇫🇷":"fr", "Spanish 🇪🇸":"es",
    "Swahili 🇰🇪":"sw", "Arabic 🇸🇦":"ar",
    "Chinese (Simplified) 🇨🇳":"zh-cn", "Chinese (Traditional) 🇹🇼":"zh-tw",
    "Zulu 🇿🇦":"zu", "Afrikaans 🇿🇦":"af", "Igbo 🇳🇬":"ig", "Yoruba 🇳🇬":"yo",
}
SS = st.session_state
SS.setdefault("selected_language", list(languages.keys())[0])
SS.setdefault("selected_category", "All")
SS.setdefault("premium_unlocked", True)
SS.setdefault("search_query", "")
SS.setdefault("favorites_only", False)
SS.setdefault("favorite_stories", set())
SS.setdefault("story_idx", 0)
SS.setdefault("stars", 0)
SS.setdefault("bedtime_mode", False)
SS.setdefault("last_title", "")
SS.setdefault("last_category", "")

# ------------------------------------------------------------
# Read ?cat= from URL (st.query_params)
# ------------------------------------------------------------
cat_from_url = None
try:
    qp = st.query_params
    cat_from_url = qp.get("cat")
    if isinstance(cat_from_url, list): cat_from_url = cat_from_url[0] if cat_from_url else None
except Exception:
    pass
if cat_from_url and cat_from_url in (["All"] + list(categories)):
    SS.selected_category = cat_from_url

# ------------------------------------------------------------
# Search (top)
# ------------------------------------------------------------
def _apply_search():
    SS.search_query = (SS.get("search_box") or "").strip()

st.markdown("<div class='search-caption'>Find a story fast:</div>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='search-wrap'>", unsafe_allow_html=True)
    s1, s2 = st.columns([7.2, 2.8])
    with s1:
        st.text_input("🔍 Search", key="search_box", value=SS.search_query,
                      placeholder="Search a story, character, or theme…",
                      label_visibility="collapsed", on_change=_apply_search)
    with s2:
        if st.button("Search", use_container_width=True, key="btn_search"):
            _apply_search(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Filtering pipeline
# ------------------------------------------------------------
filtered = stories
if SS.favorites_only:
    favs = set(SS.favorite_stories)
    filtered = [s for s in filtered if clean_title(s.get("title","")) in favs]
if SS.selected_category != "All":
    filtered = [s for s in filtered if s.get("category","Other") == SS.selected_category]
if not SS.premium_unlocked:
    filtered = [s for s in filtered if not s.get("premium", False)]

lang_code = languages[SS.selected_language].lower()
q_now = (SS.search_query or "").strip()
if q_now:
    filtered = [s for s in filtered if matches_query(s, q_now, lang_code)]

titles = [clean_title(s["title"]) for s in filtered]
if not titles:
    st.info("No stories match your filters. Try changing filters.")
    st.stop()
SS.story_idx = min(SS.story_idx, len(titles)-1)

# ------------------------------------------------------------
# Story (first)
# ------------------------------------------------------------
story = filtered[SS.story_idx]
SS.last_title = clean_title(story["title"]); SS.last_category = story.get("category","Other")

slug = story.get("slug") or slugify(story["title"])
images = get_story_images(slug)  # [cover, mid, end] if available

content = story.get("content","")
if isinstance(content, dict):
    chunks = []
    if "introduction" in content: chunks.append(str(content["introduction"]))
    if "songLyrics" in content and isinstance(content["songLyrics"], list):
        for v in content["songLyrics"]:
            for _, lines in v.items():
                chunks.append("<br>".join(lines))
    if "meaning" in content: chunks.append(f"<i>{content['meaning']}</i>")
    if "conclusion" in content: chunks.append(content["conclusion"])
    full_text = "\n\n".join(chunks)
else:
    full_text = str(content)

full_text_t = translate_text(full_text, lang_code)
parts_src = split_story_into_parts(full_text, parts=3)
parts_t = [translate_text(p, lang_code) if p else "" for p in parts_src]

title_t = translate_text(clean_title(story["title"]), lang_code)
category_t = translate_text(story.get("category","Other"), lang_code)
age = story.get("ageRange","N/A"); rtime = story.get("readingTime","N/A")

# --- Magical keyword sprinkles (English only, safe no-op otherwise)
MAGIC_MAP = {
    r"\bmoon\b": "spark-pk", r"\bstar(s)?\b": "spark-yl", r"\bmagic(al)?\b": "spark-rb",
    r"\bdream(s|ing)?\b": "spark-bu", r"\bforest\b": "spark-gr", r"\briver\b": "spark-bl",
    r"\bfriend(ship)?\b": "spark-or", r"\bkind(ness)?\b": "spark-pu", r"\bdragon\b": "spark-rd",
    r"\bwind\b": "spark-te"
}
def decorate_magic_html(html_text: str) -> str:
    if not html_text or lang_code != "en": return html_text
    out = html_text
    for pat, cls in MAGIC_MAP.items():
        out = re.sub(pat, lambda m: f'<span class="{cls}">{m.group(0)}</span>', out, flags=re.IGNORECASE)
    return out

def _safe_image(src: str):
    if not src: return
    try: st.image(src, use_container_width=True)
    except Exception: pass

st.caption(f"🔎 {len(filtered)} stor{'y' if len(filtered)==1 else 'ies'} • ⭐ {SS.stars} stars")

# ------------------------------------------------------------
# TOP NAV (above title)
# ------------------------------------------------------------
nav_cols = st.columns([1, 1, 1])
with nav_cols[0]:
    if st.button("⬅️ Previous", use_container_width=True, key="top_prev"):
        SS.story_idx = (SS.story_idx - 1) % len(titles)
        st.rerun()
with nav_cols[1]:
    if st.button("🎲 Surprise", use_container_width=True, key="top_surprise"):
        if len(titles) > 1:
            options = [i for i in range(len(titles)) if i != SS.story_idx]
            SS.story_idx = random.choice(options)
            st.rerun()
with nav_cols[2]:
    if st.button("➡️ Next", use_container_width=True, key="top_next"):
        SS.story_idx = (SS.story_idx + 1) % len(titles)
        st.rerun()

# ------------------------------------------------------------
# Story card + content
# ------------------------------------------------------------
st.markdown('<div class="story-card">', unsafe_allow_html=True)
st.markdown(f'<div class="story-title">{title_t}</div>', unsafe_allow_html=True)
st.markdown(f"<div class='meta-row'><div class='chip-mini'>📚 {category_t}</div>"
            f"<div class='chip-mini'>👶 {age}</div><div class='chip-mini'>⏱️ {rtime}</div></div>", unsafe_allow_html=True)

img1 = images[0] if len(images)>0 else ""
img2 = images[1] if len(images)>1 else ""
img3 = images[2] if len(images)>2 else ""
_safe_image(img1)
if parts_t[0]: st.markdown(f'<div class="story-text">{decorate_magic_html(parts_t[0])}</div>', unsafe_allow_html=True)
_safe_image(img2)
if parts_t[1]: st.markdown(f'<div class="story-text">{decorate_magic_html(parts_t[1])}</div>', unsafe_allow_html=True)
_safe_image(img3)
if parts_t[2]: st.markdown(f'<div class="story-text">{decorate_magic_html(parts_t[2])}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# Read Aloud + Ambient
# ------------------------------------------------------------
def gtts_bytes(text: str, lang: str = "en", tld: str = "com") -> bytes:
    buf = BytesIO(); gTTS(text, lang=lang, tld=tld).write_to_fp(buf); buf.seek(0); return buf.read()
def audio_tag_base64(mp3_bytes: bytes, controls=True, loop=False, autoplay=False) -> str:
    b64 = base64.b64encode(mp3_bytes).decode()
    attrs = []
    if controls: attrs.append("controls")
    if loop: attrs.append("loop")
    if autoplay: attrs.append("autoplay")
    return f'''<audio {" ".join(attrs)}><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'''
TTS_LANGS = {code.lower() for code in tts_langs().keys()}
NARRATOR_TLD = {"Sunny (US)":"com","Rosie (UK)":"co.uk","Skye (AU)":"com.au","Ayo (ZA)":"co.za","Priya (IN)":"co.in"}
CATEGORY_AMBIENT = {"Nature":"assets/sfx/forest.mp3","Bedtime":"assets/sfx/wind.mp3",
                    "Fantasy":"assets/sfx/magic.mp3","Friendship":"assets/sfx/birds.mp3","Adventure":"assets/sfx/wind.mp3"}

def read_aloud(text: str):
    lang_code2 = languages[SS.selected_language].lower()
    if lang_code2 not in TTS_LANGS:
        st.info("🎙️ Read Aloud not available for this language yet."); return
    tld = "com" if lang_code2 != "en" else NARRATOR_TLD.get("Sunny (US)", "com")
    try:
        mp3 = gtts_bytes(text, lang=lang_code2, tld=tld)
        st.markdown(audio_tag_base64(mp3, controls=True), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Audio generation failed: {e}")

c1, c2 = st.columns(2)
with c1:
    if st.button("🎧 Read Aloud", use_container_width=True): read_aloud(full_text_t)
with c2:
    amb = CATEGORY_AMBIENT.get(story.get("category",""))
    if amb and os.path.exists(amb):
        st.write("🫧 Ambient")
        with open(amb, "rb") as f:
            st.markdown(audio_tag_base64(f.read(), controls=True, loop=True), unsafe_allow_html=True)

# ------------------------------------------------------------
# Magic Moments
# ------------------------------------------------------------
SFX_KEYWORDS = {"rain":"assets/sfx/rain.mp3","bird":"assets/sfx/birds.mp3","birds":"assets/sfx/birds.mp3",
                "magic":"assets/sfx/magic.mp3","bell":"assets/sfx/bell.mp3","wind":"assets/sfx/wind.mp3"}
def sentence_split(text: str) -> List[str]:
    raw = re.split(r'(?<=[.!?])\s+', text.strip()); return [r for r in raw if r]
def find_sentence_sfx(sentence: str) -> List[str]:
    s = sentence.lower(); return [p for kw,p in SFX_KEYWORDS.items() if kw in s and os.path.exists(p)]

sfx_candidates = []
for sent in sentence_split(full_text_t):
    hits = find_sentence_sfx(sent)
    if hits: sfx_candidates.append((sent, hits))
if sfx_candidates:
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    st.markdown("### ✨ Magic Moments")
    for i, (sent, paths) in enumerate(sfx_candidates[:6]):
        cols = st.columns([8,1,1])
        with cols[0]: st.write(f"• {sent}")
        if len(paths)>=1:
            with cols[1]:
                if st.button("✨", key=f"sfx_{i}_0"):
                    with open(paths[0],"rb") as f: st.markdown(audio_tag_base64(f.read(), autoplay=True), unsafe_allow_html=True)
        if len(paths)>=2:
            with cols[2]:
                if st.button("🔔", key=f"sfx_{i}_1"):
                    with open(paths[1],"rb") as f: st.markdown(audio_tag_base64(f.read(), autoplay=True), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# Quick Quiz (VARIED STYLES)
# ------------------------------------------------------------
def seeded_rand(slug: str):
    seed = int(hashlib.sha256(slug.encode("utf-8")).hexdigest(), 16) % (2**32)
    return random.Random(seed)

def build_quiz_varied(s: dict):
    title = clean_title(s.get("title","")).strip() or "The hero"
    category = s.get("category","Other")
    content_text = s.get("content","")
    slug_local = s.get("slug") or slugify(title)
    rng = seeded_rand(slug_local)

    cats = ["Bedtime","Nature","Friendship","Fantasy","Adventure","Other"]
    wrong_cats = [c for c in cats if c != category]
    rng.shuffle(wrong_cats)

    name_guess = title.split()[0] if title else "The hero"
    mc1_opts = [name_guess, "A River", "A Fox"]; rng.shuffle(mc1_opts)
    q_mc1 = {"type":"mc","badge":"Character","question":"Who is the main character in this story?",
             "options": mc1_opts, "answer": name_guess}

    mc2_opts = [category, wrong_cats[0], wrong_cats[1] if len(wrong_cats)>1 else "Other"]; rng.shuffle(mc2_opts)
    q_mc2 = {"type":"mc","badge":"Theme","question":"What kind of story is this?",
             "options": mc2_opts, "answer": category}

    text_low = str(content_text).lower()
    likely_nature = any(w in text_low for w in ["forest","river","tree","wind","leaf","birds","flower"])
    tf1 = {"type":"tf","badge":"True/False","statement":"This story teaches a gentle lesson.","answer_bool": True}
    tf2 = {"type":"tf","badge":"True/False",
           "statement": "The setting includes nature sounds like wind or birds." if likely_nature else "The setting is in a busy city street.",
           "answer_bool": True if likely_nature else False}

    seq_opts = ["They learned to be kind.","They forgot their friends.","They gave up on the journey."]
    rng.shuffle(seq_opts)
    q_seq = {"type":"seq","badge":"Next","question":"What happens (or what’s the lesson) by the end?",
             "options": seq_opts, "answer": "They learned to be kind."}

    style_index = int(hashlib.md5(slug_local.encode("utf-8")).hexdigest(), 16) % 3
    if style_index == 0: return [q_mc1, q_mc2]
    elif style_index == 1: return [tf1, tf2, q_mc2]
    else: return [q_mc1, q_seq]

def render_quiz(s: dict, lang_code: str):
    slug_local = (s.get("slug") or slugify(s.get("title","")))
    quiz = build_quiz_varied(s)
    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Quick Quiz")
    for idx, q in enumerate(quiz):
        key_base = f"quiz_{slug_local}_{idx}"
        if q["type"] == "mc":
            badge = f'<span class="q-badge mc">🍬 {q["badge"]}</span>'
            q_text = translate_text(q["question"], lang_code)
            opts = [translate_text(o, lang_code) for o in q["options"]]
            ans = translate_text(q["answer"], lang_code)
            st.markdown(f"{badge} &nbsp; **{q_text}**", unsafe_allow_html=True)
            pick = st.radio("", opts, key=f"{key_base}_mc", label_visibility="collapsed")
            if st.button(f"Check {idx+1}", key=f"{key_base}_btn"):
                if pick == ans: st.success("🎉 Correct! +1 ⭐"); st.session_state.stars += 1
                else: st.error("❌ Not quite. Try again!")
        elif q["type"] == "tf":
            badge = '<span class="q-badge tf">🔵 True / False</span>'
            stmt = translate_text(q["statement"], lang_code)
            st.markdown(f"{badge} &nbsp; **{stmt}**", unsafe_allow_html=True)
            pick = st.radio("", ["True", "False"], key=f"{key_base}_tf", label_visibility="collapsed")
            if st.button(f"Check {idx+1}", key=f"{key_base}_btn"):
                is_true = (pick == "True")
                if is_true == q["answer_bool"]: st.success("🎉 Correct! +1 ⭐"); st.session_state.stars += 1
                else: st.error("❌ Not quite. Try again!")
        elif q["type"] == "seq":
            badge = '<span class="q-badge seq">🟢 What next?</span>'
            q_text = translate_text(q["question"], lang_code)
            opts = [translate_text(o, lang_code) for o in q["options"]]
            ans = translate_text(q["answer"], lang_code)
            st.markdown(f"{badge} &nbsp; **{q_text}**", unsafe_allow_html=True)
            pick = st.radio("", opts, key=f"{key_base}_seq", label_visibility="collapsed")
            if st.button(f"Check {idx+1}", key=f"{key_base}_btn"):
                if pick == ans: st.success("🎉 Correct! +1 ⭐"); st.session_state.stars += 1
                else: st.error("❌ Not quite. Try again!")
    st.markdown('</div>', unsafe_allow_html=True)

render_quiz(story, lang_code)

# ------------------------------------------------------------
# Favorites
# ------------------------------------------------------------
if st.button("⭐ Add to Favorites", key="fav_btn", use_container_width=True):
    SS.favorite_stories.add(clean_title(story["title"])); st.balloons()

# ------------------------------------------------------------
# Filters & Options (includes category chips + category click SFX)
# ------------------------------------------------------------
with st.expander("🎛️ Filters & Options", expanded=False):
    SS.bedtime_mode = st.toggle("🌙 Bedtime Mode (cozy)", value=SS.bedtime_mode)
    st.markdown("**Quick Category**")

    # Bright pastel palette (session-stable)
    PASTELS = [
        {"bg1":"#ffd6e7","bg2":"#ff9ec2","bd":"#ff9fb9","fg":"#4a2431"},
        {"bg1":"#ffe3c0","bg2":"#ffc07d","bd":"#ffc98f","fg":"#4a2e12"},
        {"bg1":"#d9ffd8","bg2":"#98f5b3","bd":"#b9f3c8","fg":"#103d29"},
        {"bg1":"#d9f3ff","bg2":"#9bd4ff","bd":"#bfe1ff","fg":"#0f2e4a"},
        {"bg1":"#e7dcff","bg2":"#c1a6ff","bd":"#d3c2ff","fg":"#2a184f"},
        {"bg1":"#fff2c6","bg2":"#ffe18a","bd":"#ffe8a9","fg":"#473a10"},
        {"bg1":"#ffe0f5","bg2":"#ffb7eb","bd":"#ffc8ef","fg":"#471639"},
        {"bg1":"#dcfff7","bg2":"#aef7e7","bd":"#c9fbf1","fg":"#0e3d37"},
    ]
    if "cat_palette" not in SS: SS.cat_palette = random.sample(PASTELS, k=len(PASTELS))
    def pastel_for_index(i:int):
        p = SS.cat_palette[i % len(SS.cat_palette)]; return p["bg1"], p["bg2"], p["bd"], p["fg"]

    # Render HTML anchor chips
    chip_labels = ["All"] + [c for c in categories if c!="All"]
    html = ['<div id="catbar">']
    for i, cat in enumerate(chip_labels):
        bg1, bg2, bd, fg = pastel_for_index(i)
        html.append(
            f'<a class="cat-btn" href="?cat={cat}" style="--bg1:{bg1};--bg2:{bg2};--bd:{bd};--fg:{fg}">'
            f'<span class="cat-emoji">{CATEGORY_EMOJI.get(cat,"✨")}</span> {cat}'
            f'</a>'
        )
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)

    # Category chips SFX (non-blocking)
    components.html("""
      <script>
        (function(){
          function hook(){
            const doc = window.parent.document;
            const bar = doc.querySelector('#catbar');
            const audio = doc.getElementById('click-snd');
            if(!bar || !audio){ setTimeout(hook, 120); return; }
            if(bar.dataset._sfx) return; bar.dataset._sfx = '1';
            const play = ()=>{ try{ audio.volume = 0.75; audio.currentTime = 0; audio.play(); }catch(_){} };
            bar.addEventListener('pointerdown', function(e){
              const a = e.target.closest('a.cat-btn'); if(!a) return; play();
            }, {capture:true, passive:true});
            bar.addEventListener('touchstart', function(e){
              const a = e.target.closest('a.cat-btn'); if(!a) return; play();
            }, {capture:true, passive:true});
            bar.addEventListener('mousedown', function(e){
              const a = e.target.closest('a.cat-btn'); if(!a) return; play();
            }, {capture:true, passive:true});
          }
          hook();
        })();
      </script>
    """, height=0)

    c1, c2 = st.columns(2)
    with c1:
        lang_label = st.selectbox("🌍 Language", list(languages.keys()),
                                  index=list(languages.keys()).index(SS.selected_language))
        SS.selected_language = lang_label
    with c2:
        SS.premium_unlocked = st.toggle("🔓 Unlocked (premium on)", value=SS.premium_unlocked)

    st.markdown("**Choose Story**")
    selected_title = st.selectbox("", titles, index=SS.story_idx, label_visibility="collapsed")
    if titles[SS.story_idx] != selected_title:
        SS.story_idx = titles.index(selected_title); st.experimental_rerun()

# ------------------------------------------------------------
# Bedtime palette override (cozy)
# ------------------------------------------------------------
if SS.bedtime_mode:
    st.markdown("""
    <style>
      :root{ --bg:#2a2230; --surf:#362a3d; --ink:#efe7ff; }
      .stApp{ background:var(--bg) !important; color:var(--ink) !important; }
      .bt-hero{ background: linear-gradient(180deg, #3a2b46, #2f2439) !important; box-shadow: 0 18px 44px rgba(60,40,100,.35) !important; }
      .bt-title{ background: linear-gradient(90deg, #f0e6ff, #d0c3ff, #f7d282) !important; -webkit-background-clip:text; color:transparent; text-shadow:none; }
      .story-text, .bt-tag, .story-title { color:#efe7ff !important; }
      .story-card, .quiz-card { background: var(--surf) !important; box-shadow: 8px 8px 16px #211a26, -8px -8px 18px #3f3248 !important; border-color:#4a3d56 !important; }
      .search-wrap .stTextInput input{ background:#2f2439 !important; border-color:#4a3d56 !important; color:#efe7ff !important; }
      .search-wrap .stButton>button{ background: linear-gradient(135deg, #b99cff, #d7c6ff) !important; color:#2a2230 !important; }
      #catbar .cat-btn{ filter: saturate(.92); }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# Always-On Magical Theme (applies only when NOT in Bedtime Mode)
# ------------------------------------------------------------
if not SS.bedtime_mode:
    st.markdown("""
    <style>
      /* Sky background with soft twinkles */
      :root{
        --bg: linear-gradient(180deg,#fef3ff 0%, #ffe9f5 35%, #fff3d6 100%);
        --surf:#fffaf5; --ink:#2b1c14;
      }
      .stApp{ background: var(--bg) !important; }
      body::before{
        content:""; position:fixed; inset:0; pointer-events:none; z-index:-1;
        background:
          radial-gradient(circle at 12% 18%, rgba(255,255,255,.7) 0 6px, transparent 7px),
          radial-gradient(circle at 82% 22%, rgba(255,255,255,.7) 0 6px, transparent 7px),
          radial-gradient(circle at 30% 42%, rgba(255,255,255,.7) 0 4px, transparent 5px),
          radial-gradient(circle at 70% 64%, rgba(255,255,255,.7) 0 5px, transparent 6px);
        animation: twinkle 5s linear infinite;
      }
      @keyframes twinkle{ 0%{opacity:.7} 50%{opacity:.35} 100%{opacity:.7} }

      /* Header: brighter clouds + animated rainbow title */
      .bt-hero{
        background: linear-gradient(180deg, #ffe6ff, #ffd9ef, #ffefc8) !important;
        box-shadow: 0 20px 52px rgba(255,140,180,.28) !important;
      }
      .bt-title{
        font-family:'Fredoka','Baloo 2',system-ui,sans-serif !important;
        letter-spacing:.5px; font-weight:900;
        background: linear-gradient(90deg,#ff6f91,#ff9671,#ffc75f,#f9f871,#a0e7e5,#b4f8c8,#f6a6ff);
        background-size: 400% 100%;
        -webkit-background-clip:text; background-clip:text; color:transparent;
        text-shadow: 0 2px 0 rgba(255,255,255,.95);
        animation: rainbowSlide 10s linear infinite;
      }
      @keyframes rainbowSlide{0%{background-position:0% 50%}100%{background-position:100% 50%}}
      .bt-owl{ animation: owlblink 3.5s infinite; }
      @keyframes owlblink{ 0%,92%,100%{filter:none} 96%{filter:brightness(.9)} }
      .bt-tag{ font-family:'Sniglet','Quicksand',system-ui,sans-serif !important; font-weight:800; }

      /* Story card: glassy pastel & playful text */
      .story-card{
        background: radial-gradient(120% 120% at 20% 0%, #ffffff 0%, #fff6fb 40%, #fff9f2 100%) !important;
        border: 1px solid #ffe2f2 !important;
        box-shadow: 10px 12px 28px rgba(255,150,200,.20), -6px -6px 18px #ffffff !important;
      }
      .story-title{
        font-family:'Fredoka','Baloo 2',system-ui,sans-serif !important;
        font-weight:900 !important; letter-spacing:.3px; font-size:1.7rem !important;
        background: linear-gradient(90deg,#ff8fab,#ffc6ff,#ffd6a5,#caffbf);
        background-size: 300% 100%;
        -webkit-background-clip:text; background-clip:text; color:transparent;
        animation: rainbowSlide 12s linear infinite;
      }
      .story-text{
        font-family:'Quicksand',system-ui,sans-serif !important;
        font-size:1.06rem !important; line-height:1.7 !important; color:#3a2a1d !important;
      }
      .story-text p:first-letter{
        font-family:'Sniglet','Fredoka',system-ui,sans-serif;
        font-weight:800; font-size:1.35em; padding-right:2px; color:#ff6f91;
      }
      .story-card img{ border:6px solid #fff !important;
        box-shadow: 0 18px 36px rgba(0,0,0,.12), 0 2px 0 rgba(255,255,255,.95) inset !important; }

      /* Chips + quiz badges playful */
      .chip-mini{ border-color:#ffdff1 !important; font-weight:800 !important; }
      .quiz-card{
        background: linear-gradient(180deg,#fff7fd,#fffaf2) !important;
        border-color:#ffe3f3 !important;
        box-shadow: 10px 10px 22px rgba(255,170,210,.18), -8px -8px 20px #ffffff !important;
      }
      .q-badge{ font-family:'Sniglet','Baloo 2',system-ui,sans-serif !important; font-weight:800 !important; }
      .q-badge.mc{ background:#ffe0ff !important; color:#4a1843 !important; border-color:#ffc8ff !important; }
      .q-badge.tf{ background:#e0f5ff !important; color:#08324a !important; border-color:#bfe9ff !important; }
      .q-badge.seq{ background:#e9ffe1 !important; color:#153d21 !important; border-color:#c7f7c3 !important; }

      /* Buttons: bouncy feel */
      .stButton>button{
        font-family:'Fredoka','Baloo 2',system-ui,sans-serif !important;
        font-weight:900; letter-spacing:.2px;
        transition: transform .12s ease, filter .12s ease !important;
      }
      .stButton>button:hover{ transform: translateY(-1px) scale(1.02); }

      /* Tiny floating stickers */
      .stApp::after{
        content: "🌙✨🧸"; position: fixed; right: 10px; top: 8px; opacity:.35; font-size:20px; pointer-events:none;
      }

      /* Sparkle highlight styles for English keyword decoration */
      .spark-pk{ background:linear-gradient(90deg,#ffb3d9,#ffd1e8); border-radius:6px; padding:0 .2em }
      .spark-yl{ background:linear-gradient(90deg,#fff2a8,#ffe19a); border-radius:6px; padding:0 .2em }
      .spark-rb{ background:linear-gradient(90deg,#ffc0cb,#ffecd2); border-radius:6px; padding:0 .2em }
      .spark-bu{ background:linear-gradient(90deg,#c6f0ff,#e9f7ff); border-radius:6px; padding:0 .2em }
      .spark-gr{ background:linear-gradient(90deg,#c5ffd6,#e8ffef); border-radius:6px; padding:0 .2em }
      .spark-bl{ background:linear-gradient(90deg,#cfe7ff,#e8f1ff); border-radius:6px; padding:0 .2em }
      .spark-or{ background:linear-gradient(90deg,#ffd3a3,#ffe6c7); border-radius:6px; padding:0 .2em }
      .spark-pu{ background:linear-gradient(90deg,#e5d0ff,#f0e5ff); border-radius:6px; padding:0 .2em }
      .spark-rd{ background:linear-gradient(90deg,#ffb0b0,#ffd6d6); border-radius:6px; padding:0 .2em }
      .spark-te{ background:linear-gradient(90deg,#c0fff6,#e3fffb); border-radius:6px; padding:0 .2em }
    </style>
    """, unsafe_allow_html=True)
