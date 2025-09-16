import streamlit as st
import json

st.set_page_config(page_title="BeluTales Test", page_icon="🦉", layout="wide")

# Simple test to see if we can load stories
st.title("🦉 BeluTales - Test Version")
st.write("Testing if the app loads properly...")

try:
    with open("stories.json", "r", encoding="utf-8", errors="ignore") as f:
        stories = json.load(f)
    
    st.success(f"✅ Successfully loaded {len(stories)} stories!")
    
    if stories:
        st.write("### First Story:")
        first_story = stories[0]
        st.write(f"**Title:** {first_story.get('title', 'No title')}")
        st.write(f"**Category:** {first_story.get('category', 'No category')}")
        
except Exception as e:
    st.error(f"❌ Error loading stories: {e}")

st.write("### If you can see this, the app is working!")
st.balloons()
