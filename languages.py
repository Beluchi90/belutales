# Language configuration for BeluTales
# Each language has an ISO code for GoogleTranslator and a flag emoji for display

LANGUAGES = {
    "English": {"code": "en", "flag": "🇬🇧"},
    "French": {"code": "fr", "flag": "🇫🇷"},
    "Zulu": {"code": "zu", "flag": "🇿🇦"},
    "Chinese": {"code": "zh-CN", "flag": "🇨🇳"},
    "Arabic": {"code": "ar", "flag": "🇸🇦"},
    "Afrikaans": {"code": "af", "flag": "🇿🇦"},
    "Igbo": {"code": "ig", "flag": "🇳🇬"},
    "Yoruba": {"code": "yo", "flag": "🇳🇬"},
    "Spanish": {"code": "es", "flag": "🇪🇸"},
    "German": {"code": "de", "flag": "🇩🇪"},
    "Portuguese": {"code": "pt", "flag": "🇵🇹"},
    "Hindi": {"code": "hi", "flag": "🇮🇳"}
}

# RTL languages that need special text direction handling
RTL_LANGUAGES = ["Arabic"]

# Helper function to get language code by name
def get_language_code(language_name: str) -> str:
    """Get the ISO language code for a given language name"""
    return LANGUAGES.get(language_name, {}).get("code", "en")

# Helper function to get flag by language name
def get_language_flag(language_name: str) -> str:
    """Get the flag emoji for a given language name"""
    return LANGUAGES.get(language_name, {}).get("flag", "🇬🇧")

# Helper function to get display label (flag + name)
def get_language_display(language_name: str) -> str:
    """Get the display label combining flag and language name"""
    flag = get_language_flag(language_name)
    return f"{flag} {language_name}"
