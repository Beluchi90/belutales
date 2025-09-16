# BeluTales Deployment Guide

A magical storytelling app for kids, built with Python + Streamlit.

## Features
- Fun, illustrated stories (with free and premium options)
- Category navigation, favorites, and progress tracker
- Read Aloud (TTS) in multiple languages
- Interactive quizzes
- Multilingual UI (English, French, Spanish, Swahili, Arabic)

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## Running Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploying to Streamlit Cloud
1. Push your code (including `app.py`, `stories.json`, `images/`, and `requirements.txt`) to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/) and deploy your repo.
3. The app will run automatically.

## Packaging as .exe (PyInstaller)
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   pyinstaller --onefile --add-data "stories.json;." --add-data "images;images" app.py
   ```
3. The `.exe` will be in the `dist/` folder. Make sure `stories.json` and `images/` are in the same directory as the `.exe` if not bundled.
4. The app uses a `resource_path` utility for compatibility with PyInstaller.

## Mobile/Webview Option
- Deploy to Streamlit Cloud and open in a mobile browser.
- Or use a Python webview wrapper (e.g., Toga, Kivy, PyWebView) to wrap the Streamlit Cloud URL.

## Notes
- Keep `stories.json` and `images/` in the root directory for all deployments.
- For PyInstaller, the app uses a `resource_path` utility for compatibility.

Enjoy magical stories with BeluTales! 🌟 