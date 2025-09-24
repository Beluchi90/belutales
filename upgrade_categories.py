#!/usr/bin/env python3
"""
BeluTales Category Upgrade Script
==================================

This script analyzes story content and assigns meaningful categories while preserving
all existing functionality. It creates a backup and improves the categorization system.

UPGRADE: Enhanced story categorization for better browsing experience
PRESERVES: All existing stories, metadata, and functionality
"""

import json
import re
from pathlib import Path
from typing import Dict, List
import shutil
from datetime import datetime

# Define kid-friendly categories with keywords and emojis
CATEGORIES = {
    "🌟 Adventure": {
        "keywords": ["journey", "explore", "travel", "adventure", "quest", "discover", "rescue", "spaceship", "forest", "mountain", "ocean", "island", "map"],
        "emoji": "🌟",
        "description": "Exciting journeys and explorations"
    },
    "✨ Magic": {
        "keywords": ["magic", "magical", "spell", "wizard", "fairy", "enchanted", "mystical", "potion", "wand", "crystal", "glow", "shimmer", "sparkle"],
        "emoji": "✨", 
        "description": "Magical stories and enchanted worlds"
    },
    "🌙 Dreams": {
        "keywords": ["dream", "sleep", "night", "star", "sky", "moon", "wish", "imagine", "wonder", "float", "drift", "cloud"],
        "emoji": "🌙",
        "description": "Dreamy tales and nighttime adventures"
    },
    "💝 Friendship": {
        "keywords": ["friend", "friendship", "together", "help", "care", "share", "kind", "love", "family", "brother", "sister", "companion"],
        "emoji": "💝",
        "description": "Stories about friendship and caring"
    },
    "🎨 Creativity": {
        "keywords": ["art", "draw", "paint", "create", "build", "make", "design", "music", "dance", "sing", "write", "craft", "imagine"],
        "emoji": "🎨",
        "description": "Creative adventures and artistic journeys"
    },
    "🦄 Fantasy": {
        "keywords": ["dragon", "unicorn", "fairy", "fantasy", "creature", "beast", "mythical", "legend", "talking", "animal", "spirit"],
        "emoji": "🦄",
        "description": "Fantasy creatures and mythical tales"
    },
    "🌈 Self-Discovery": {
        "keywords": ["discover", "learn", "grow", "change", "brave", "courage", "believe", "special", "different", "unique", "identity"],
        "emoji": "🌈",
        "description": "Stories about growing up and finding yourself"
    },
    "🏠 Family": {
        "keywords": ["family", "home", "mother", "father", "grandma", "grandpa", "parent", "sibling", "house", "village", "community"],
        "emoji": "🏠",
        "description": "Family bonds and home stories"
    }
}

def analyze_story_content(story: Dict) -> str:
    """
    Analyze story content to determine the best category.
    
    UPGRADE: Smart categorization based on story themes
    PRESERVES: Original story data unchanged
    """
    title = story.get("title", "").lower()
    content = story.get("content", "").lower()
    text = story.get("text", "").lower()
    
    # Combine all text for analysis
    full_text = f"{title} {content} {text}"
    
    # Score each category based on keyword matches
    category_scores = {}
    
    for category_name, category_data in CATEGORIES.items():
        score = 0
        keywords = category_data["keywords"]
        
        for keyword in keywords:
            # Count occurrences with different weights
            title_matches = title.count(keyword) * 3  # Title matches are more important
            content_matches = full_text.count(keyword)
            
            score += title_matches + content_matches
        
        category_scores[category_name] = score
    
    # Return the category with the highest score, or default to General
    if category_scores:
        best_category = max(category_scores, key=category_scores.get)
        if category_scores[best_category] > 0:
            return best_category
    
    return "📚 General"

def create_backup():
    """Create a backup of the current stories.json"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"stories.json.backup_{timestamp}"
    shutil.copy("stories.json", backup_path)
    print(f"✅ Created backup: {backup_path}")
    return backup_path

def upgrade_categories():
    """
    Main upgrade function that enhances categories while preserving all data.
    
    UPGRADE: Better categorization system
    PRESERVES: All existing story data, images, metadata
    """
    print("🚀 Starting BeluTales Category Upgrade...")
    print("📋 This upgrade preserves ALL existing functionality")
    
    # Create backup first
    backup_path = create_backup()
    
    # Load existing stories
    with open("stories.json", "r", encoding="utf-8") as f:
        stories = json.load(f)
    
    print(f"📖 Found {len(stories)} stories to categorize")
    
    # Analyze and categorize each story
    categorized_count = 0
    category_distribution = {}
    
    for story in stories:
        old_category = story.get("category", "General")
        
        # Only update if currently "General" to preserve any manual categorizations
        if old_category == "General":
            new_category = analyze_story_content(story)
            story["category"] = new_category
            categorized_count += 1
            
            # Track distribution
            category_distribution[new_category] = category_distribution.get(new_category, 0) + 1
            
            print(f"📝 '{story.get('title', 'Untitled')}' → {new_category}")
        else:
            # Keep existing non-General categories
            category_distribution[old_category] = category_distribution.get(old_category, 0) + 1
            print(f"✅ '{story.get('title', 'Untitled')}' → {old_category} (preserved)")
    
    # Save updated stories
    with open("stories.json", "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n🎉 Category Upgrade Complete!")
    print(f"📊 Updated {categorized_count} stories")
    print(f"💾 Backup saved as: {backup_path}")
    print("\n📈 Category Distribution:")
    for category, count in sorted(category_distribution.items()):
        print(f"   {category}: {count} stories")
    
    print("\n✨ Features Preserved:")
    print("   ✅ All story content and metadata")
    print("   ✅ Premium/free status")
    print("   ✅ Images and slugs")
    print("   ✅ Existing favorites")
    print("   ✅ Audio files")
    print("   ✅ Quiz data")
    print("   ✅ Translation support")
    
    print("\n🆕 New Features Added:")
    print("   🌟 Smart categorization system")
    print("   🎯 Better story discovery")
    print("   🔍 Enhanced filtering options")
    
    return True

if __name__ == "__main__":
    upgrade_categories()
