# components/audio_manager.py — Enhanced audio management with SFX and ambience
import streamlit as st
from pathlib import Path
import time
import os
import base64

class AudioManager:
    """Centralized audio management for the BeluTales app"""
    
    def __init__(self):
        import streamlit as st
        self.audio_dir = Path("audio")
        self.sounds_dir = Path("public/assets/sounds") if Path("public/assets/sounds").exists() else Path("audio")
        
        # Default settings
        self.default_settings = {
            "sfx_enabled": True,
            "volume": 0.7,
            "ambience_enabled": False,
            "ambience_volume": 0.3,
            "narration_enabled": True,
            "narration_volume": 0.8
        }
        
        # Initialize settings in session state
        for key, default in self.default_settings.items():
            if key not in st.session_state:
                st.session_state[key] = default
    
    def is_sound_enabled(self, sound_type="sfx"):
        """Check if a specific type of sound is enabled"""
        import streamlit as st
        if sound_type == "sfx":
            return st.session_state.get("sfx_enabled", True)
        elif sound_type == "ambience":
            return st.session_state.get("ambience_enabled", False)
        elif sound_type == "narration":
            return st.session_state.get("narration_enabled", True)
        return False
    
    def get_volume(self, sound_type="sfx"):
        """Get volume for a specific type of sound"""
        import streamlit as st
        if sound_type == "sfx":
            return st.session_state.get("volume", 0.7)
        elif sound_type == "ambience":
            return st.session_state.get("ambience_volume", 0.3)
        elif sound_type == "narration":
            return st.session_state.get("narration_volume", 0.8)
        return 0.5
    
    def play_sound_effect(self, sound_name: str, auto_play=True):
        """Play a sound effect if enabled"""
        if not self.is_sound_enabled("sfx"):
            return False
        
        # Try multiple possible file locations and formats
        possible_paths = [
            self.sounds_dir / f"{sound_name}.mp3",
            self.sounds_dir / f"{sound_name}.wav",
            self.audio_dir / f"{sound_name}.mp3",
            self.audio_dir / f"{sound_name}.wav"
        ]
        
        audio_path = None
        for path in possible_paths:
            if path.exists():
                audio_path = path
                break
        
        if not audio_path:
            # Create a fallback silent audio element
            import streamlit as st
            st.markdown(f"<!-- Sound effect '{sound_name}' not found -->", unsafe_allow_html=True)
            return False
        
        # Read and encode audio file
        try:
            audio_bytes = audio_path.read_bytes()
            audio_b64 = base64.b64encode(audio_bytes).decode()
        except Exception as e:
            import streamlit as st
            st.markdown(f"<!-- Error reading audio file: {e} -->", unsafe_allow_html=True)
            return False
        
        volume = self.get_volume("sfx")
        
        # Create HTML audio element with base64 data
        audio_id = f"sfx_{sound_name}_{int(time.time() * 1000)}"
        audio_html = f"""
        <div style="display: none;">
            <audio id="{audio_id}" preload="auto">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
        </div>
        """
        
        if auto_play:
            audio_html += f"""
            <script type="text/javascript">
                setTimeout(function() {{
                    try {{
                        console.log('Attempting to play sound: {sound_name}');
                        const audio = document.getElementById('{audio_id}');
                        if (audio) {{
                            console.log('Audio element found, setting volume to {volume}');
                            audio.volume = {volume};
                            const playPromise = audio.play();
                            if (playPromise !== undefined) {{
                                playPromise.then(_ => {{
                                    console.log('Audio playing successfully: {sound_name}');
                                }}).catch(function(e) {{
                                    console.log('Audio autoplay prevented by browser:', e.message);
                                    // Try playing with user interaction
                                    document.addEventListener('click', function() {{
                                        audio.play().catch(console.log);
                                    }}, {{ once: true }});
                                }});
                            }}
                        }} else {{
                            console.log('Audio element not found: {audio_id}');
                        }}
                    }} catch (e) {{
                        console.log('Audio error:', e.message);
                    }}
                }}, 100);
            </script>
            """
        
        import streamlit as st
        import streamlit.components.v1 as components
        
        # Use components.html for better script execution
        components.html(audio_html, height=0)
        return True
    
    def play_ambience(self, ambience_name="forest", loop=True):
        """Play background ambience if enabled"""
        if not self.is_sound_enabled("ambience"):
            return False
        
        # Try to find ambience file
        possible_paths = [
            self.sounds_dir / "ambience" / f"{ambience_name}.mp3",
            self.sounds_dir / f"ambience_{ambience_name}.mp3",
            self.audio_dir / f"ambience_{ambience_name}.mp3"
        ]
        
        audio_path = None
        web_audio_path = None
        for path in possible_paths:
            if path.exists():
                audio_path = str(path)
                # Convert to web-accessible path
                if "audio/" in audio_path:
                    web_audio_path = f"./audio/ambience_{ambience_name}.mp3"
                else:
                    web_audio_path = f"./sounds/ambience_{ambience_name}.mp3"
                break
        
        if not audio_path:
            return False
        
        volume = self.get_volume("ambience")
        loop_attr = "loop" if loop else ""
        
        # Create persistent ambience player with better error handling
        ambience_html = f"""
        <div style="display: none;">
            <audio id="ambience_player" {loop_attr}>
                <source src="{web_audio_path}" type="audio/mpeg">
            </audio>
        </div>
        <script type="text/javascript">
            setTimeout(function() {{
                try {{
                    const ambiencePlayer = document.getElementById('ambience_player');
                    if (ambiencePlayer) {{
                        ambiencePlayer.volume = {volume};
                        ambiencePlayer.play().catch(function(e) {{
                            console.log('Ambience autoplay prevented by browser:', e.message);
                        }});
                    }}
                }} catch (e) {{
                    console.log('Ambience error:', e.message);
                }}
            }}, 100);
        </script>
        """
        
        import streamlit as st
        import streamlit.components.v1 as components
        
        # Use components.html for better script execution
        components.html(ambience_html, height=0)
        return True
    
    def stop_ambience(self):
        """Stop background ambience"""
        import streamlit as st
        stop_html = """
        <script>
            var ambiencePlayer = document.getElementById('ambience_player');
            if (ambiencePlayer) {
                ambiencePlayer.pause();
                ambiencePlayer.currentTime = 0;
            }
        </script>
        """
        import streamlit.components.v1 as components
        components.html(stop_html, height=0)
    
    def create_audio_controls(self, audio_path: str, label="Play Audio"):
        """Create enhanced audio controls for story narration"""
        import streamlit as st
        if not Path(audio_path).exists():
            st.info("Audio narration not available for this story.")
            return
        
        volume = self.get_volume("narration")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button(f"🔊 {label}", use_container_width=True):
                self.play_sound_effect("click", auto_play=True)
                
                # Read and encode the narration audio file
                try:
                    audio_file = Path(audio_path)
                    audio_bytes = audio_file.read_bytes()
                    audio_b64 = base64.b64encode(audio_bytes).decode()
                    
                    # Play narration with base64 encoding
                    audio_html = f"""
                    <audio controls autoplay style="width: 100%;">
                        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                        Your browser does not support the audio element.
                    </audio>
                    <script type="text/javascript">
                        setTimeout(function() {{
                            try {{
                                console.log('Playing narration audio');
                                const audioElements = document.querySelectorAll('audio[controls]');
                                const latestAudio = audioElements[audioElements.length - 1];
                                if (latestAudio) {{
                                    latestAudio.volume = {volume};
                                    console.log('Narration volume set to {volume}');
                                }}
                            }} catch (e) {{
                                console.log('Audio volume setting error:', e.message);
                            }}
                        }}, 100);
                    </script>
                    """
                    import streamlit.components.v1 as components
                    components.html(audio_html, height=50)
                    
                except Exception as e:
                    st.error(f"Error loading audio file: {e}")
                    return
        
        with col2:
            if st.button("⏸️ Stop"):
                self.play_sound_effect("click", auto_play=True)
                # Stop all audio with better error handling
                stop_html = """
                <script type="text/javascript">
                    setTimeout(function() {
                        try {
                            document.querySelectorAll('audio').forEach(function(audio) {
                                audio.pause();
                                audio.currentTime = 0;
                            });
                        } catch (e) {
                            console.log('Audio stop error:', e.message);
                        }
                    }, 50);
                </script>
                """
                import streamlit.components.v1 as components
                components.html(stop_html, height=0)

# Create a global audio manager instance
def get_audio_manager():
    """Get or create the global audio manager instance"""
    import streamlit as st
    if "audio_manager" not in st.session_state:
        st.session_state.audio_manager = AudioManager()
    return st.session_state.audio_manager

# Convenience functions for common operations
def play_click_sound():
    """Quick function to play click sound"""
    try:
        audio_manager = get_audio_manager()
        if audio_manager.is_sound_enabled("sfx"):
            audio_manager.play_sound_effect("click")
    except Exception as e:
        print(f"Click sound error: {e}")

def play_success_sound():
    """Quick function to play success sound"""
    try:
        audio_manager = get_audio_manager()
        if audio_manager.is_sound_enabled("sfx"):
            audio_manager.play_sound_effect("success")
    except Exception as e:
        print(f"Success sound error: {e}")

def play_error_sound():
    """Quick function to play error sound"""
    try:
        audio_manager = get_audio_manager()
        if audio_manager.is_sound_enabled("sfx"):
            audio_manager.play_sound_effect("error")
    except Exception as e:
        print(f"Error sound error: {e}")
