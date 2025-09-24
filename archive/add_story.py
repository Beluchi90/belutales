import streamlit as st
import json
import os
from datetime import datetime

def load_stories():
    try:
        with open("stories.json", "r", encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_stories(stories):
    with open("stories.json", "w", encoding='utf-8') as file:
        json.dump(stories, indent=4, ensure_ascii=False)

st.title("📝 Add New Story to BeluTales")

# Load existing stories
stories = load_stories()

# Story type selection
story_type = st.selectbox(
    "Select Story Type",
    ["Regular Story", "Poetry/Song"]
)

# Basic information
title = st.text_input("Story Title")
category = st.text_input("Category", value="Moral Stories" if story_type == "Regular Story" else "Poetry & Songs")
age_range = st.text_input("Age Range (e.g., '5-10')")
reading_time = st.text_input("Reading Time (e.g., '5 minutes')")

# Tags
tags = st.text_input("Tags (comma-separated)")

if story_type == "Poetry/Song":
    # Poetry/Song specific fields
    author = st.text_input("Author")
    published_year = st.number_input("Published Year", min_value=1, max_value=datetime.now().year, value=2024)
    background = st.text_area("Historical Background/Context")
    
    # Structured content
    introduction = st.text_area("Introduction")
    
    # Verse input
    st.subheader("Add Verses")
    st.write("Enter each line of the verse, press Enter for a new line. Leave a blank line to start a new verse.")
    verse_text = st.text_area("Verses (one line per verse line, blank line between verses)")
    
    meaning = st.text_area("Meaning")
    conclusion = st.text_area("Conclusion")
else:
    # Regular story content
    content = st.text_area("Story Content")
    moral = st.text_area("Moral of the Story (optional)")

# Image upload
st.write("Note: Place the image in the 'images' folder and provide the filename below")
image_filename = st.text_input("Image Filename (e.g., 'story_title.jpg')")

if st.button("Add Story"):
    new_story = {
        "title": title,
        "category": category,
        "ageRange": age_range,
        "readingTime": reading_time,
        "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
        "image": image_filename,
        "dateAdded": datetime.now().strftime("%Y-%m-%d"),
        "lastUpdated": datetime.now().strftime("%Y-%m-%d")
    }

    if story_type == "Poetry/Song":
        new_story.update({
            "author": author,
            "publishedYear": published_year,
            "background": background,
            "content": {
                "introduction": introduction,
                "songLyrics": [],
                "meaning": meaning,
                "conclusion": conclusion
            }
        })
        
        # Process verses
        verses = []
        current_verse = []
        for line in verse_text.split("\n"):
            if line.strip():
                current_verse.append(line.strip())
            elif current_verse:  # Empty line and we have verses collected
                verses.append({f"verse{len(verses)+1}": current_verse})
                current_verse = []
        if current_verse:  # Add the last verse if exists
            verses.append({f"verse{len(verses)+1}": current_verse})
        
        new_story["content"]["songLyrics"] = verses
    else:
        new_story["content"] = content
        if moral:
            new_story["moral"] = moral

    # Add the new story to the list
    stories.append(new_story)
    
    # Save updated stories
    save_stories(stories)
    
    st.success(f"Successfully added '{title}' to the stories collection!")
    st.write("New story details:", new_story) 