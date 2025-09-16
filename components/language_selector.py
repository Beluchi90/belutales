# components/language_selector.py — friendly language dropdown with flags
import streamlit as st

LANGS = {
    "English 🇬🇧": "en",
    "French 🇫🇷": "fr",
    "Spanish 🇪🇸": "es",
    "Portuguese 🇵🇹": "pt",
    "German 🇩🇪": "de",
    "Italian 🇮🇹": "it",
    "Arabic 🇸🇦": "ar",
    "Swahili 🇰🇪": "sw",
    "Zulu 🇿🇦": "zu",
    "Yoruba 🇳🇬": "yo",
    "Igbo 🇳🇬": "ig",
    "Chinese (Simplified) 🇨🇳": "zh-cn",
    "Chinese (Traditional) 🇹🇼": "zh-tw"
}

def render_language_selector():
    """Shows a compact selector and stores the code in session."""
    if "language" not in st.session_state:
        st.session_state.language = "en"
        st.session_state.language_label = "English 🇬🇧"

    with st.container():
        c1, c2 = st.columns([1.2, 2.8])
        with c1:
            st.caption("Language")
        with c2:
            label = st.selectbox(
                label="Language",
                options=list(LANGS.keys()),
                index=list(LANGS.keys()).index(st.session_state.get("language_label","English 🇬🇧")),
                label_visibility="collapsed"
            )
            st.session_state.language_label = label
            st.session_state.language = LANGS[label]
    return st.session_state.language_label, st.session_state.language
