# ✅ Cursor Instructions for BeluTales App

## 🌟 APP NAME: BeluTales  
**GOAL**: A magical storytelling app for kids, built with Python + Streamlit.  
Displays stories with illustrations from a JSON file. Some stories are Premium-only.

---

## ✅ INSTRUCTIONS FOR CURSOR AI

Please help improve the BeluTales app based on this step-by-step roadmap.  
**Don’t erase working features unless told to.**  
Beluchi is still learning, so explain changes clearly and use simple code.

---

## 🔹 PHASE 1: UI POLISH

- Set a soft pastel background color (e.g. light yellow, light blue).
- Add a large, fun header with emojis:
  > 🌟 BeluTales – Magical Stories for Kids
- Add cute icons or a banner (optional but encouraged).
- Use fun fonts and layout elements (Streamlit `st.markdown`, emojis, `unsafe_allow_html=True` for better design if needed).

---

## 🔹 PHASE 2: STORY NAVIGATION

- Add a **category dropdown** (Bedtime, Adventure, Animals, etc).
- Filter stories by category (add `"category"` field to each story in `stories.json`).
- Add **"Next Story" / "Previous Story"** navigation buttons.

---

## 🔹 PHASE 3: PREMIUM STORIES

- Add `"premium": true/false` to each story in `stories.json`.
- By default, show only free stories.
- Show 🔒 icon beside locked titles.
- Add an **“Unlock Premium”** toggle (simulate unlock with `st.session_state`).

---

## 🔹 PHASE 4: AUDIO, TRANSLATION, & EXPERIENCE

### 1. 🎧 **Read Aloud**
- Add a “Read Aloud” button using `pyttsx3`, `gTTS`, or similar.
- Let users hear the story in their selected language.

### 2. 📈 **Progress Tracker**
- Track how many stories the user has read (e.g. “You’ve read 3 of 20 stories”).

### 3. ⭐ **Favorites**
- Add a ⭐ “Favorite” toggle per story.
- Store favorite titles in `st.session_state` and display them at the top.

### 4. 🌍 **Multilingual Support**
- Add a **language selector**: English, French, Spanish, Swahili, Arabic, etc.
- Use `googletrans`, `deep_translator`, or `translatepy` to translate:
  - Story title and content
  - UI buttons and headings
  - Quiz questions + feedback text
- For audio: use a TTS library that supports the selected language (e.g. `gTTS` with language codes).
- Store the selected language and apply it across the session.
- Make sure layout, fonts, and buttons still display nicely after translation.

📝 Optional: Add language flag icons in the dropdown using `unsafe_allow_html=True`.

---

## 🔹 PHASE 5: INTERACTIVE QUIZZES

- Add an optional `"quiz"` field to some stories in `stories.json`, like this:

```json
"quiz": {
  "question": "What did the character invent?",
  "options": ["Robot", "Candy Lab", "Flying Shoes", "Magic Mirror"],
  "answer": "Candy Lab"
}
```

- After showing a story, check if a quiz exists.
- Display a multiple-choice quiz using `st.radio()`.
- On submission:
  - ✅ Show `st.success("🎉 Correct!")` for right answer
  - ❌ Show `st.error("❌ Try again!")` for wrong answer
- Handle stories with no quiz gracefully.

---

## 🔹 PHASE 6: DEPLOYMENT PREP

- Help Beluchi deploy to:
  - ✅ **Streamlit Cloud**
  - ✅ Convert to `.exe` using `pyinstaller`
  - ✅ Optional mobile wrap (Toga, Kivy, or WebView for Android/iOS)
- Make sure paths to `stories.json` and `images/` still work after packaging.

---

## ✨ ADDITIONAL IDEAS (OPTIONAL)
- Add **search** by title or keyword.
- Add **“Story of the Day”** feature.
- Add **offline fallback** for read-aloud audio (pre-generate MP3s).
- Add **emoji-based story ratings** or mood tags (😍🌈😴).

---

## 🛑 FINAL NOTES:

- Never erase `stories.json`.
- Keep images inside the `images/` folder.
- Write clear, simple, well-commented code.
- Beluchi is still learning—**please explain what you’re doing, step-by-step.**
