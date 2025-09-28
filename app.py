import streamlit as st
import json

# Page configuration
st.set_page_config(page_title="BeluTales", page_icon="🦉", layout="wide")

# Custom CSS styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One:wght@400&family=Baloo+2:wght@600;700;800&family=Comic+Neue:wght@400;700&display=swap');

/* Story title styling - magical and bold */
.stApp .story-card h3,
.stApp .story-card .stSubheader,
.stApp h1[data-testid="stMarkdownContainer"],
.stApp h2[data-testid="stMarkdownContainer"],
.stApp h3[data-testid="stMarkdownContainer"] {
    font-family: "Fredoka One", "Baloo 2", "Comic Neue", sans-serif !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 1.4em !important;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.3), 0 2px 8px rgba(0, 0, 0, 0.4) !important;
    letter-spacing: 0.5px !important;
    animation: gentleFadeIn 0.8s ease-out !important;
    text-align: center !important;
    margin-bottom: 1rem !important;
}

/* Story body text styling - readable and cute */
.stApp .story-text,
.stApp .story-card p,
.stApp .story-card .stMarkdown,
.stApp div[data-testid="stMarkdownContainer"] p {
    font-family: "Baloo 2", "Comic Neue", sans-serif !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 1.1em !important;
    line-height: 1.6 !important;
    text-shadow: 0 0 8px rgba(255, 255, 255, 0.2), 0 1px 4px rgba(0, 0, 0, 0.3) !important;
    animation: gentleFadeIn 1.0s ease-out !important;
    text-align: justify !important;
    margin-bottom: 1.2rem !important;
}

/* Story content wrapper for better presentation */
.stApp .story-text {
    background: rgba(255, 255, 255, 0.05) !important;
    padding: 1.2rem !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(5px) !important;
    margin: 0.8rem 0 !important;
    animation: gentleFadeIn 1.2s ease-out !important;
}

/* Gentle fade-in animation */
@keyframes gentleFadeIn {
    0% {
        opacity: 0;
        transform: translateY(10px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Story card title enhancement */
.stApp .story-card .stSubheader h3 {
    font-family: "Fredoka One", "Baloo 2", sans-serif !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 1.3em !important;
    text-shadow: 0 0 8px rgba(255, 255, 255, 0.25), 0 2px 6px rgba(0, 0, 0, 0.4) !important;
    animation: gentleFadeIn 0.6s ease-out !important;
}

/* Detail view story title */
.stApp div[data-testid="stMarkdownContainer"] h1 {
    font-family: "Fredoka One", "Baloo 2", sans-serif !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 2.2em !important;
    text-shadow: 0 0 15px rgba(255, 255, 255, 0.4), 0 3px 10px rgba(0, 0, 0, 0.5) !important;
    text-align: center !important;
    animation: gentleFadeIn 0.8s ease-out !important;
    margin-bottom: 1.5rem !important;
}

/* Accessibility: Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
    .stApp .story-text,
    .stApp .story-card h3,
    .stApp .story-card .stSubheader,
    .stApp h1[data-testid="stMarkdownContainer"],
    .stApp h2[data-testid="stMarkdownContainer"],
    .stApp h3[data-testid="stMarkdownContainer"] {
        animation: none !important;
    }
}

/* Ensure good contrast for readability */
.stApp .story-text::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    z-index: -1;
    pointer-events: none;
}

/* Normal-sized kid-friendly buttons with playful styling */
.stApp .stButton>button,
.stApp .stDownloadButton>button {
    border-radius: 18px !important;
    padding: 0.25rem 0.75rem !important;
    border: none !important;
    font-size: 0.875rem !important;
    min-height: 2rem !important;
    font-family: "Baloo 2", "Comic Neue", sans-serif !important;
    font-weight: 600 !important;
    color: white !important;
    letter-spacing: 0.2px !important;
    line-height: 1.4 !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    background: linear-gradient(135deg, #ffcc70, #ff6ec4) !important;
    background-size: 200% 200% !important;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15), 0 1px 6px rgba(255, 110, 196, 0.2) !important;
    transition: all 0.25s ease !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
}

/* Hover effects */
.stApp .stButton>button:hover,
.stApp .stDownloadButton>button:hover {
    transform: scale(1.03) translateY(-1px) !important;
    background: linear-gradient(135deg, #ffd580, #ff7ed4) !important;
    background-position: 100% 0 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), 0 2px 8px rgba(255, 110, 196, 0.4), 0 0 15px rgba(255, 204, 112, 0.3) !important;
    color: white !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
}

/* Active/pressed state */
.stApp .stButton>button:active,
.stApp .stDownloadButton>button:active {
    transform: scale(1.01) !important;
    transition: all 0.1s ease !important;
}

/* Focus states for accessibility */
.stApp .stButton>button:focus,
.stApp .stDownloadButton>button:focus {
    outline: 2px solid rgba(255, 204, 112, 0.8) !important;
    outline-offset: 2px !important;
    box-shadow: 0 0 0 3px rgba(255, 204, 112, 0.2) !important;
}

/* Navigation buttons */
.stApp .stButton>button[kind="secondary"],
.stApp .stButton>button:contains("Previous"),
.stApp .stButton>button:contains("Next") {
    padding: 0.2rem 0.6rem !important;
    font-size: 0.8rem !important;
    min-height: 1.8rem !important;
    background: linear-gradient(135deg, #a8e6cf, #88d8c0) !important;
}

.stApp .stButton>button[kind="secondary"]:hover,
.stApp .stButton>button:contains("Previous"):hover,
.stApp .stButton>button:contains("Next"):hover {
    background: linear-gradient(135deg, #b8f6df, #98e8d0) !important;
    transform: scale(1.02) translateY(-1px) !important;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15), 0 2px 6px rgba(136, 216, 192, 0.3) !important;
}

/* Special buttons */
.stApp .stButton>button[data-testid*="read"],
.stApp .stButton>button[data-testid*="favorite"],
.stApp .stButton>button[data-testid*="settings"],
.stApp .stButton>button:contains("Read"),
.stApp .stButton>button:contains("❤️"),
.stApp .stButton>button:contains("⚙️") {
    background: linear-gradient(135deg, #ffcc70, #ff6ec4) !important;
    padding: 0.375rem 1rem !important;
    font-size: 0.9rem !important;
}

/* Ensure all text stays white and bold */
.stApp .stButton>button *,
.stApp .stDownloadButton>button * {
    color: white !important;
    font-weight: 600 !important;
}

/* BeluTales Navigation Button Styling */
.belu-nav-button {
    width: 200px !important;
    height: 40px !important;
    border-radius: 20px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    font-family: "Baloo 2", "Comic Neue", sans-serif !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-decoration: none !important;
}

/* Back to Stories Button */
.belu-back-button {
    background: linear-gradient(135deg, #a8e6cf, #88d8c0) !important;
    color: #2d5a4a !important;
}

.belu-back-button:hover {
    transform: scale(1.05) !important;
    background: linear-gradient(135deg, #b8f6df, #98e8d0) !important;
    box-shadow: 0 6px 16px rgba(168, 230, 207, 0.4) !important;
}

/* Pay with PayPal Button */
.belu-paypal-button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    width: 280px !important;
    height: 60px !important;
    border-radius: 30px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    font-family: "Baloo 2", "Comic Neue", sans-serif !important;
    border: none !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4), 0 0 20px rgba(118, 75, 162, 0.3) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
    letter-spacing: 0.5px !important;
}

.belu-paypal-button:hover {
    transform: scale(1.08) !important;
    background: linear-gradient(135deg, #7c8ef0, #8a5fb8) !important;
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6), 0 0 30px rgba(118, 75, 162, 0.5) !important;
    text-shadow: 0 2px 6px rgba(0,0,0,0.4) !important;
}

/* Premium Info Button */
.belu-premium-button {
    background: linear-gradient(135deg, #dda0dd, #98fb98) !important;
    color: #4a2c4a !important;
}

.belu-premium-button:hover {
    transform: scale(1.05) !important;
    background: linear-gradient(135deg, #e6b3e6, #a8f5a8) !important;
    box-shadow: 0 6px 16px rgba(221, 160, 221, 0.4) !important;
}

/* Button Container Centering */
.belu-button-container {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 15px !important;
    margin: 20px 0 !important;
    flex-wrap: wrap !important;
}

/* Single Button Centering */
.belu-single-button-container {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    margin: 20px 0 !important;
}
</style>
""", unsafe_allow_html=True)

from pathlib import Path
import unicodedata
import re
import math
import io
import os
from typing import List, Dict, Optional, Set
from PIL import Image, ImageOps
from dataclasses import dataclass
import time
import random
import subprocess
import threading
import requests
import atexit
import hashlib
import hmac
import secrets
from contextlib import closing

# Import performance optimizations
from utils.performance import (
    load_story_index, load_story_full, get_thumbnail, get_clients,
    debounce_search, get_pagination_info, apply_filters_optimized,
    get_categories_optimized, render_pagination_controls, get_current_page,
    clear_cache, PAGE_SIZE
)

# Development helper function for cache management
def reset_cache():
    """
    Clear all caches - for development use only.
    Call this function manually if needed during development.
    """
    clear_cache()
    st.rerun()




# Quiz helper functions
def _normalize_id(s: str) -> str:
    return (s or "").lower().replace("_", "-")

def load_quiz_data():
    """Robustly load quizzes.json from root or stories/."""
    for path in ["quizzes.json", os.path.join("stories", "quizzes.json")]:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data
            except Exception:
                pass
    return []

def get_story_quiz(story_id: str):
    data = load_quiz_data()
    sid = _normalize_id(story_id)
    for q in data:
        if _normalize_id(q.get("story_id")) == sid:
            # shallow copy + shuffle each question's options safely
            qs = []
            for item in q.get("questions", [])[:3]:
                opts = list(item.get("options", []))
                random.shuffle(opts)
                qs.append({"q": item.get("q",""), "options": opts, "answer": item.get("answer","")})
            return qs[:3]
    return []

def ensure_quiz_state(key_prefix: str = "quiz"):
    ss = st.session_state
    for k, v in {
        f"{key_prefix}_index": 0,
        f"{key_prefix}_score": 0,
        f"{key_prefix}_locked": False,
        f"{key_prefix}_selected": None,
        f"{key_prefix}_done": False,
    }.items():
        if k not in ss:
            ss[k] = v

def reset_quiz_state(key_prefix: str = "quiz"):
    for k in [f"{key_prefix}_index", f"{key_prefix}_score", f"{key_prefix}_locked", f"{key_prefix}_selected", f"{key_prefix}_done"]:
        st.session_state[k] = 0 if "score" in k or "index" in k else (False if "locked" in k or "done" in k else None)

def render_quiz(story_id: str, key_prefix: str = "quiz"):
    ensure_quiz_state(key_prefix)
    idx_key = f"{key_prefix}_index"
    score_key = f"{key_prefix}_score"
    locked_key = f"{key_prefix}_locked"
    sel_key = f"{key_prefix}_selected"
    done_key = f"{key_prefix}_done"

    questions = get_story_quiz(story_id)
    total = len(questions)

    # If no quiz questions, show a friendly notice and exit.
    if total == 0:
        st.info("🧩 No quiz available for this story yet.")
        return

    # Header + progress
    st.markdown(
        """
        <style>
        .quiz-card{padding:18px 20px;border-radius:18px;background:rgba(255,255,255,0.06);backdrop-filter:blur(6px);}
        .quiz-opt button{
            width: 100%;
            padding: 12px 16px;
            border-radius: 20px;
            font-size: 0.95rem;
            font-weight: 600;
            font-family: 'Comic Neue', 'Baloo 2', cursive;
            border: 2px solid transparent;
            background: linear-gradient(135deg, #FFB6C1, #87CEEB);
            color: #2E2A65;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            min-height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .quiz-opt button:hover{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255,182,193,0.4);
            background: linear-gradient(135deg, #FF9AA2, #74C0FC);
            border-color: #FF6B9D;
            animation: glow 0.6s ease-in-out;
        }
        .quiz-opt button:active{
            transform: translateY(0px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        @keyframes glow {
            0% { box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            50% { box-shadow: 0 8px 30px rgba(255,107,157,0.6); }
            100% { box-shadow: 0 8px 25px rgba(255,182,193,0.4); }
        }
        .spacer{height:8px;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.progress((st.session_state[idx_key])/max(1,total), text=f"Question {st.session_state[idx_key]+1 if st.session_state[idx_key]<total else total} of {total}")

    # Finished view
    if st.session_state[done_key] or st.session_state[idx_key] >= total:
        score = st.session_state[score_key]
        st.markdown("### 🌟 Quiz Complete!")
        st.markdown(f"**You got {score} / {total} correct.**")
        if score == total:
            st.balloons()
            st.success("Amazing! Perfect score! 🌈")
        colA, colB = st.columns([1,1])
        with colA:
            if st.button("🔁 Retry Quiz"):
                reset_quiz_state(key_prefix)
                st.rerun()
        with colB:
            st.markdown("")  # keep layout balanced
        return

    q = questions[st.session_state[idx_key]]
    st.markdown(f"### 🎯 {q['q']}")
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    # Options grid
    cols = st.columns(3)
    for i, opt in enumerate(q["options"][:3]):
        with cols[i]:
            disabled = st.session_state[locked_key]
            clicked = st.button(opt, key=f"{key_prefix}_opt_{st.session_state[idx_key]}_{i}", disabled=disabled)
            if clicked and not disabled:
                # Play click sound effect
                try:
                    play_click_sound()
                except:
                    pass  # Gracefully handle if audio is not available
                
                st.session_state[sel_key] = opt
                # lock buttons for feedback
                st.session_state[locked_key] = True
                if opt == q["answer"]:
                    st.session_state[score_key] += 1
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Try again!")
                    # allow retry on wrong; unlock after a brief moment
                    time.sleep(0.2)
                    st.session_state[locked_key] = False

    # If correct (locked True and selected is the correct answer), show Next
    if st.session_state[locked_key] and st.session_state[sel_key] == q["answer"]:
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        if st.button("➡️ Next question"):
            st.session_state[idx_key] += 1
            st.session_state[locked_key] = False
            st.session_state[sel_key] = None
            if st.session_state[idx_key] >= total:
                st.session_state[done_key] = True
            st.rerun()

_EMOJI_RE = re.compile(
    r"[\U0001F1E6-\U0001F1FF"   # flags
    r"\U0001F300-\U0001F5FF"    # symbols & pictographs
    r"\U0001F600-\U0001F64F"    # emoticons
    r"\U0001F680-\U0001F6FF"    # transport & map
    r"\U0001F700-\U0001F77F"
    r"\U0001F780-\U0001F7FF"
    r"\U0001F800-\U0001F8FF"
    r"\U0001F900-\U0001F9FF"
    r"\U0001FA00-\U0001FAFF"
    r"\u2600-\u26FF"            # misc symbols
    r"\u2700-\u27BF"            # dingbats
    r"]"
)

def has_emoji(s: str) -> bool:
    return bool(_EMOJI_RE.search(s or ""))

def norm_cat(s: str) -> str:
    txt = unicodedata.normalize("NFKD", s or "")
    txt = _EMOJI_RE.sub("", txt)                 # strip emoji
    txt = re.sub(r"[^A-Za-z\s\-]", "", txt)      # keep letters/spaces/hyphens
    txt = re.sub(r"\s+", " ", txt).strip().lower()
    return txt

def dedup_with_emoji_priority(options: list[str]) -> list[str]:
    items = [str(o).strip() for o in (options or []) if str(o).strip()]
    if not any(i.lower() == "all" for i in items):
        items.insert(0, "All")
    chosen = {}
    order = []
    for label in items:
        key = "all" if label.lower() == "all" else norm_cat(label)
        if key not in order:
            order.append(key)
        keep = chosen.get(key)
        if keep is None or (has_emoji(label) and not has_emoji(keep)):
            chosen[key] = label   # prefer emoji version
    final = []
    if "all" in chosen:
        final.append(chosen["all"])
    for k in order:
        if k == "all": continue
        final.append(chosen[k])
    return final

# Canonical categories and emoji display labels
CATEGORY_EMOJI = {
    "All": "All",
    "Favorites": "🌟 Favorites",
    "Adventure": "🌞 Adventure", 
    "Dreams": "🌙 Dreams",
    "Family": "🏡 Family",
    "Self-Discovery": "🌈 Self-Discovery",
}

def normalize_category(s: str) -> str:
    """Normalize category by trimming whitespace and title-casing"""
    if not s:
        return "General"
    return s.strip().title()

def category_label(canonical: str) -> str:
    """User-facing label with emoji for a canonical category key."""
    return CATEGORY_EMOJI.get(canonical, canonical)

@dataclass
class FilterState:
    """Holds all current filter selections for consistent filtering"""
    language: str = "English"
    story_type: str = "All"  # All, Free, Premium
    search_text: str = ""
    favorites_only: bool = False
    category: str = "All"
    favorite_ids: Optional[Set[str]] = None
    
    def __post_init__(self):
        if self.favorite_ids is None:
            self.favorite_ids = set()

def apply_filters(stories: List[Dict], fs: FilterState, ignore_category: bool = False) -> List[Dict]:
    """Apply unified filtering logic to stories based on FilterState"""
    filtered = []
    
    for story in stories:
        # Language filter (if multiple languages supported)
        # Note: Currently language is applied via translation, not filtering
        # This could be extended to filter by story language if needed
        
        # Type filter (Free/Premium) - All stories are now free
        # if fs.story_type == "Free" and story.get("is_premium", False):
        #     continue
        # if fs.story_type == "Premium" and not story.get("is_premium", False):
        #     continue
        
        # Search text filter
        if fs.search_text:
            searchable = f"{story.get('title', '')} {story.get('category', '')}".lower()
            if fs.search_text.lower() not in searchable:
                continue
        
        # Favorites filter
        if fs.favorites_only and story.get("title") not in fs.favorite_ids:
            continue
        
        # Category filter (unless ignored for category counting)
        if not ignore_category and fs.category != "All":
            story_canonical_cat = normalize_category(story.get("category", "General"))
            filter_canonical_cat = normalize_category(fs.category)
            if story_canonical_cat != filter_canonical_cat:
                continue
        
        filtered.append(story)
    
    return filtered

from utils.image_loader import load_image_safe
from utils.categories import load_stories_json, category_counts

# Import language support
try:
    from languages import LANGUAGES, RTL_LANGUAGES, get_language_code, get_language_display
    LANGUAGES_AVAILABLE = True
except ImportError:
    LANGUAGES_AVAILABLE = False
    LANGUAGES = {"English": {"code": "en", "flag": "🇬🇧"}}
    RTL_LANGUAGES = []

# Import translation support
try:
    from utils.translator import translate_text
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    def translate_text(text: str, target_language: str) -> str:
        return text

# Import TTS support
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# Import enhanced components (graceful fallback if not available)
try:
    from components.audio_manager import AudioManager, play_click_sound, play_success_sound
    from components.quiz_enhanced import render_quiz_enhanced, get_quiz_progress
    from components.settings_panel import render_settings_panel
    ENHANCED_FEATURES = True
except ImportError:
    ENHANCED_FEATURES = False
    def play_click_sound(): pass
    def play_success_sound(): pass
    def render_settings_panel(): 
        st.write("Enhanced settings not available")
    AudioManager = None

# Import PayPal integration
try:
    from paypal_integration import (
        init_paypal_session, 
        is_premium_active, 
        render_premium_unlock_page,
        check_payment_status,
        get_premium_stats
    )
    PAYPAL_AVAILABLE = True
except ImportError:
    PAYPAL_AVAILABLE = False
    def init_paypal_session(): pass
    def is_premium_active(): return False
    def render_premium_unlock_page(story): st.warning("PayPal integration not available")
    def check_payment_status(): pass
    def get_premium_stats(): return {"active": False}


# Backend server management
BACKEND_URL = "http://localhost:8000"
BACKEND_PROCESS = None
BACKEND_STARTED = False

def check_backend_health():
    """Check if the backend server is running and healthy"""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_backend_server():
    """Start the PayPal backend server using subprocess"""
    global BACKEND_PROCESS, BACKEND_STARTED
    
    if BACKEND_STARTED:
        return True
    
    try:
        # Check if server is already running
        if check_backend_health():
            BACKEND_STARTED = True
            return True
        
        # Start the server in a subprocess
        BACKEND_PROCESS = subprocess.Popen(
            ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if server started successfully
        if check_backend_health():
            BACKEND_STARTED = True
            return True
        else:
            # Server failed to start
            if BACKEND_PROCESS:
                BACKEND_PROCESS.terminate()
                BACKEND_PROCESS = None
            return False
            
    except Exception as e:
        st.error(f"Failed to start backend server: {e}")
        return False

def stop_backend_server():
    """Stop the backend server"""
    global BACKEND_PROCESS, BACKEND_STARTED
    
    if BACKEND_PROCESS:
        try:
            BACKEND_PROCESS.terminate()
            BACKEND_PROCESS.wait(timeout=5)
        except subprocess.TimeoutExpired:
            BACKEND_PROCESS.kill()
        except Exception:
            pass
        finally:
            BACKEND_PROCESS = None
            BACKEND_STARTED = False

def ensure_backend_running():
    """Ensure backend is running, start if needed"""
    if not check_backend_health():
        if not start_backend_server():
            st.warning("⚠️ PayPal backend server is not available. Premium features may not work.")
            return False
    return True

# Register cleanup function
atexit.register(stop_backend_server)




    
    # Add playful button click sounds
button_sounds_js = """
    <script>
    // Initialize button click sounds for BeluTales
    (function() {
        // Prevent multiple sound system initializations
        if (window.beluButtonSoundsInitialized) {
            return;
        }
        window.beluButtonSoundsInitialized = true;
        
        // Create audio element for button clicks
        const clickSound = new Audio('assets/sounds/click.mp3');
        clickSound.preload = 'auto';
        clickSound.volume = 0.3; // Gentle volume for kids
        
        // Function to play click sound
        function playClickSound() {
            try {
                clickSound.currentTime = 0; // Reset to start for rapid clicks
                clickSound.play().catch(e => {
                    // Silently handle autoplay restrictions
                    console.log('Sound play prevented by browser policy');
                });
            } catch (e) {
                // Silently handle any audio errors
            }
        }
        
        // Function to add click sound to buttons
        function addSoundToButtons() {
            // Select all Streamlit buttons
            const buttons = document.querySelectorAll(
                '.stButton > button, ' +
                '.stDownloadButton > button, ' +
                'button[data-testid*="button"], ' +
                'button[kind="primary"], ' +
                'button[kind="secondary"]'
            );
            
            buttons.forEach(button => {
                // Check if sound event already added
                if (!button.hasAttribute('data-belu-sound-added')) {
                    // Add click event listener
                    button.addEventListener('click', function(e) {
                        playClickSound();
                    }, { passive: true });
                    
                    // Mark as processed
                    button.setAttribute('data-belu-sound-added', 'true');
                }
            });
        }
        
        // Initialize sounds when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', addSoundToButtons);
        } else {
            addSoundToButtons();
        }
        
        // Re-scan for new buttons when Streamlit updates the page
        const observer = new MutationObserver(function(mutations) {
            let shouldRescan = false;
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    // Check if any buttons were added
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // Element node
                            if (node.matches && 
                                (node.matches('button') || 
                                 node.querySelector && node.querySelector('button'))) {
                                shouldRescan = true;
                            }
                        }
                    });
                }
            });
            
            if (shouldRescan) {
                // Small delay to let Streamlit finish rendering
                setTimeout(addSoundToButtons, 100);
            }
        });
        
        // Observe the main app container for changes
        const appContainer = document.querySelector('.stApp');
        if (appContainer) {
            observer.observe(appContainer, {
                childList: true,
                subtree: true
            });
        }
        
        // Enable audio context on first user interaction (for browsers with autoplay restrictions)
        function enableAudioContext() {
            clickSound.play().then(() => {
                clickSound.pause();
                clickSound.currentTime = 0;
            }).catch(() => {
                // Audio context will be enabled on actual button clicks
            });
            
            // Remove this one-time listener
            document.removeEventListener('click', enableAudioContext);
            document.removeEventListener('touchstart', enableAudioContext);
        }
        
        // Add one-time listeners to enable audio context
        document.addEventListener('click', enableAudioContext, { once: true });
        document.addEventListener('touchstart', enableAudioContext, { once: true });
        
    })();
    </script>
    """
    st.markdown(button_sounds_js, unsafe_allow_html=True)

# Inject premium theme immediately (every run to prevent background disappearing)
inject_premium_theme()

# Custom fonts and sounds
from utils.ui import inject_fonts_and_sounds, story_container_open
# Quiz system is now implemented directly in app.py
inject_fonts_and_sounds()

# BeluTales Unified CSS and JavaScript System (duplicate - will be removed)
OLD_CSS = """
<style>
/* Import kid-friendly Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Nunito:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #1e1b4b;
    --card: #2e2a65;
    --text: #ffffff;
    --muted: #d1d5db;
    --accent: #facc15;
    --sky: #38bdf8;
    --pink: #f472b6;
    --success: #34d399;
    
    /* Enhanced font stack */
    --font-heading: 'Baloo 2', 'Comic Sans MS', cursive, sans-serif;
    --font-body: 'Nunito', 'Trebuchet MS', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, var(--bg) 0%, #312e81 50%, var(--bg) 100%);
    color: var(--text);
    font-family: var(--font-body) !important;
    font-weight: 500;
}

/* FORCE fonts on ALL elements - comprehensive override */
*, .stApp, .stApp *, .stMarkdown, .stMarkdown *, 
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] *,
[data-testid="stSidebar"], [data-testid="stSidebar"] *,
.css-1d391kg *, .css-1cypcdb *, p, div, span {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
}

/* FORCE heading fonts - comprehensive override */
h1, h2, h3, h4, h5, h6,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
[data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3, [data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5, [data-testid="stMarkdownContainer"] h6,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: var(--text) !important;
    font-family: var(--font-heading) !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
}

h1 { 
    font-size: 2.5rem; 
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

h2 { 
    font-size: 2rem; 
}

h3 { 
    font-size: 1.5rem; 
}

/* Story text enhanced readability */
.story-text {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    font-size: 1.2rem !important;
    line-height: 1.8 !important;
    letter-spacing: 0.3px !important;
    text-align: justify;
    color: #e9ecff;
    text-indent: 20px;
    margin-bottom: 20px;
}

.header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin: 20px 0;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
    font-size: 48px;
    padding: 10px;
    border-radius: 15px;
    background: linear-gradient(135deg, var(--accent), var(--sky));
}

.title {
    font-family: var(--font-heading);
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(45deg, var(--accent), var(--sky), var(--pink));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    letter-spacing: 1px;
    text-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.subtitle {
    color: var(--muted);
    font-style: italic;
}

/* Enhanced buttons with click sounds and better fonts */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--sky)) !important;
    color: #1e1b4b !important;
    border-radius: 16px !important;
    border: none !important;
    padding: 12px 24px !important;
    font-family: var(--font-heading) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 20px rgba(250, 204, 21, 0.4) !important;
    background: linear-gradient(135deg, var(--sky), var(--pink)) !important;
}

.stButton > button:active {
    transform: translateY(-1px) scale(0.98) !important;
    transition: all 0.1s ease !important;
}

/* Click sound integration for buttons */
.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s ease;
}

.stButton > button:hover::before {
    left: 100%;
}

/* Enhanced form inputs with better fonts */
.stSelectbox > div > div,
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input::placeholder {
    color: var(--muted) !important;
    font-family: var(--font-body) !important;
    font-weight: 400 !important;
}

.stSelectbox > div > div:focus,
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(250, 204, 21, 0.2) !important;
    outline: none !important;
}

/* Enhanced story cards with better fonts */
.story-card {
    background: linear-gradient(135deg, var(--card), rgba(46, 42, 101, 0.8));
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    padding: 20px;
    margin: 12px 0;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
}

.story-card:hover {
    transform: translateY(-6px) scale(1.02);
    border-color: var(--accent);
    box-shadow: 0 12px 32px rgba(250, 204, 21, 0.3);
}

.story-card h1, .story-card h2, .story-card h3 {
    font-family: var(--font-heading);
    font-weight: 700;
}

.story-text {
    font-family: var(--font-body);
    font-weight: 500;
    line-height: 1.8;
    font-size: 1.125rem;
    text-align: justify;
    color: #e9ecff;
    text-indent: 20px;
    margin-bottom: 20px;
    letter-spacing: 0.3px;
}

/* Enhanced captions and metadata */
.stCaption {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

/* Click sound integration script */
</style>

<script>
// Enhanced click sound system with simpler, more reliable audio
function playClickSound() {
    // Check if sounds are enabled (default to true if not set)
    const soundsEnabled = window.sessionStorage.getItem('sfx_enabled') !== 'false';
    if (!soundsEnabled) return;
    
    // Create a simple click sound using Web Audio API
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        // Create a pleasant click sound
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.1);
        
        const volume = parseFloat(window.sessionStorage.getItem('volume') || '0.2');
        gainNode.gain.setValueAtTime(volume, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.1);
        
        oscillator.type = 'sine';
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    } catch (e) {
        // Fallback: try HTML5 audio with a shorter beep
        try {
            const audio = new Audio('data:audio/wav;base64,UklGRu4CAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YcoCAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSyCz/LdeSQGLIXO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaqfp8LNwJANEoeH1NwUJKo/M8tlxOAoeXqzp8KlYDwNMmt/zxXEqBCuEzfLaeCUGLYHO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaqfp8LNwJANEoeH1NwUJKo/M8tlxOAoeXqzp8KlYDwNMmt/zxXEqBCuEzfLaeCUGLYHO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaqfp8LNwJANEoeH1NwUJKo/M8tlxOAoeXqzp8KlYDwNMmt/zxXEqBCuEzfLaeCUGLYHO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaqfp8LNwJANEoeH1NwUJKo/M8tlxOAoeXqzp8KlYDwNMmt/zxXEqBCuEzfLaeCUGLYHO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaqfp8LNwJANEoeH1NwUJKo/M8tlxOAoeXqzp8KlYDwNMmt/zxXEqBCuEzfLaeCUGLYHO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaqfp8LNwJANEoeH1NwUJKo/M8tlxOAoeXqzp8KlYDwNMmt/zxXEqBCuEzfLaeCUGLYHO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaqfp8LNwJANEoeH1NwUJKo/M8tlxOAoeXqzp8KlYDwNMmt/zxXEqBCuEzfLaeCUGLYHO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaqfp8LNwJANEoeH1NwUJKo/M8tlxOAoeXqzp8KlYDwNMmt/zxXEqBCuEzfLaeCUGLYHO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaqfp8LNwJANEoeH1NwUJKo/M8tlxOAoeXqzp8KlYDwNMmt/zxXEqBCuEzfLaeCUGLYHO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaqfp8LNwJANEoeH1NwUJKo/M8tlxOAoeXqzp8KlYDwNMmt/zxXEqBCuEzfLaeCUGLYHO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJysO7nq1kVCECU4PLJayoUXKzj9Lh4IAYieclxNwtOuO/nsFUVCjeN0PHKdywGHW3d9KJVFUJGn+FxOPNOSnjD9Kx2IAUihM9xOAsJaq');
            audio.volume = parseFloat(window.sessionStorage.getItem('volume') || '0.2');
            audio.play().catch(() => {});
        } catch (e2) {
            console.log('Audio not available');
        }
    }
}

// Add click sound to all buttons when they're clicked
document.addEventListener('click', function(e) {
    if (e.target.matches('button') || e.target.closest('button')) {
        playClickSound();
    }
});

// Add click sound to language selector
document.addEventListener('change', function(e) {
    if (e.target.matches('select') || e.target.closest('.stSelectbox')) {
        playClickSound();
    }
});

// Sync Streamlit session state with browser storage for settings
function syncSettings() {
    // This would be called when settings change in Streamlit
    const sfxEnabled = window.parent.document.querySelector('[data-testid="stCheckbox"] input')?.checked || true;
    window.sessionStorage.setItem('sfx_enabled', sfxEnabled.toString());
    
    // Sync volume if available
    const volumeSlider = window.parent.document.querySelector('[data-testid="stSlider"] input');
    if (volumeSlider) {
        window.sessionStorage.setItem('volume', volumeSlider.value);
    }
}

// Initial sync
setTimeout(syncSettings, 1000);
</script>
</style>
"""

# BeluTales Unified CSS and JavaScript System
UNIFIED_CSS_JS = """
<!-- Preconnect to Google Fonts for faster loading -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Nunito:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Nunito:wght@400;500;600;700;800&display=swap">

<style>

:root {
    --bg: #1e1b4b;
    --card: #2e2a65;
    --text: #ffffff;
    --muted: #d1d5db;
    --accent: #facc15;
    --sky: #38bdf8;
    --pink: #f472b6;
    --success: #34d399;
    
    /* Enhanced font stack */
    --font-heading: 'Baloo 2', 'Comic Sans MS', cursive, sans-serif;
    --font-body: 'Nunito', 'Trebuchet MS', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, var(--bg) 0%, #312e81 50%, var(--bg) 100%);
    color: var(--text);
    font-family: var(--font-body) !important;
    font-weight: 500;
}

/* FORCE fonts on ALL elements - comprehensive override */
*, .stApp, .stApp *, .stMarkdown, .stMarkdown *, 
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] *,
[data-testid="stSidebar"], [data-testid="stSidebar"] *,
.css-1d391kg *, .css-1cypcdb *, p, div, span {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
}

/* FORCE heading fonts - comprehensive override */
h1, h2, h3, h4, h5, h6,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
[data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3, [data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5, [data-testid="stMarkdownContainer"] h6,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: var(--text) !important;
    font-family: var(--font-heading) !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
}

h1 { 
    font-size: 2.5rem; 
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

h2 { 
    font-size: 2rem; 
}

h3 { 
    font-size: 1.5rem; 
}

/* Story text enhanced readability */
.story-text {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    font-size: 1.2rem !important;
    line-height: 1.8 !important;
    letter-spacing: 0.3px !important;
    text-align: justify;
    color: #e9ecff;
    text-indent: 20px;
    margin-bottom: 20px;
}

.header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin: 20px 0;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
    font-size: 48px;
    padding: 10px;
    border-radius: 15px;
    background: linear-gradient(135deg, var(--accent), var(--sky));
}

.title {
    font-family: var(--font-heading);
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(45deg, var(--accent), var(--sky), var(--pink));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    letter-spacing: 1px;
    text-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.subtitle {
    color: var(--muted);
    font-style: italic;
}

/* Enhanced buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--sky)) !important;
    color: #1e1b4b !important;
    border-radius: 16px !important;
    border: none !important;
    padding: 12px 24px !important;
    font-family: var(--font-heading) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 20px rgba(250, 204, 21, 0.4) !important;
    background: linear-gradient(135deg, var(--sky), var(--pink)) !important;
}

.stButton > button:active {
    transform: translateY(-1px) scale(0.98) !important;
    transition: all 0.1s ease !important;
}

/* Enhanced form inputs */
.stSelectbox > div > div,
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input::placeholder {
    color: var(--muted) !important;
    font-family: var(--font-body) !important;
    font-weight: 400 !important;
}

.stSelectbox > div > div:focus,
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(250, 204, 21, 0.2) !important;
    outline: none !important;
}

/* Enhanced story cards */
.story-card {
    background: linear-gradient(135deg, var(--card), rgba(46, 42, 101, 0.8));
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    padding: 20px;
    margin: 12px 0;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
}

.story-card:hover {
    transform: translateY(-6px) scale(1.02);
    border-color: var(--accent);
    box-shadow: 0 12px 32px rgba(250, 204, 21, 0.3);
}

.story-card h1, .story-card h2, .story-card h3 {
    font-family: var(--font-heading);
    font-weight: 700;
}

/* Enhanced captions and metadata */
.stCaption {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}
</style>

<script>
// BeluTales Unified Audio & Font System
console.log('🎨 BeluTales Unified System Loading...');

class BeluTalesSystem {
    constructor() {
        this.audioEnabled = true;
        this.volume = 0.3;
        this.clickAudio = null;
        this.init();
    }
    
    init() {
        // Load click.mp3 file
        try {
            this.clickAudio = new Audio('./audio/click.mp3');
            this.clickAudio.volume = this.volume;
            this.clickAudio.preload = 'none';
            console.log('✅ Loaded click.mp3');
        } catch (e) {
            console.log('⚠️ click.mp3 not available, using fallback');
        }
        
        this.syncWithSessionStorage();
        this.attachEventListeners();
        this.monitorSettings();
    }
    
    syncWithSessionStorage() {
        // Read from sessionStorage (synced from Settings panel)
        this.audioEnabled = sessionStorage.getItem('sfx_enabled') !== 'false';
        this.volume = parseFloat(sessionStorage.getItem('volume') || '0.3');
        
        if (this.clickAudio) {
            this.clickAudio.volume = this.volume;
        }
    }
    
    attachEventListeners() {
        // Attach to all buttons and selects
        document.addEventListener('click', (e) => {
            if (e.target.matches('button') || e.target.closest('button')) {
                this.playClick();
            }
        });
        
        document.addEventListener('change', (e) => {
            if (e.target.matches('select') || e.target.closest('.stSelectbox')) {
                this.playClick();
            }
        });
    }
    
    playClick() {
        if (!this.audioEnabled) return;
        
        // Try click.mp3 first
        if (this.clickAudio) {
            try {
                this.clickAudio.currentTime = 0;
                this.clickAudio.volume = this.volume;
                this.clickAudio.play().catch(() => {
                    this.playFallbackBeep();
                });
                return;
            } catch (e) {
                // Fall through to WebAudio beep
            }
        }
        
        this.playFallbackBeep();
    }
    
    playFallbackBeep() {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.1);
            
            gainNode.gain.setValueAtTime(this.volume, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.1);
            
            oscillator.type = 'sine';
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.1);
        } catch (e) {
            console.log('Audio unavailable');
        }
    }
    
    monitorSettings() {
        // Monitor Streamlit settings changes
        setInterval(() => {
            this.syncWithSessionStorage();
        }, 1000);
    }
}

// Initialize system
const beluTalesSystem = new BeluTalesSystem();

// Settings sync function for Streamlit to call
window.updateBeluTalesSettings = function(sfxEnabled, volume) {
    sessionStorage.setItem('sfx_enabled', sfxEnabled.toString());
    sessionStorage.setItem('volume', volume.toString());
    beluTalesSystem.syncWithSessionStorage();
};

console.log('🚀 BeluTales System Ready!');
</script>
"""

# Inject CSS/JS only once per session
if not st.session_state.get("_assets_injected"):
    st.markdown(UNIFIED_CSS_JS, unsafe_allow_html=True)
    st.session_state["_assets_injected"] = True

# Helper functions
def slugify(name: str) -> str:
    """Convert story title to URL-friendly slug"""
    s = unicodedata.normalize("NFKC", name).lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s or "story"

def seeded_rand(slug: str):
    """Create a seeded random generator for consistent quiz questions"""
    import hashlib
    import random
    seed = int(hashlib.sha256(slug.encode("utf-8")).hexdigest(), 16) % (2**32)
    return random.Random(seed)

# Quiz functions moved to components/quiz.py for modularity

# Story loading is now handled by load_story_index() and load_story_full() in utils/performance.py
# This function is kept for backward compatibility but redirects to optimized version
@st.cache_data
def load_stories() -> List[Dict]:
    """Load stories from stories.json - DEPRECATED: Use load_story_index() for list view"""
    return load_story_index()

@st.cache_data
def load_favorites() -> set:
    """Load favorites from favorites.json"""
    try:
        favorites_file = Path("favorites.json")
        if favorites_file.exists():
            with open(favorites_file, "r", encoding="utf-8") as f:
                return set(json.load(f))
        return set()
    except Exception:
        return set()

def save_favorites(favorites: set):
    """Save favorites to favorites.json"""
    try:
        with open("favorites.json", "w", encoding="utf-8") as f:
            json.dump(list(favorites), f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Failed to save favorites: {e}")

@st.cache_resource
def load_image(image_path: str, size=(800, 600)):
    """Load image or return placeholder if not found"""
    if image_path and Path(image_path).exists():
        try:
            img = Image.open(image_path)
            return img
        except Exception:
            pass
    # Create placeholder image
    img = Image.new("RGB", size, (30, 27, 75))  # Dark blue placeholder
    return img

# get_thumbnail function moved to utils/performance.py for better organization

def show_image_resilient(path_or_bytes, caption=None):
    """Display image with robust error handling and fallback"""
    img = load_image_safe(path_or_bytes)
    if img is None:
        # Use fallback and log a warning in the UI (not a crash)
        fallback_path = Path("assets/fallback.png")
        try:
            fallback = Image.open(fallback_path)
            st.warning("Some illustrations couldn't be decoded. Showing a placeholder instead.")
            st.image(fallback, use_container_width=True, caption=caption)
    except Exception:
            st.warning("Image failed to load and no fallback available.")
        return
    st.image(img, use_column_width=True, caption=caption)


@st.cache_resource
def get_tts_engine(lang_code: str):
    """Get cached TTS engine for language"""
    if not TTS_AVAILABLE:
        return None
    return gTTS(text="", lang=lang_code, slow=False)

@st.cache_resource
def generate_audio(text: str, language: str, story_slug: str) -> str:
    """Generate audio file for story text"""
    if not TTS_AVAILABLE:
        return None
    
    try:
        # Create audio directory if it doesn't exist
        audio_dir = Path("audio")
        audio_dir.mkdir(exist_ok=True)
        
        # Get language code for TTS
        lang_code = LANGUAGES.get(language, {}).get("code", "en")
        filename = f"{story_slug}_{lang_code}.mp3"
        filepath = audio_dir / filename
        
        # Return existing file if it exists
        if filepath.exists():
            return str(filepath)
        
        # Generate new audio file
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(str(filepath))
        return str(filepath)
    except Exception:
        return None

# Authentication UI Functions
# New Auth UI Functions
def render_guest_mode():
    # Guest mode button is now handled in render_header() to avoid duplicates
    pass


# Top navigation (replace your current "Stories | Login | Sign Up" row)
def render_header():
    st.markdown("""
    <div class="header">
        <div class="logo">🦉</div>
        <div>
            <div class="title">BeluTales</div>
            <div class="subtitle">Magical bedtime stories for kids</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome banner
    st.markdown("""
    <div style="text-align: center; margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);">
        <p style="color: white; font-size: 18px; font-weight: bold; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3); font-family: 'Comic Sans MS', cursive;">
            ✨ Unlock 100+ magical stories, quizzes, and narrations — forever with one payment.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1.2,0.9,1.0])
    with c1:
        if st.button("📚 Stories", use_container_width=True):
            _go("stories")
    with c2:
        st.markdown("### ✨ All Stories Free! ✨")
    with c3:
        st.markdown("### 🎉 Enjoy Reading! 🎉")
    
    # Language selector and settings
    if LANGUAGES_AVAILABLE:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            # Create language options with flags
            language_options = []
            for lang_name, lang_data in LANGUAGES.items():
                flag = lang_data.get("flag", "🌐")
                language_options.append(f"{flag} {lang_name}")
            
            selected_display = st.selectbox(
                "🌐 Language",
                language_options,
                index=0,
                key="language_selector"
            )
            
            # Extract language name from display
            selected_language = selected_display.split(" ", 1)[1] if " " in selected_display else "English"
            st.session_state["selected_language"] = selected_language
        
        with col3:
            # Settings panel integration with enhanced features
            if ENHANCED_FEATURES:
                with st.popover("⚙️ Settings"):
                    render_settings_panel()
            else:
                # Enhanced fallback settings with font and sound controls
                with st.popover("⚙️ Settings"):
                    st.markdown("### ⚙️ BeluTales Settings")
                    
                    # Premium Status
                    if PAYPAL_AVAILABLE:
                        premium_stats = get_premium_stats()
                        if premium_stats["active"]:
                            st.success("✅ Premium Active")
                            if premium_stats["expires"]:
                                st.caption(f"Expires: {premium_stats['expires']}")
                        else:
                            st.info("💎 Premium: Inactive")
                        st.markdown("---")
                    
                    # Audio Settings
                    st.markdown("**🔊 Audio**")
                    sfx_enabled = st.toggle(
                        "Click Sounds", 
                        key="sfx_enabled", 
                        value=st.session_state.get("sfx_enabled", True),
                        help="Play soft click sounds when navigating"
                    )
                    
                    if sfx_enabled:
                        volume = st.slider(
                            "Sound Volume",
                            min_value=0.0,
                            max_value=1.0,
                            value=st.session_state.get("volume", 0.3),
                            step=0.1,
                            key="volume"
                        )
                    
                    # Sync settings with JavaScript audio system
                    if "sfx_enabled" in st.session_state and "volume" in st.session_state:
                        st.markdown(f"""
                        <script>
                        // Update BeluTales audio settings
                        if (window.updateBeluTalesSettings) {{
                            window.updateBeluTalesSettings({str(st.session_state.sfx_enabled).lower()}, {st.session_state.volume});
                        }}
                        </script>
                        """, unsafe_allow_html=True)
                    
                    # Change Password (only for logged in users)
                    if st.session_state.get("user_logged_in", False):
                        st.markdown("**🔐 Account**")
                        with st.expander("Change Password", expanded=False):
                            st.info("Password change functionality will be available in a future update.")
                    
                    # Display Settings
                    st.markdown("**🎨 Display**")
                    st.info("Enhanced fonts: Baloo 2 (headings) + Nunito (body text)")
                    st.caption("Premium Google Fonts loaded for better readability")
    else:
        st.session_state["selected_language"] = "English"

@st.cache_data(ttl=3600)
def get_categories(stories: tuple) -> List[str]:
    """Get unique categories from stories"""
    categories = {"All"}
    for story in stories:
        categories.add(story.get("category", "General"))
    return sorted(list(categories))

@st.cache_data(ttl=300)
def get_categories_with_counts(stories: List[Dict], current_fs=None) -> dict:
    """Get categories with counts using Counter for consistent counting"""
    from collections import Counter
    
    # Get all stories that match filters except category
    if current_fs:
        base_filtered = apply_filters(stories, current_fs, ignore_category=True)
    else:
        base_filtered = stories
    
    # Collect all normalized categories from stories
    categories = [normalize_category(story.get("category", "General")) for story in base_filtered]
    counts = Counter(categories)
    counts = dict(sorted(counts.items()))
    counts = {"All": len(stories), **counts}
    return counts

@st.cache_data(ttl=300)
def filter_stories(stories: tuple, query: str, category: str, favorites_tuple: tuple, show_favorites_only: bool, premium_filter: str) -> List[Dict]:
    """Filter stories based on search criteria"""
    favorites = set(favorites_tuple) if favorites_tuple else set()
    filtered = []
    for story in stories:
        # Text search
        if query:
            searchable = f"{story.get('title', '')} {story.get('category', '')}".lower()
            if query.lower() not in searchable:
                continue
        
        # Category filter
        if category != "All" and story.get("category") != category:
            continue
            
        # Favorites filter
        if show_favorites_only and story.get("title") not in favorites:
            continue
            
        # Premium filter
        if premium_filter == "Free" and story.get("is_premium", False):
            continue
        if premium_filter == "Premium" and not story.get("is_premium", False):
            continue
            
        filtered.append(story)
    
    return filtered

# Initialize session state
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "list"

# Initialize audio settings with defaults
st.session_state.setdefault("sfx_enabled", True)
st.session_state.setdefault("volume", 0.3)

# Initialize pagination
st.session_state.setdefault("page", 1)

# Initialize authentication system

# Initialize session state keys
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "email" not in st.session_state:
    st.session_state["email"] = None
if "premium" not in st.session_state:
    st.session_state["premium"] = False
if "active_tab" not in st.session_state:
    st.session_state.active_tab = st.query_params.get("tab", ["stories"])[0]

# Restore user session from users.json file on startup
# This ensures accounts persist after reload

def _go(tab: str):
    st.session_state.active_tab = tab
    st.query_params.update({"tab": tab})
    st.rerun()

# Ensure backend is running before initializing PayPal
if PAYPAL_AVAILABLE:
    ensure_backend_running()

# Initialize PayPal session
init_paypal_session()

# Check for PayPal payment status
check_payment_status()

# Capture PayPal payment if returned
capture_paypal_if_returned()

# Handle PayPal redirect logic
if "paypal_approval_url" in st.session_state:
    import streamlit.components.v1 as components

    st.info("Redirecting to PayPal... Please complete your payment in the new window.")
    components.html(
        f"<script>window.open('{st.session_state['paypal_approval_url']}', '_blank').focus();</script>",
        height=0,
    )
    st.stop()

# Handle PayPal cancel page
query_params = st.query_params
if "cancel" in query_params:
    # Clear any stored order ID
    st.session_state["paypal_order_id"] = None
    st.session_state["premium"] = False
    
    st.markdown("## ❌ Payment was canceled")
    st.markdown("You can try again anytime.")
    
    # Centered back button
    st.markdown('<div class="belu-single-button-container">', unsafe_allow_html=True)
    if st.button("🏠 Back to Stories", key="cancel_back_btn", use_container_width=False):
        st.query_params.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()
if "current_story" not in st.session_state:
    st.session_state.current_story = None
if "favorites" not in st.session_state:
    st.session_state.favorites = load_favorites()

# ---- Handle PayPal success page early and exit cleanly ----
qp = st.query_params
is_success = (qp.get("success") == "1") or ("token" in qp and "PayerID" in qp)

if is_success:
    st.markdown(
        """
        <div style="margin:2rem auto; max-width:980px; padding:2rem 2.5rem; 
                    border-radius:22px; background:rgba(40,50,120,.35); 
                    box-shadow:0 6px 24px rgba(0,0,0,.25); text-align:center;">
            <div style="font-size:64px; line-height:1.1;">🎉</div>
            <h1 style="margin:.5rem 0 0; font-size:32px;">Premium Unlocked</h1>
            <p style="font-size:16px; opacity:.9; margin:1rem 0;">
                You now have lifetime premium access to all stories and features. Enjoy!
            </p>
            <div style="margin-top:16px; font-size:14px; opacity:.8;">
                Redirecting you back to your stories...
            </div>
            <div style="margin-top:12px;">
                <div class="loader"></div>
            </div>
        </div>

        <style>
        .loader {{
          border: 4px solid rgba(255, 255, 255, 0.3);
          border-top: 4px solid #00c3ff;
          border-radius: 50%;
          width: 28px;
          height: 28px;
          animation: spin 1s linear infinite;
          margin: 12px auto 0 auto;
        }}
        @keyframes spin {{
          0% {{ transform: rotate(0deg); }}
          100% {{ transform: rotate(360deg); }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <script>
        setTimeout(function(){
            window.location.href = "?tab=stories";
        }, 2500);
        </script>
        """,
        unsafe_allow_html=True,
    )

    st.stop()
# ---- end success handler ----

# Initialize authentication system

# Load stories using optimized performance functions
stories_index = load_story_index()  # Lightweight index for list view
stories_full = load_stories()  # Keep for backward compatibility

# Render header
render_header()

# All stories are now free - no authentication required

# Check view mode
if st.session_state.view_mode == "detail" and st.session_state.current_story:
    # Story detail view - use lazy loading for full story content
    story_id = st.session_state.current_story
    story = load_story_full(story_id)
    
    if story:
        # Get selected language for translation
        selected_language = st.session_state.get("selected_language", "English")
        
        # Translate title
        lang_code = LANGUAGES.get(selected_language, {}).get("code", "en")
        translated_title = translate_text(story.get("title", "Untitled"), lang_code)
        st.title(translated_title)
        
        # Story metadata
        category = story.get("category", "General")
        translated_category = translate_text(category, lang_code)
        is_premium = story.get("is_premium", False)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption(f"📚 {translated_category} {'• 💎 Premium' if is_premium else '• 🆓 Free'}")
        
        with col2:
            # Favorite toggle
            title = story.get("title", "")
            is_fav = title in st.session_state.favorites
            
            if st.button("❤️" if is_fav else "🤍", key="fav_toggle"):
                # Play click sound if enhanced features available
                if ENHANCED_FEATURES:
                    play_click_sound()
                
                if is_fav:
                    st.session_state.favorites.remove(title)
                else:
                    st.session_state.favorites.add(title)
                    # Play success sound for favoriting
                    if ENHANCED_FEATURES:
                        play_success_sound()
                
                save_favorites(st.session_state.favorites)
                st.rerun()
        
        # Show cover image
        cover_image = story.get("cover_image", "")
        if cover_image:
            show_image_resilient(f"images/{cover_image}", caption="📖 Story Cover")
        
        st.markdown("---")
        
        # Show story content
        if is_premium and not st.session_state.get("premium", False):
            # Check user state and show appropriate UI
            if not st.session_state.get("logged_in", False):
                # Not logged in - show login/signup prompt
                st.markdown("""
                <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #1e1b4b, #312e81); border-radius: 20px; margin: 20px 0;">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🔒</div>
                    <h2 style="color: #facc15; font-family: 'Baloo 2', cursive; font-weight: 800; margin-bottom: 10px;">
                        Premium Story Locked
                    </h2>
                    <h3 style="color: white; margin-bottom: 30px;">
                        {0}
                    </h3>
                    <p style="color: #d1d5db; font-size: 1.2rem; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto;">
                        All stories are now free to enjoy!
                    </p>
                </div>
                """.format(story.get("title", "")), unsafe_allow_html=True)
                
                # Show login/signup buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔐 Login", key="premium_login_btn", use_container_width=True):
                        _go("login")
                with col2:
                    if st.button("✨ Sign Up", key="premium_signup_btn", use_container_width=True):
                        _go("signup")
            else:
                # Logged in without premium - show PayPal unlock page (single message)
                render_premium_unlock_page(story)
        else:
            # Get and translate story text
            story_text = story.get("text", story.get("content", "No content available."))
            translated_text = translate_text(story_text, lang_code)
            
            # Audio narration section
            st.subheader("🔊 Audio Narration")
            if TTS_AVAILABLE:
                story_slug = slugify(story.get("title", ""))
                audio_file = generate_audio(translated_text, selected_language, story_slug)
                
                if audio_file and Path(audio_file).exists():
                    # Show audio player
                    st.audio(audio_file, format="audio/mp3")
                else:
                    if st.button("🎵 Generate Audio Narration", key="generate_audio_btn"):
                        with st.spinner("Generating audio..."):
                            audio_file = generate_audio(translated_text, selected_language, story_slug)
                            if audio_file:
                                st.success("Audio generated!")
                                st.rerun()
                            else:
                                st.error("Failed to generate audio")
            else:
                st.info("Install gTTS for audio narration: pip install gTTS")
            
            st.markdown("---")
            
            # Display story text with proper RTL handling
            st.subheader("📖 Story")
            
            with story_container_open():
                st.markdown('<div class="story-content">', unsafe_allow_html=True)
                
                paragraphs = translated_text.split("\n\n")
                
                # Show first half
                first_half = paragraphs[:len(paragraphs)//2]
                for para in first_half:
                    if para.strip():
                        if selected_language in RTL_LANGUAGES:
                            st.markdown(f'<div class="story-text" style="direction: rtl; text-align: right;">{para.strip()}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="story-text">{para.strip()}</div>', unsafe_allow_html=True)
                
                # Show mid image
                mid_image = story.get("mid_image", "")
                if mid_image:
                    show_image_resilient(f"images/{mid_image}", caption="🎨 Mid-story Illustration")
                
                # Show second half
                second_half = paragraphs[len(paragraphs)//2:]
                for para in second_half:
                    if para.strip():
                        if selected_language in RTL_LANGUAGES:
                            st.markdown(f'<div class="story-text" style="direction: rtl; text-align: right;">{para.strip()}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="story-text">{para.strip()}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Show end image
            end_image = story.get("end_image", "")
            if end_image:
                show_image_resilient(f"images/{end_image}", caption="🌟 Story Ending")
        
        st.markdown("---")
        
        # Quiz section - All quizzes are now free
            # Get current story ID (use slug for consistency)
            current_story_id = story.get("slug", story.get("title", "")).lower().replace(" ", "-").replace("_", "-")
            
            # Render the new polished quiz UI
            render_quiz(current_story_id)
        
        st.markdown("---")
        
        # Auto-scroll to top when story loads
        st.markdown("""
        <script>
        // Auto-scroll to top when story loads
        window.scrollTo({ top: 0, behavior: 'smooth' });
        </script>
        """, unsafe_allow_html=True)
        
    else:
        st.error("Story not found!")
    
    # Single back button at the bottom - centered
    st.markdown('<div class="belu-single-button-container">', unsafe_allow_html=True)
    if st.button("🏠 Back to Stories", key="back_to_stories_btn", use_container_width=False):
        # Play click sound if enhanced features available
        if ENHANCED_FEATURES:
            play_click_sound()
        
        st.session_state.view_mode = "list"
        st.session_state.current_story = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # List view - using optimized story index
    if not stories_index:
        st.error("No stories found! Please check if stories.json exists and has content.")
    else:
        # Search and filters with debounced search
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Debounced search input
            search_input = st.text_input("🔍 Search stories...", placeholder="Search by title or category", key="search_input")
            # Update search state for debouncing
            if search_input != st.session_state.get("search_query_value", ""):
                st.session_state["search_query_value"] = search_input
                st.session_state["search_query_last_update"] = time.time()
            
            # Get debounced search query
            query = debounce_search("search_query", delay=0.3)
        
        # Build current filter state for consistent counting
        current_fs = FilterState(
            language=st.session_state.get("selected_language", "English"),
            story_type="All",  # Will be updated below
            search_text=query,
            favorites_only=False,  # Will be updated below
            category="All",  # Will be updated below
            favorite_ids=set(st.session_state.favorites)
        )
        
        with col3:
            premium_filter = st.selectbox("💎 Type", ["All", "Free", "Premium"])
            current_fs.story_type = premium_filter
        
        # Additional filters
        col4, col5 = st.columns([1, 1])
        with col4:
            # Favorites filter moved to category dropdown
            pass
        
        # Get categories with counts using optimized function
        categories_with_counts = get_categories_optimized(stories_index)
        
        with col2:
            # Build category options with counts - deduplicated and properly sorted
            category_options = []
            category_mapping = {}  # Maps display option to canonical key
            
            # Define the exact order for categories
            category_order = ["All", "Favorites", "Adventure", "Dreams", "Family", "Self-Discovery"]
            
            # Process each category in the defined order
            for canonical_key in category_order:
                if canonical_key == "All":
                    # Add "All" first
                    all_count = categories_with_counts.get("All", 0)
                    option_text = f"All ({all_count})"
                    category_options.append(option_text)
                    category_mapping[option_text] = "All"
                    
                elif canonical_key == "Favorites":
                    # Add "Favorites" as a special category
                    favorites_count = len(st.session_state.favorites)
                    if favorites_count > 0:
                        display_label = category_label(canonical_key)
                        option_text = f"{display_label} ({favorites_count})"
                        category_options.append(option_text)
                        category_mapping[option_text] = "Favorites"
                        
                else:
                    # Add other categories with deduplicated counts
                    count = categories_with_counts.get(canonical_key, 0)
                    if count > 0:  # Only show categories that have stories
                        display_label = category_label(canonical_key)
                        option_text = f"{display_label} ({count})"
                        category_options.append(option_text)
                        category_mapping[option_text] = canonical_key
            
            selected_category_option = st.selectbox("📚 Category", category_options, index=0)
            category = category_mapping[selected_category_option]
            current_fs.category = category
        
        # Apply optimized filtering on lightweight index
        filter_dict = {
            "search_text": query,
            "category": current_fs.category,
            "story_type": current_fs.story_type,
            "favorites_only": False,  # Now handled by category filter
            "favorite_ids": current_fs.favorite_ids
        }
        filtered_stories = apply_filters_optimized(stories_index, filter_dict)
        
        # Guest Mode limitation: Show only 3 free stories for non-logged-in users
        is_guest_mode = not st.session_state.get("logged_in", False)
        if is_guest_mode:
            # Filter to only free stories and limit to 3
            free_stories = [story for story in filtered_stories if not story.get("is_premium", False)]
            filtered_stories = free_stories[:3]  # Limit to first 3 free stories
        
        # Store filter state in session for sidebar access
        st.session_state['current_filter_state'] = current_fs
        
        # Get current page from query params
        current_page = get_current_page()
        
        # Calculate pagination info
        total_stories = len(filtered_stories)
        current_page, total_pages, start_idx, end_idx = get_pagination_info(total_stories, current_page)
        
        # For Guest Mode, disable pagination since we only show 3 stories
        if is_guest_mode:
            current_page = 1
            total_pages = 1
            start_idx = 0
            end_idx = len(filtered_stories)
        
        st.markdown("---")
        
        # Render pagination controls (hidden for Guest Mode)
        if not is_guest_mode:
            render_pagination_controls(current_page, total_pages, "main")
        
        st.subheader(f"📖 {len(filtered_stories)} stories found")
        
        if not filtered_stories:
            st.info("No stories match your search criteria.")
        else:
            # Slice stories for current page using optimized pagination
            page_stories = filtered_stories[start_idx:end_idx]
            
            # Display stories in a grid with thumbnails
            for i, story in enumerate(page_stories):
                with st.container():
                    st.markdown('<div class="story-card">', unsafe_allow_html=True)
                    
                    # Get selected language for translation
                    selected_language = st.session_state.get("selected_language", "English")
                    lang_code = LANGUAGES.get(selected_language, {}).get("code", "en")
                    
                    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
                    
                    with col1:
                        # Show cover image thumbnail using optimized function
                        cover_path = story.get("cover_path", "")
                        if cover_path:
                            # Use full path for thumbnail generation
                            full_cover_path = f"images/{cover_path}"
                            thumbnail_bytes = get_thumbnail(full_cover_path, max_w=400)
                            if thumbnail_bytes:
                                st.image(thumbnail_bytes, use_column_width=True)
                        else:
                                # Fallback to original image if thumbnail generation fails
                                show_image_resilient(full_cover_path)
                    
                    with col2:
                        # Translate title and category
                        translated_title = translate_text(story.get("title", "Untitled"), lang_code)
                        translated_category = translate_text(story.get('category', 'General'), lang_code)
                        
                        st.subheader(translated_title)
                        st.caption(f"📚 {translated_category} {'• 💎 Premium' if story.get('is_premium', False) else '• 🆓 Free'}")
                        
                        # Show translated excerpt from lightweight index
                        snippet = story.get("snippet", "")
                        translated_excerpt = translate_text(snippet, lang_code)
                        st.write(translated_excerpt)
                    
                    with col3:
                        # Open button - use story ID for navigation
                        if st.button("📖 Read", key=f"read_{i}"):
                            # Play click sound if enhanced features available
                            if ENHANCED_FEATURES:
                                play_click_sound()
                            
                            st.session_state.view_mode = "detail"
                            st.session_state.current_story = story.get("id", "")  # Use story ID
                            st.rerun()
                    
                    with col4:
                        # Favorite button
                        title = story.get("title", "")
                        is_fav = title in st.session_state.favorites
                        
                        if st.button("❤️" if is_fav else "🤍", key=f"fav_{i}"):
                            if is_fav:
                                st.session_state.favorites.remove(title)
                            else:
                                st.session_state.favorites.add(title)
                            save_favorites(st.session_state.favorites)
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if i < len(page_stories) - 1:
                    st.markdown("<br>", unsafe_allow_html=True)
            
            # Guest Mode upgrade banner
            if is_guest_mode:

# Sidebar with favorites - HIDDEN (moved to category filter)
# with st.sidebar:
#     st.header("⭐ Favorites")
#     
#     favorites = st.session_state.favorites
#     if not favorites:
#         st.info("No favorites yet! Click 🤍 on stories to add them.")
#     else:
#         for fav_title in sorted(favorites):
#             if st.button(f"📖 {fav_title}", key=f"sidebar_{fav_title}"):
#                 st.session_state.view_mode = "detail"
#                 st.session_state.current_story = slugify(fav_title)
#                 st.rerun()
#     
#     st.markdown("---")
#     st.caption(f"📊 Total: {len(stories_index)} stories")
#     st.caption(f"⭐ Favorites: {len(favorites)}")
#     
#     # Show category distribution using optimized function
#     sidebar_categories = get_categories_optimized(stories_index)
#     st.caption("📚 Categories:")
#     
#     # Add "All" first
#     all_count = sidebar_categories.get("All", 0)
#     if all_count > 0:
#         st.caption(f"  All: {all_count}")
#     
#     # Add other categories sorted by name
#     other_cats = {k: v for k, v in sidebar_categories.items() if k != "All"}
#     for canonical_key in sorted(other_cats.keys()):
#         count = other_cats[canonical_key]
#         if count > 0:
#             display_label = category_label(canonical_key)
#             st.caption(f"  {display_label}: {count}")
#     
#     # Performance info (only in development)
#     if st.checkbox("🔧 Show Performance Info", key="perf_info"):
#         st.caption(f"📈 Index size: {len(stories_index)} stories")
#         st.caption(f"💾 Cache status: Active")
        # Clear Cache button removed from UI - available as helper function for development
