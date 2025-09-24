import streamlit as st
import base64
from pathlib import Path

st.title("Audio Test")

# Test if we can play audio files
audio_file = Path("audio/click.mp3")

if audio_file.exists():
    st.write(f"Audio file exists: {audio_file}")
    
    # Try method 1: Direct file path
    st.write("Method 1: Direct audio element")
    try:
        audio_bytes = audio_file.read_bytes()
        st.audio(audio_bytes, format='audio/mp3')
    except Exception as e:
        st.error(f"Error with st.audio: {e}")
    
    # Try method 2: HTML with data URI
    st.write("Method 2: HTML with data URI")
    try:
        audio_bytes = audio_file.read_bytes()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        
        html = f"""
        <audio controls autoplay>
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error with HTML method: {e}")
    
    # Try method 3: Button that plays sound
    if st.button("Play Click Sound"):
        try:
            import streamlit.components.v1 as components
            
            audio_bytes = audio_file.read_bytes()
            audio_b64 = base64.b64encode(audio_bytes).decode()
            
            html = f"""
            <audio id="test_audio" preload="auto">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
            <script>
                document.getElementById('test_audio').play();
            </script>
            """
            components.html(html, height=0)
            st.success("Attempted to play sound!")
        except Exception as e:
            st.error(f"Error playing sound: {e}")
else:
    st.error(f"Audio file not found: {audio_file}")
    
    # List available files
    audio_dir = Path("audio")
    if audio_dir.exists():
        st.write("Available audio files:")
        for f in audio_dir.glob("*.mp3"):
            st.write(f"- {f.name}")
