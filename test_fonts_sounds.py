import streamlit as st
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="BeluTales - Font & Sound Test",
    page_icon="✨",
    layout="wide"
)

# Enhanced CSS with fonts and styling
ENHANCED_CSS = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Nunito:wght@400;500;600;700;800&display=swap');

/* Apply fonts globally with maximum specificity */
html, body, div, span, h1, h2, h3, h4, h5, h6, p, a, button, input, select, textarea,
.stApp, .stApp *, 
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] *,
[data-testid="stSidebar"], [data-testid="stSidebar"] *,
.css-1d391kg, .css-1d391kg *,
.css-1cypcdb, .css-1cypcdb * {
    font-family: 'Nunito', 'Arial', sans-serif !important;
}

/* Force headings to use Baloo 2 */
h1, h2, h3, h4, h5, h6,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
[data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3, [data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5, [data-testid="stMarkdownContainer"] h6 {
    font-family: 'Baloo 2', 'Comic Sans MS', cursive, sans-serif !important;
    font-weight: 700 !important;
    color: #facc15 !important;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%) !important;
}

/* Enhanced buttons */
.stButton > button {
    background: linear-gradient(135deg, #facc15, #38bdf8) !important;
    color: #1e1b4b !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 12px 24px !important;
    font-family: 'Baloo 2', cursive, sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(250, 204, 21, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: 0 8px 20px rgba(250, 204, 21, 0.5) !important;
}

/* Status indicator */
.font-status {
    position: fixed;
    top: 10px;
    right: 10px;
    background: linear-gradient(135deg, #34d399, #38bdf8);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-family: 'Baloo 2', cursive, sans-serif !important;
    font-weight: 700;
    font-size: 12px;
    z-index: 9999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* Test text styles */
.test-heading {
    font-family: 'Baloo 2', cursive, sans-serif !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    color: #facc15 !important;
    text-align: center;
    margin: 20px 0;
}

.test-body {
    font-family: 'Nunito', sans-serif !important;
    font-size: 1.2rem !important;
    font-weight: 500 !important;
    color: white !important;
    text-align: center;
    line-height: 1.6;
    margin: 20px 0;
}
</style>

<div class="font-status" id="font-indicator">
    🎨 Loading Enhanced Fonts...
</div>

<script>
// Enhanced sound system
class EnhancedAudio {
    constructor() {
        this.enabled = true;
        this.volume = 0.4;
        this.audioContext = null;
        this.initAudio();
    }
    
    initAudio() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            console.log('✅ Audio Context initialized');
        } catch (e) {
            console.log('❌ Audio Context failed:', e);
        }
    }
    
    playClickSound() {
        if (!this.enabled || !this.audioContext) return;
        
        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            // Pleasant click sound
            oscillator.frequency.setValueAtTime(800, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(400, this.audioContext.currentTime + 0.12);
            
            gainNode.gain.setValueAtTime(this.volume, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + 0.12);
            
            oscillator.type = 'sine';
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.12);
            
            // Update indicator
            this.updateStatus('🔊 Click Sound Played!');
            
        } catch (e) {
            console.log('❌ Sound error:', e);
            this.playFallbackSound();
        }
    }
    
    playFallbackSound() {
        try {
            // Simple beep using HTML5 Audio
            const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSyCz/LdeSQGLIXO8tiMOAkZZ7zr7qNBFAREn+DysmETBSJ7');
            audio.volume = this.volume;
            audio.play().catch(() => console.log('Fallback audio failed'));
        } catch (e) {
            console.log('All audio methods failed');
        }
    }
    
    updateStatus(message) {
        const indicator = document.getElementById('font-indicator');
        if (indicator) {
            const originalText = indicator.textContent;
            indicator.textContent = message;
            setTimeout(() => {
                indicator.textContent = originalText;
            }, 1500);
        }
    }
}

// Initialize audio system
const audioSystem = new EnhancedAudio();

// Font detection and status update
function checkFonts() {
    setTimeout(() => {
        // Test Baloo 2
        const testEl = document.createElement('div');
        testEl.style.fontFamily = 'Baloo 2, cursive';
        testEl.style.position = 'absolute';
        testEl.style.visibility = 'hidden';
        testEl.textContent = 'Test';
        document.body.appendChild(testEl);
        
        const computed = window.getComputedStyle(testEl);
        const fontFamily = computed.fontFamily.toLowerCase();
        
        const indicator = document.getElementById('font-indicator');
        if (indicator) {
            if (fontFamily.includes('baloo')) {
                indicator.textContent = '✅ Baloo 2 + Nunito + Sounds Active';
                indicator.style.background = 'linear-gradient(135deg, #34d399, #38bdf8)';
            } else if (fontFamily.includes('nunito')) {
                indicator.textContent = '⚠️ Nunito Only (Baloo 2 Loading...)';
                indicator.style.background = 'linear-gradient(135deg, #f59e0b, #38bdf8)';
            } else {
                indicator.textContent = '❌ Default Fonts (Loading...)';
                indicator.style.background = 'linear-gradient(135deg, #ef4444, #f59e0b)';
            }
        }
        
        document.body.removeChild(testEl);
        
        // Test sound
        setTimeout(() => {
            audioSystem.playClickSound();
        }, 1000);
        
    }, 3000);
}

// Add click listeners
function addClickListeners() {
    document.querySelectorAll('button').forEach(button => {
        if (!button.hasAttribute('data-enhanced-sound')) {
            button.addEventListener('click', (e) => {
                audioSystem.playClickSound();
            });
            button.setAttribute('data-enhanced-sound', 'true');
        }
    });
}

// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
    checkFonts();
    addClickListeners();
});

// Re-run for Streamlit updates
setInterval(addClickListeners, 2000);

console.log('🚀 Enhanced BeluTales Font & Sound System Loaded!');
</script>
"""

# Apply the enhanced CSS
st.markdown(ENHANCED_CSS, unsafe_allow_html=True)

# Main content
st.markdown('<div class="test-heading">🌟 BeluTales Enhanced Test</div>', unsafe_allow_html=True)

st.markdown('<div class="test-body">This text should be using Nunito font (clean, rounded). The heading above should use Baloo 2 (playful, kid-friendly).</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎵 Test Click Sound"):
        st.success("Button clicked! Did you hear a sound?")

with col2:
    if st.button("🎨 Font Test"):
        st.info("Check the indicator in top-right corner!")

with col3:
    if st.button("✨ Magic Button"):
        st.balloons()

st.markdown("---")

st.markdown('<div class="test-body">Instructions:</div>', unsafe_allow_html=True)
st.markdown("""
1. **Look for the indicator** in the top-right corner
2. **Click any button** to test sounds
3. **Check if fonts look different** from default
4. **Tell me what the indicator shows**:
   - ✅ Green = Everything working
   - ⚠️ Yellow = Partial working  
   - ❌ Red = Not working
""")

# Debug info
with st.expander("🔧 Debug Information"):
    st.write("**Current URL:** Check if you're on the right port")
    st.write("**Browser:** Try Chrome/Edge for best compatibility")
    st.write("**Fonts:** Should load automatically from Google Fonts")
    st.write("**Sounds:** Uses Web Audio API with fallback")

