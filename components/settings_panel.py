# components/settings_panel.py — Enhanced settings panel for BeluTales
import streamlit as st

# Import functions with error handling
try:
    from components.audio_manager import get_audio_manager, play_click_sound
except ImportError:
    def get_audio_manager():
        class DummyAudioManager:
            def play_ambience(self, *args, **kwargs): pass
        return DummyAudioManager()
    def play_click_sound(): pass

try:
    from components.quiz_enhanced import render_quiz_statistics
except ImportError:
    def render_quiz_statistics():
        import streamlit as st
        st.info("Quiz statistics not available")

def render_settings_panel():
    """Render the enhanced settings panel"""
    import streamlit as st  # Ensure streamlit is available in function scope
    audio_manager = get_audio_manager()
    
    st.markdown("### ⚙️ Settings")
    
    # Premium Status (if available)
    try:
        from paypal_integration import get_premium_stats
        premium_stats = get_premium_stats()
        if premium_stats["active"]:
            st.success("✅ Premium Active")
            if premium_stats["expires"]:
                st.caption(f"Expires: {premium_stats['expires']}")
        else:
            st.info("💎 Premium: Inactive")
        st.markdown("---")
    except ImportError:
        pass
    
    # Audio Settings Section
    with st.expander("🔊 Audio Settings", expanded=True):
        
        # Master audio toggle
        master_audio = st.checkbox(
            "Enable Audio", 
            value=st.session_state.get("master_audio_enabled", True),
            key="master_audio_enabled",
            help="Master switch for all audio features"
        )
        
        if master_audio:
            # Sound Effects
            col1, col2 = st.columns([3, 1])
            with col1:
                sfx_enabled = st.checkbox(
                    "Sound Effects (clicks, success sounds)", 
                    value=st.session_state.get("sfx_enabled", True),
                    key="sfx_enabled"
                )
            with col2:
                if sfx_enabled:
                    if st.button("🔊 Test", key="test_sfx"):
                        play_click_sound()
            
            # Volume controls
            if sfx_enabled:
                volume = st.slider(
                    "SFX Volume",
                    min_value=0.0,
                    max_value=1.0,
                    value=st.session_state.get("volume", 0.7),
                    step=0.1,
                    key="volume"
                )
            
            # Narration Settings
            st.markdown("**Story Narration**")
            narration_enabled = st.checkbox(
                "Enable story narration (text-to-speech)",
                value=st.session_state.get("narration_enabled", True),
                key="narration_enabled"
            )
            
            if narration_enabled:
                narration_volume = st.slider(
                    "Narration Volume",
                    min_value=0.0,
                    max_value=1.0,
                    value=st.session_state.get("narration_volume", 0.8),
                    step=0.1,
                    key="narration_volume"
                )
            
            # Ambience Settings
            st.markdown("**Background Ambience**")
            ambience_enabled = st.checkbox(
                "Enable background ambience (nature sounds)",
                value=st.session_state.get("ambience_enabled", False),
                key="ambience_enabled",
                help="Plays gentle background sounds while reading stories"
            )
            
            if ambience_enabled:
                col1, col2 = st.columns([3, 1])
                with col1:
                    ambience_volume = st.slider(
                        "Ambience Volume",
                        min_value=0.0,
                        max_value=0.5,  # Lower max for ambience
                        value=st.session_state.get("ambience_volume", 0.3),
                        step=0.1,
                        key="ambience_volume"
                    )
                
                with col2:
                    if st.button("🎵 Test", key="test_ambience"):
                        audio_manager.play_ambience("forest", loop=False)
                
                # Ambience type selection
                ambience_type = st.selectbox(
                    "Ambience Type",
                    ["forest", "rain", "ocean", "night", "birds"],
                    index=0,
                    key="ambience_type"
                )
        
        else:
            # Disable all audio when master is off
            st.session_state.sfx_enabled = False
            st.session_state.narration_enabled = False
            st.session_state.ambience_enabled = False
    
    # Quiz Settings Section
    with st.expander("🧠 Quiz Settings", expanded=False):
        quiz_difficulty = st.selectbox(
            "Quiz Difficulty",
            ["Easy", "Normal", "Hard"],
            index=1,  # Default to Normal
            key="quiz_difficulty",
            help="Easy: Unlimited time, hints available\nNormal: 60s per quiz, retries allowed\nHard: 30s per quiz, no hints or retries"
        )
        
        st.markdown("**Difficulty Features:**")
        if quiz_difficulty == "Easy":
            st.info("• Unlimited time\n• Hints available\n• Unlimited retries")
        elif quiz_difficulty == "Normal":
            st.info("• 60 second time limit\n• Retries allowed\n• No hints")
        else:  # Hard
            st.warning("• 30 second time limit\n• No retries\n• No hints")
        
        # Quiz statistics
        st.markdown("**Your Quiz Statistics:**")
        render_quiz_statistics()
    
    # Display Settings Section
    with st.expander("🎨 Display Settings", expanded=False):
        
        # Theme preferences (if implemented)
        theme_preference = st.selectbox(
            "Theme Preference",
            ["Auto", "Light", "Dark"],
            index=0,
            key="theme_preference",
            help="Theme preference (requires page refresh)"
        )
        
        # Animation settings
        animations_enabled = st.checkbox(
            "Enable animations (confetti, transitions)",
            value=st.session_state.get("animations_enabled", True),
            key="animations_enabled"
        )
        
        # Font size adjustment
        font_size = st.selectbox(
            "Story Text Size",
            ["Small", "Medium", "Large", "Extra Large"],
            index=1,  # Default to Medium
            key="font_size_preference"
        )
        
        # Language preferences (already handled in main app)
        st.markdown("**Language Settings**")
        st.info("Language selection is available in the main header.")
    
    # Accessibility Settings Section
    with st.expander("♿ Accessibility Settings", expanded=False):
        
        # Screen reader support
        screen_reader_mode = st.checkbox(
            "Enhanced screen reader support",
            value=st.session_state.get("screen_reader_mode", False),
            key="screen_reader_mode",
            help="Provides additional announcements for screen readers"
        )
        
        # High contrast mode
        high_contrast = st.checkbox(
            "High contrast mode",
            value=st.session_state.get("high_contrast_mode", False),
            key="high_contrast_mode",
            help="Increases color contrast for better visibility"
        )
        
        # Reduced motion
        reduced_motion = st.checkbox(
            "Reduce motion and animations",
            value=st.session_state.get("reduced_motion", False),
            key="reduced_motion",
            help="Minimizes animations and transitions"
        )
        
        # Focus indicators
        enhanced_focus = st.checkbox(
            "Enhanced focus indicators",
            value=st.session_state.get("enhanced_focus", False),
            key="enhanced_focus",
            help="More visible focus indicators for keyboard navigation"
        )
    
    # Data Management Section
    with st.expander("📊 Data Management", expanded=False):
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Quiz Progress", use_container_width=True):
                play_click_sound()
                # Export quiz progress as JSON
                import json
                progress_data = st.session_state.get("quiz_progress", {})
                if progress_data:
                    json_str = json.dumps(progress_data, indent=2)
                    st.download_button(
                        label="Download quiz_progress.json",
                        data=json_str,
                        file_name="belutales_quiz_progress.json",
                        mime="application/json"
                    )
                else:
                    st.info("No quiz progress to export yet.")
        
        with col2:
            if st.button("🗑️ Reset All Data", use_container_width=True):
                play_click_sound()
                
                # Confirmation dialog
                if st.checkbox("I understand this will delete all my progress"):
                    if st.button("⚠️ Confirm Reset", type="primary"):
                        # Clear all user data
                        keys_to_clear = [
                            "quiz_progress", "quiz_scores", "quiz_answers", 
                            "favorites", "user_preferences"
                        ]
                        for key in keys_to_clear:
                            if key in st.session_state:
                                del st.session_state[key]
                        
                        st.success("All data has been reset!")
                        st.rerun()
    
    # App Information Section
    with st.expander("ℹ️ About BeluTales", expanded=False):
        st.markdown("""
        **BeluTales** - Magical bedtime stories for children
        
        **Features:**
        - 🦉 100+ original stories in multiple languages
        - 🧠 Interactive quizzes with progress tracking
        - 🔊 Audio narration and sound effects
        - ❤️ Favorites system
        - 🌍 Multi-language support with translation
        - 🎨 Beautiful illustrations for each story
        
        **Version:** 2.0.0 Enhanced
        **Last Updated:** 2024
        
        Made with ❤️ using Streamlit
        """)
        
        # System information for debugging
        if st.checkbox("Show system information"):
            import platform
            import streamlit as st
            st.code(f"""
            Python: {platform.python_version()}
            Streamlit: {st.__version__}
            Platform: {platform.system()} {platform.release()}
            """)

def render_settings_button():
    """Render a compact settings button for the main interface"""
    if st.button("⚙️", help="Settings", key="settings_button"):
        play_click_sound()
        return True
    return False
