# utils/media.py — root-aware image resolution (+diagnostics)
import json, os, base64, re, unicodedata, glob, mimetypes
from typing import List, Dict, Optional
from io import BytesIO
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]

try:
    from gtts import gTTS
except Exception:
    gTTS = None

try:
    from googletrans import Translator
    _translator = Translator()
except Exception:
    _translator = None

def _nfkd(s: str) -> str:
    return unicodedata.normalize("NFKD", s or "")

def slugify(text: str) -> str:
    t = _nfkd((text or "").strip().lower())
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "untitled"

def clean_title(s: str) -> str:
    if not s: return "Untitled"
    s = s.replace("\\\"", "\"").replace("\\'", "'").replace("\\*", "*").replace("\\\\", "\\")
    s = re.sub(r"[\\]+$", "", s)
    s = re.sub(r"^\s*['\"\*]+\s*|\s*['\"\*]+\s*$", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s or "Untitled"

def normalize(s: str) -> str:
    s = _nfkd((s or "").lower())
    return "".join(ch for ch in s if not unicodedata.combining(ch))

_KEYWORDS_TO_CATEGORY = [
    (["night","moon","star","sleep","dream"], "Bedtime"),
    (["forest","glow","river","tree","wind","leaf","birds","flower","mountain"], "Nature"),
    (["friend","kind","share","help","together","team"], "Friendship"),
    (["magic","sparkle","fairy","dragon","wizard","castle"], "Fantasy"),
    (["adventure","journey","explore","quest","space","rocket","planet"], "Adventure"),
]
def infer_category(title: str, content: str) -> str:
    text = f"{title} {content}".lower()
    for words, cat in _KEYWORDS_TO_CATEGORY:
        if any(w in text for w in words): return cat
    return "Other"

IMAGE_ROOTS = [
    ROOT / "images",
    ROOT / "assets" / "images",
    ROOT / "premium",
    ROOT / "stories",
    ROOT
]
# added JFIF and uppercase handling by normalizing
IMAGE_EXTS = ["jpg","jpeg","png","webp","gif","jfif"]

def _scan_images_once() -> Dict[str, str]:
    """Map lowercase basename -> ABS path."""
    if "IMAGE_INDEX" in st.session_state:
        return st.session_state.IMAGE_INDEX
    index: Dict[str, str] = {}
    total_scanned = 0
    for root in IMAGE_ROOTS:
        if not root.exists(): continue
        for p in root.rglob("*"):
            if not p.is_file(): continue
            ext = p.suffix.lower().lstrip(".")
            if ext in IMAGE_EXTS:
                bn = p.name.lower()
                total_scanned += 1
                if bn not in index:
                    index[bn] = str(p)
    st.session_state.IMAGE_INDEX = index
    st.session_state.IMAGE_INDEX_SUMMARY = f"Indexed {len(index)} unique filenames (scanned {total_scanned} files) under {', '.join(str(r) for r in IMAGE_ROOTS if r.exists())}"
    return index

def _resolve_one_path(raw: str) -> str:
    if not raw: return ""
    raw = raw.strip()
    if raw.startswith(("http://","https://","data:")):
        return raw
    p = raw.replace("\\","/")
    if os.path.isabs(p) and os.path.exists(p):
        return p
    abs_try = ROOT / p
    if abs_try.exists():
        return str(abs_try)
    bn = os.path.basename(p).lower()
    idx = _scan_images_once()
    if bn in idx: return idx[bn]
    return ""

def _guess_by_slug(slug: str) -> List[str]:
    guesses = []
    patterns = [
        f"{slug}.{{ext}}", f"{slug}_1.{{ext}}", f"{slug}_2.{{ext}}", f"{slug}_3.{{ext}}",
        f"{slug}-1.{{ext}}", f"{slug}-2.{{ext}}", f"{slug}-3.{{ext}}",
    ]
    for root in IMAGE_ROOTS:
        for ext in IMAGE_EXTS:
            for pat in patterns:
                p = root / pat.format(ext=ext)
                if p.exists(): guesses.append(str(p))
        cand = root / slug
        if cand.is_dir():
            for p in cand.rglob("*"):
                if p.is_file() and p.suffix.lower().lstrip(".") in IMAGE_EXTS:
                    guesses.append(str(p))
    seen=set(); out=[]
    for g in guesses:
        if g not in seen:
            out.append(g); seen.add(g)
    return out[:3]

def load_stories(path:str) -> List[dict]:
    fpath = path if os.path.isabs(path) else str((ROOT / path).resolve())
    if not os.path.exists(fpath): return []
    with open(fpath,"r",encoding="utf-8") as f: data=json.load(f)
    for s in data:
        s["title"] = clean_title(s.get("title","Untitled"))
        s.setdefault("author","BeluTales")
        s.setdefault("language","en")
        s.setdefault("age","4+")
        s.setdefault("readingTime","3 min")
        s.setdefault("tags",[])
        s["slug"] = s.get("slug") or slugify(s["title"])
        if not s.get("category"):
            s["category"] = infer_category(s["title"], s.get("content",""))
        for k in ("image_1","image_2","image_3","cover"):
            if s.get(k): s[k] = s[k].replace("\\","/")
    return data

def load_quizzes(path:str)->Dict[str,List[dict]]:
    fpath = path if os.path.isabs(path) else str((ROOT / path).resolve())
    if not os.path.exists(fpath): return {}
    with open(fpath,"r",encoding="utf-8") as f: return json.load(f)

def story_images(story:dict)->List[str]:
    resolved: List[str] = []
    if isinstance(story.get("images"), list):
        for val in story["images"]:
            p = _resolve_one_path(str(val))
            if p: resolved.append(p)
            if len(resolved) == 3: break
    for k in ("cover","image_1","image_2","image_3"):
        p = _resolve_one_path(story.get(k,""))
        if p and p not in resolved:
            resolved.append(p)
        if len(resolved) == 3: break
    if len(resolved) < 3:
        slug = story.get("slug") or slugify(story.get("title",""))
        for g in _guess_by_slug(slug):
            if g not in resolved:
                resolved.append(g)
            if len(resolved) == 3: break
    if not resolved:
        st.session_state["IMAGE_MISS"] = st.session_state.get("IMAGE_MISS", 0) + 1
    return resolved

def first_cover(story:dict)->str:
    imgs = story_images(story)
    return imgs[0] if imgs else ""

def image_src_for_html(path_or_url: str) -> str:
    if not path_or_url: return ""
    if path_or_url.startswith(("http://","https://","data:")):
        return path_or_url
    try:
        mime, _ = mimetypes.guess_type(path_or_url)
        mime = mime or "image/jpeg"
        with open(path_or_url, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return ""

def split_into_parts(text:str, min_parts=3, max_parts=6)->List[str]:
    raw = re.split(r'(?<=[.!?])\s+', (text or "").strip()); raw=[r for r in raw if r]
    if not raw: return [""]
    target = max(min_parts, min(max_parts, len(raw)))
    per = max(1, len(raw)//target)
    parts,buf=[],[]
    for i,s in enumerate(raw,1):
        buf.append(s)
        if len(buf)>=per and len(parts)<target-1:
            parts.append(" ".join(buf)); buf=[]
    if buf: parts.append(" ".join(buf))
    return parts

def translate_text(text: str, dest: str="en", src: Optional[str]=None) -> str:
    if not text: return text
    if not dest: dest = "en"
    if src and dest.lower() == src.lower(): return text
    if _translator is None: return text
    try:
        return _translator.translate(text, dest=dest).text
    except Exception:
        return text

def try_tts_mp3(text:str, lang:str="en", tld:str|None=None)->bytes|None:
    if not text or gTTS is None: return None
    try:
        kwargs = {"lang": lang or "en"}
        if tld and (lang or "en").lower() == "en":
            kwargs["tld"] = tld
        buf=BytesIO(); gTTS(text, **kwargs).write_to_fp(buf); buf.seek(0); return buf.read()
    except Exception:
        return None

def audio_tag_b64(mp3:bytes, controls=True, loop=False, autoplay=False)->str:
    b64=base64.b64encode(mp3).decode()
    attrs=[]
    if controls: attrs.append("controls")
    if loop: attrs.append("loop")
    if autoplay: attrs.append("autoplay")
    return f'''<audio {" ".join(attrs)}><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'''

def emoji_for_category(cat:str)->str:
    return {"Bedtime":"🌙","Nature":"🌲","Friendship":"🤝","Fantasy":"🧚","Adventure":"🗺️","Other":"✨"}.get(cat,"✨")
