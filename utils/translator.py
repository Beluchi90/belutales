from deep_translator import GoogleTranslator

def translate_text(text: str, target_lang: str = "en") -> str:
    """
    Safely translate text using deep-translator.
    - text: The string to translate.
    - target_lang: Language code to translate into (default 'en').
    Returns: Translated string.
    """
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception:
        # If translation fails, return the original text
        return text