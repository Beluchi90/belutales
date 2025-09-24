# components/hero.py — Night sky hero with rainbow title
import streamlit as st

def render_hero():
    st.markdown("""
    <div class="bt-hero">
      <div style="display:flex;gap:12px;align-items:center;">
        <div style="width:56px;height:56px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:32px;background: radial-gradient(circle at 40% 35%, #ffd7a1, #ffa955); box-shadow:inset 0 0 0 5px #fff8ee30, 0 10px 22px rgba(255,170,80,.28);">🦉</div>
        <div>
          <h1 class="bt-rb">BeluTales</h1>
          <div class="bt-hero-tag">Bedtime adventures • gentle lessons</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
