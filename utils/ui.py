from pathlib import Path
import streamlit as st

def inject_fonts_and_sounds():
    # Prefer local fonts; fall back to Google CDN if missing
    baloo_local = Path("assets/fonts/Baloo2-VariableFont_wght.woff2").exists()
    quick_local = Path("assets/fonts/Quicksand-VariableFont_wght.woff2").exists()

    font_face = ""
    if baloo_local or quick_local:
        font_face += """
        <style>
        @font-face {
          font-family: 'Baloo2';
          src: url('/app/assets/fonts/Baloo2-VariableFont_wght.woff2') format('woff2'),
               url('assets/fonts/Baloo2-VariableFont_wght.woff2') format('woff2');
          font-weight: 400 800; font-style: normal; font-display: swap;
        }
        @font-face {
          font-family: 'Quicksand';
          src: url('/app/assets/fonts/Quicksand-VariableFont_wght.woff2') format('woff2'),
               url('assets/fonts/Quicksand-VariableFont_wght.woff2') format('woff2');
          font-weight: 300 700; font-style: normal; font-display: swap;
        }
        </style>
        """
    else:
        font_face += """
        <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700&family=Quicksand:wght@400;600;700&display=swap" rel="stylesheet">
        """

    # Global CSS for playful, readable typography
    css = """
    <style>
      :root{
        --display: 'Baloo2', system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
        --body: 'Quicksand', system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
        --story-size: clamp(18px, 2.2vw, 22px);
        --story-line: 1.8;
        --menu-size: 16px;
        --heading-size: clamp(24px, 3vw, 32px);
      }
      html, body, [data-testid="stAppViewContainer"]{
        font-family: var(--body);
      }
      /* Story text area */
      .story-content p, .story-content li{
        font-size: var(--story-size) !important;
        line-height: var(--story-line) !important;
        letter-spacing: 0.2px;
      }
      .story-content h1, .story-content h2, .story-content h3{
        font-family: var(--display);
        font-size: var(--heading-size);
        line-height: 1.2;
        margin: 0.2rem 0 0.6rem 0;
      }
      /* Sidebar */
      section[data-testid="stSidebar"]{
        font-size: var(--menu-size);
      }
      /* Buttons a bit larger for kids */
      button[kind="primary"], button[kind="secondary"]{
        font-family: var(--display);
        font-weight: 700;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
      }
    </style>
    """

    # Audio + JS: play sounds whenever any Streamlit button is clicked
    # We add three audio elements and a small script to hook into clicks.
    audio_html = """
    <audio id="sfx-click" src="assets/sounds/click.mp3" preload="auto"></audio>
    <audio id="sfx-success" src="assets/sounds/success.mp3" preload="auto"></audio>
    <audio id="sfx-nav" src="assets/sounds/nav.mp3" preload="auto"></audio>
    <script>
      // Debounce so rapid reruns don't double-hook
      if (!window._belutalesSFX){
        window._belutalesSFX = true;
        const play = (id) => {
          const el = document.getElementById(id);
          if (el) { try { el.currentTime = 0; el.play(); } catch(e) {} }
        };
        // Global click sound on Streamlit buttons
        document.addEventListener('click', (e) => {
          const btn = e.target.closest('button');
          if (!btn) return;
          // Heuristics for special buttons
          const label = (btn.innerText || '').toLowerCase();
          if (/(next|previous|prev|back)/.test(label)) play('sfx-nav');
          else if (/(favorite|favourite|add|save|buy|subscribe)/.test(label)) play('sfx-success');
          else play('sfx-click');
        }, {capture:true});
      }
    </script>
    """

    st.markdown(font_face, unsafe_allow_html=True)
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(audio_html, unsafe_allow_html=True)

def story_container_open():
    # Helper to wrap story text with class for styling
    return st.container()
