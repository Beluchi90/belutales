# utils/state.py — query params + session helpers
import streamlit as st

def init_session():
    st.session_state.setdefault("favorites", set())
    st.session_state.setdefault("sfx_enabled", True)
    st.session_state.setdefault("current_cat", "All")
    st.session_state.setdefault("quiz_scores", {})  # slug -> score
    st.session_state.setdefault("language", "en")
    st.session_state.setdefault("language_label", "English 🇬🇧")

def get_qp() -> dict:
    try:
        return dict(st.query_params)
    except Exception:
        return {}

def set_qp(_merge=False, **kwargs):
    try:
        if _merge:
            q = dict(st.query_params)
            q.update({k:v for k,v in kwargs.items() if v is not None})
            st.query_params.update(q)
        else:
            st.query_params.update({k:v for k,v in kwargs.items() if v is not None})
    except Exception:
        pass
