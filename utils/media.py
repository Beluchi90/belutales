# utils/media.py - Media utilities for BeluTales

def emoji_for_category(category: str) -> str:
    """Return an emoji for a given category"""
    emoji_map = {
        "All": "📚",
        "Adventure": "🗺️",
        "Bedtime": "🌙",
        "Friendship": "👫",
        "Nature": "🌿",
        "Fantasy": "🦄",
        "Other": "✨",
        "General": "📖",
        "Magic": "🪄",
        "Animals": "🐾",
        "Space": "🚀",
        "Ocean": "🌊"
    }
    
    return emoji_map.get(category, "📖")
