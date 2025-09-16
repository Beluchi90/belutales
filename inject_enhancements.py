import streamlit as st
import streamlit.components.v1 as components

def inject_enhanced_features():
    """Inject enhanced fonts and sounds into any Streamlit app"""
    
    # Enhanced CSS and JavaScript injection
    enhanced_code = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Nunito:wght@400;500;600;700;800&display=swap');
    
    /* Force fonts on ALL elements */
    .stApp, .stApp * {
        font-family: 'Nunito', 'Trebuchet MS', sans-serif !important;
    }
    
    /* Force heading fonts */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        font-family: 'Baloo 2', 'Comic Sans MS', cursive, sans-serif !important;
        font-weight: 700 !important;
        color: white !important;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        font-family: 'Baloo 2', cursive, sans-serif !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
    }
    
    /* Story text */
    .stMarkdown p {
        font-family: 'Nunito', sans-serif !important;
        font-size: 1.125rem !important;
        line-height: 1.8 !important;
        font-weight: 500 !important;
    }
    
    /* Visual indicator that enhancements are active */
    .enhancement-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: linear-gradient(135deg, #facc15, #38bdf8);
        color: #1e1b4b;
        padding: 8px 12px;
        border-radius: 20px;
        font-family: 'Baloo 2', cursive, sans-serif;
        font-weight: 700;
        font-size: 12px;
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    </style>
    
    <div class="enhancement-indicator">
        ✨ Enhanced Fonts Active
    </div>
    
    <script>
    // Enhanced click sound system
    let soundEnabled = true;
    let soundVolume = 0.3;
    
    function playEnhancedClickSound() {
        if (!soundEnabled) return;
        
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            // Pleasant click sound
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.1);
            
            gainNode.gain.setValueAtTime(soundVolume, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.1);
            
            oscillator.type = 'sine';
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.1);
            
            // Update indicator
            const indicator = document.querySelector('.enhancement-indicator');
            if (indicator) {
                indicator.textContent = '🔊 Click Sound Played!';
                setTimeout(() => {
                    indicator.textContent = '✨ Enhanced Fonts & Sounds Active';
                }, 1000);
            }
        } catch (e) {
            console.log('Sound failed:', e);
        }
    }
    
    // Add click listeners to ALL buttons
    function addClickSounds() {
        document.querySelectorAll('button').forEach(button => {
            if (!button.hasAttribute('data-sound-added')) {
                button.addEventListener('click', playEnhancedClickSound);
                button.setAttribute('data-sound-added', 'true');
            }
        });
        
        // Also add to select elements
        document.querySelectorAll('select').forEach(select => {
            if (!select.hasAttribute('data-sound-added')) {
                select.addEventListener('change', playEnhancedClickSound);
                select.setAttribute('data-sound-added', 'true');
            }
        });
    }
    
    // Initial setup
    setTimeout(addClickSounds, 1000);
    
    // Re-add sounds when page updates (Streamlit re-renders)
    setInterval(addClickSounds, 2000);
    
    // Test sound on load
    setTimeout(() => {
        playEnhancedClickSound();
    }, 2000);
    
    console.log('🎉 BeluTales Enhanced Features Injected!');
    </script>
    """
    
    # Inject the code
    components.html(enhanced_code, height=0)

# Auto-run if this file is executed directly
if __name__ == "__main__":
    st.title("🚀 BeluTales Enhancement Injector")
    st.write("This will inject enhanced fonts and sounds into any Streamlit app!")
    
    if st.button("🎨 Activate Enhanced Features"):
        inject_enhanced_features()
        st.success("✅ Enhanced features injected!")
        st.balloons()

