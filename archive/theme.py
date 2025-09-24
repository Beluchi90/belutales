# theme.py — Bright Magical Pastel Theme (mobile-first)

import streamlit as st

def inject_fonts():
    st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Baloo+2:wght@700;900&family=Sniglet:wght@400;800&family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

def inject_theme_css():
    st.markdown("""
<style>
  /* Hide desktop chrome; keep a tight mobile canvas */
  #MainMenu, footer, header [data-testid="stToolbar"], section[data-testid="stSidebar"]{display:none !important}
  .block-container{ max-width: 460px !important; padding: .6rem .6rem 6.8rem !important; margin: 0 auto !important; }

  :root{
    /* Bright, enchanting palette */
    --ink:#2b1c14;          /* primary text on light */
    --ink2:#5d4a3a;         /* secondary text */
    --skyTop:#fff7fb;       /* soft pink */
    --skyMid:#f7fbff;       /* soft blue-white */
    --skyBot:#fff6e6;       /* warm peach */
    --card:#ffffff;         /* reader card base */
    --card2:#ffffff;        /* tile base */
    --border:#ffffff;
    --ring:rgba(255,180,220,.40);
    --btnGrad: linear-gradient(135deg,#ffd36b,#ff96d0,#8ccaff); /* sunny → raspberry → sky */
  }

  /* Pastel sky background with subtle sparkles */
  .stApp{
    color:var(--ink) !important;
    background:
      radial-gradient(900px 520px at 95% -10%, rgba(255,255,255,.70), transparent 60%),
      linear-gradient(180deg, var(--skyTop) 0%, var(--skyMid) 45%, var(--skyBot) 100%) !important;
    position:relative; overflow-x:hidden;
  }
  /* Sparkles (very light, non-distracting) */
  .stApp:before, .stApp:after{
    content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
    background-image:
      radial-gradient(2px 2px at 20% 30%, rgba(255,180,220,.7) 50%, transparent 51%),
      radial-gradient(2px 2px at 80% 20%, rgba(160,210,255,.7) 50%, transparent 51%),
      radial-gradient(1.8px 1.8px at 60% 70%, rgba(255,210,120,.7) 50%, transparent 51%),
      radial-gradient(1.7px 1.7px at 30% 80%, rgba(180,255,210,.7) 50%, transparent 51%),
      radial-gradient(1.5px 1.5px at 70% 45%, rgba(200,190,255,.7) 50%, transparent 51%);
    background-repeat:repeat;
    animation: twinkle 6s ease-in-out infinite alternate;
    opacity:.45;
  }
  .stApp:after{ animation-duration: 9s; opacity:.30; filter:blur(0.2px) }
  @keyframes twinkle{0%{opacity:.30}100%{opacity:.60}}

  /* HERO (glossy cloud) */
  .hero{
    position:relative; z-index:1; border-radius:18px; padding:14px;
    background: linear-gradient(180deg, rgba(255,255,255,.78), rgba(255,255,255,.58));
    border:2px solid var(--border);
    box-shadow: 0 16px 40px rgba(255,170,200,.22);
    margin: 0 0 12px;
  }
  .hero-row{display:flex;gap:12px;align-items:center}
  .owl{
    width:56px;height:56px;border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:32px;
    background: radial-gradient(circle at 40% 35%, #ffdba6, #ffb455);
    box-shadow: inset 0 0 0 5px #fff8, 0 10px 22px rgba(255,170,80,.28)
  }
  .title{
    margin:0;font:900 34px/1 'Fredoka','Baloo 2',system-ui;
    background:linear-gradient(90deg,#ff6f91,#ff9671,#ffc75f,#9cffac,#8ccaff);
    background-size:300% 100%;
    -webkit-background-clip:text;background-clip:text;color:transparent;
    text-shadow: 0 3px 0 rgba(255,255,255,.9);
    animation: brand 12s linear infinite
  }
  .tag{margin:3px 0 0;font:800 13px/1 'Sniglet',system-ui;color:var(--ink2);opacity:.95}
  @keyframes brand{0%{background-position:0% 50%}100%{background-position:100% 50%}}

  /* SEARCH (glassy) */
  .search-wrap{
    background: rgba(255,255,255,.82);
    border:2px solid var(--border);
    border-radius:16px; padding:.38rem .48rem;
    box-shadow: 0 12px 26px rgba(0,0,0,.08);
    backdrop-filter: blur(8px);
  }
  .search-wrap .stTextInput input{
    font-size:16px !important; padding:.62rem .8rem !important; border-radius:14px !important;
    border:2px solid #ffe0f2 !important; background:#fff8fd !important; color:#443225 !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,.04);
  }
  .search-wrap .stButton>button{
    font:900 16px/1 system-ui; border-radius:999px !important; padding:.68rem 0 !important;
    background: var(--btnGrad) !important; color:#103a57 !important; border:1px solid #f7f1ff !important;
    box-shadow:0 6px 14px rgba(0,0,0,.08);
  }

  /* CATEGORY CHIPS (single row) */
  .catbar{display:flex;gap:.5rem;overflow-x:auto;padding:.5rem .1rem;scroll-snap-type:x proximity;-webkit-overflow-scrolling:touch}
  .catbar::-webkit-scrollbar{height:6px}.catbar::-webkit-scrollbar-thumb{background:#eadcff;border-radius:8px}
  .chip{
    flex:0 0 auto; scroll-snap-align:center; text-decoration:none; user-select:none;
    display:inline-flex; align-items:center; gap:.45rem; padding:.58rem .95rem; border-radius:999px;
    background: linear-gradient(135deg,#fff,#fff9f6);
    border:2px solid #ffe6f6;
    box-shadow: 0 6px 14px rgba(0,0,0,.08), inset 0 1px 0 rgba(255,255,255,.9);
    font:900 15px/1 'Baloo 2',system-ui; color:#3a2a1d;
    transition: transform .12s ease, box-shadow .12s ease, filter .12s ease;
  }
  .chip:active{ transform: scale(.98) }
  .chip.active{ background: linear-gradient(135deg,#fff,#fff2fb); border-color:#ffc9ec }
  .chip .em{font-size:18px}
  .count{font:800 12px/1 'Fredoka';padding:.18rem .5rem;border-radius:999px;background:#fff5fb;border:1px solid #ffe6f6}

  /* GRID: 1-col mobile; 2-col tablet+ */
  .grid{display:grid;grid-template-columns:1fr;gap:12px;margin:.35rem 0 .8rem; position:relative; z-index:1}
  @media (min-width: 680px){ .grid{ grid-template-columns:1fr 1fr; }}

  /* TILES (uniform, glossy) */
  .tile{
    display:block; text-decoration:none; color:inherit;
    background: linear-gradient(180deg,#ffffff,#fff9f2);
    border:2px solid var(--border); border-radius:18px;
    box-shadow: 8px 10px 22px rgba(0,0,0,.08), -6px -6px 16px #ffffff;
    overflow:hidden; transition: transform .12s ease, box-shadow .12s ease, filter .12s ease;
  }
  .tile:hover{ transform: translateY(-2px); box-shadow: 10px 12px 24px rgba(0,0,0,.10), -6px -6px 16px #ffffff; }
  .tile:active{ transform: translateY(0) scale(.995); filter: brightness(.98) }
  .cover{ width:100%; aspect-ratio: 3/2; object-fit:cover; display:block; background:#fff7fb; border-bottom:2px solid #fff }
  .cover-emoji{
    width:100%; aspect-ratio:3/2; display:flex; align-items:center; justify-content:center; font-size:40px;
    background: radial-gradient(circle at 30% 25%, #fff2f9, #ffeae0 60%, #fff);
  }
  .meta{ padding:.65rem .75rem .8rem }
  .t{ font:900 18px/1.25 'Fredoka','Baloo 2',system-ui; margin:0 0 .24rem 0; color:#2e2118 }
  .c{
    display:inline-flex; align-items:center; gap:.35rem; font:800 14px/1 'Sniglet';
    padding:.24rem .6rem; border-radius:999px; background:#fff5fb; border:1px solid #ffe6f6; color:#4a2e2e
  }
  .c .em{ font-size:16px }

  /* READER CARD */
  .card{
    background: linear-gradient(180deg,#ffffff,#fff9f2); border-radius:20px; padding:.95rem; border:2px solid var(--border);
    box-shadow: 12px 16px 32px rgba(255,170,210,.18), -10px -10px 22px #ffffff; position:relative; z-index:1;
  }
  .h1{
    font:900 28px/1.12 'Fredoka'; text-align:center; margin:.2rem 0 .5rem;
    background:linear-gradient(90deg,#ff6f91,#ff9671,#ffc75f,#9cffac,#8ccaff);
    -webkit-background-clip:text; color:transparent;
  }
  .meta-row{ display:flex; gap:.5rem; justify-content:center; flex-wrap:wrap; margin:.1rem 0 .5rem }
  .mini{
    background:#fff; border:1px solid #ffe6f6; border-radius:999px; padding:.28rem .66rem;
    font:900 14px 'Sniglet'; color:#5b4634
  }
  .txt{ font:400 18px/1.75 'Quicksand',system-ui; color:#3a2a1d }

  /* Reader images */
  .stImage img{
    border-radius:16px !important; border:6px solid #fff !important;
    box-shadow: 0 14px 30px rgba(0,0,0,.12), 0 2px 0 rgba(255,255,255,.95) inset !important;
  }

  /* BOTTOM TABS */
  .tabs{
    position:fixed; left:50%; transform:translateX(-50%); bottom:8px; z-index:80; width:min(480px,96vw);
    background: rgba(255,255,255,.85); backdrop-filter: blur(10px); border:2px solid var(--border);
    border-radius:18px; box-shadow: 0 18px 36px rgba(0,0,0,.12); padding:.35rem;
  }
  .tabs .stButton>button{
    border-radius:16px !important; height:48px !important; font:900 14px 'Fredoka';
    background:var(--btnGrad) !important; color:#103a57 !important; border:1px solid #f7f1ff !important;
    box-shadow: 0 6px 14px rgba(0,0,0,.08);
  }
</style>
""", unsafe_allow_html=True)
