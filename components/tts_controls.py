# components/tts_controls.py — narrator presets per language
import streamlit as st

# English accents via gTTS tld
_EN_NARRATORS = {
    "Sunny (US)":  "com",
    "Rosie (UK)":  "co.uk",
    "Skye (AU)":   "com.au",
    "Ayo (ZA)":    "co.za",
    "Priya (IN)":  "co.in"
}

def get_narrator_for_language(lang_code: str):
    """
    Renders a compact narrator selector.
    Returns (label, tld) where tld is only used for English.
    """
    with st.container():
        c1, c2 = st.columns([1.3, 2.7])
        with c1:
            st.caption("Narrator")
        with c2:
            if lang_code.lower() == "en":
                # Show English accent choices
                default = "Sunny (US)"
                label = st.selectbox("Narrator", list(_EN_NARRATORS.keys()),
                                     index=list(_EN_NARRATORS.keys()).index(default),
                                     label_visibility="collapsed")
                return label, _EN_NARRATORS[label]
            else:
                # Single narrator label for non-English (gTTS picks a voice)
                st.text_input("Narrator", value="Native voice", label_visibility="collapsed", disabled=True)
                return "Native voice", None
