# Translation Installation Guide

## Install the Translation Library

To enable automatic multilingual translations in BeluTales, install the required package:

```bash
pip install deep-translator
```

## Supported Languages

The app supports the following languages:
- **English** 🇬🇧 (default, no translation needed)
- **French** 🇫🇷 (Français)
- **Spanish** 🇪🇸 (Español)
- **Zulu** 🇿🇦 (isiZulu)
- **Chinese** 🇨🇳 (中文) - zh-CN
- **Arabic** 🇸🇦 (العربية) - RTL support
- **Afrikaans** 🇿🇦
- **Igbo** 🇳🇬
- **Yoruba** 🇳🇬
- **German** 🇩🇪 (Deutsch)
- **Portuguese** 🇵🇹 (Português)
- **Hindi** 🇮🇳 (हिन्दी)

## How It Works

1. **Language Selection**: Use the language dropdown at the top of the app
2. **Automatic Translation**: When you select a non-English language, the app automatically translates:
   - Story titles
   - Story categories
   - Story text content
   - UI labels and buttons
3. **Real-time Translation**: Uses Google Translate API through the deep-translator package
4. **RTL Support**: Arabic text is automatically displayed right-to-left

## Audio Narration

The app also supports text-to-speech narration for stories:

1. **Installation**: gTTS is already included in requirements.txt
2. **Supported Languages**: Audio narration works for all supported languages
3. **Automatic Generation**: Audio files are generated on-demand and cached in the `audio/` folder
4. **File Naming**: Audio files follow the pattern `{story-slug}_{language-code}.mp3`

## Favorites System

The app includes a comprehensive favorites management system:

1. **Favorite Toggle**: Each story has a heart button (🤍/❤️) to mark as favorite
2. **Persistent Storage**: Favorites are saved in `favorites.json` and persist between sessions
3. **Filter Option**: Use the "Show Favorites Only" checkbox to filter the main story list
4. **Sidebar Quick Access**: A dedicated sidebar section "⭐ Favorites" lists all favorite stories as clickable buttons
5. **Visual Indicators**: Favorite status is clearly displayed in both story list and detail views
6. **Immediate Updates**: The sidebar favorites list updates instantly when adding/removing favorites

## Story Display

The app provides a clean, focused reading experience with properly separated view modes:

1. **List View Mode**: Shows all stories in a grid layout with search, filters, and favorites
2. **Detail View Mode**: Each story opens in its own dedicated page/route using story slugs
3. **Full Story Display**: All story text and images are always visible when opening a story
4. **Improved Story Flow**: 
   - Cover image displayed at the top
   - First half of story text
   - Mid-story image with separator
   - Second half of story text
   - Ending image with separator
   - Audio narration button below the text
5. **Story Completion**: Shows "🎉 You finished this story!" with a "Back to Stories" button
6. **Clean Interface**: No progress tracking or Continue Reading buttons - just pure story content
7. **Focused Reading**: Each story opens in its own dedicated view without other story cards underneath
8. **Smart Navigation**: "Open" buttons switch to detail view, "Back to Stories" returns to list view
9. **Proper Separation**: List and detail views are completely independent - no story loops or multiple rendering
10. **Clean Conditional Rendering**: Uses conditional logic to ensure only the selected story displays in detail mode
11. **Robust Story Loading**: New `load_story()` function ensures all story content is properly loaded with fallbacks
12. **Placeholder Content**: Shows helpful messages like "(No cover image)" or "(No text yet.)" for missing content

## Premium Story Features

The app now supports premium story management:

1. **Premium Story Detection**: Stories with `"is_premium": true` in `stories.json` are automatically identified
2. **Premium Filtering**: Users can filter stories by type (All, Free, Premium) using a dropdown
3. **Premium Button Display**: Premium stories show "Premium – Unlock" button (currently disabled), free stories show "Open" button
4. **Premium Story Locking**: When users try to open premium stories, they see a centered lock screen with:
   - 🔒 Large lock icon
   - Story title prominently displayed
   - "This is a premium story. Unlock to continue." message
   - 🔓 Unlock (Coming Soon) disabled button
   - Back to Stories navigation button
5. **Backward Compatibility**: Existing free stories continue to work normally

## Performance Features

The app includes several performance optimizations:

1. **Translation Caching**: All translations are cached using `@st.cache_data` for faster loading
2. **Audio Caching**: Generated audio files are cached using `@st.cache_resource` to prevent regeneration
3. **Query Parameters**: Direct story access via URL parameters (e.g., `?story=story-slug`)
4. **Auto-scroll**: Stories automatically scroll to the top when opened for better reading experience

## Notes

- Translations are cached for performance - first load may be slower, subsequent loads are instant
- If translation fails, the app falls back to English
- Audio narration is generated using Google Text-to-Speech (gTTS)
- If a language is not supported for TTS, it falls back to English audio
- The app maintains all existing functionality (images, favorites, search, translations)
- No changes to story content or structure
