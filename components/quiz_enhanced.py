# components/quiz_enhanced.py — Enhanced quiz with feedback, sound effects & progress tracking
import streamlit as st
import json
import random
from pathlib import Path
try:
    from utils.state import set_qp
except ImportError:
    # Fallback for when utils.state is not available
    def set_qp(**kwargs):
        import streamlit as st
        for key, value in kwargs.items():
            if key != '_merge':
                st.session_state[key] = value

# Enhanced quiz settings and constants
QUIZ_DIFFICULTIES = {
    "Easy": {"time_limit": None, "hints_enabled": True, "retry_allowed": True},
    "Normal": {"time_limit": 60, "hints_enabled": False, "retry_allowed": True},
    "Hard": {"time_limit": 30, "hints_enabled": False, "retry_allowed": False}
}

def play_sound_effect(sound_name: str):
    """Play a sound effect if audio is enabled"""
    import streamlit as st
    if not st.session_state.get("sfx_enabled", True):
        return
    
    # Use HTML audio element for sound effects
    audio_path = f"audio/{sound_name}.mp3"
    if Path(audio_path).exists():
        st.markdown(f"""
        <audio autoplay>
            <source src="{audio_path}" type="audio/mpeg">
        </audio>
        """, unsafe_allow_html=True)

def get_quiz_progress(story_slug: str) -> dict:
    """Get quiz progress for a specific story"""
    import streamlit as st
    if "quiz_progress" not in st.session_state:
        st.session_state.quiz_progress = {}
    
    return st.session_state.quiz_progress.get(story_slug, {
        "completed": False,
        "score": 0,
        "total": 0,
        "attempts": 0,
        "best_score": 0,
        "perfect_attempts": 0
    })

def update_quiz_progress(story_slug: str, score: int, total: int):
    """Update quiz progress for a specific story"""
    import streamlit as st
    if "quiz_progress" not in st.session_state:
        st.session_state.quiz_progress = {}
    
    progress = get_quiz_progress(story_slug)
    progress["score"] = score
    progress["total"] = total
    progress["attempts"] += 1
    progress["completed"] = True
    
    if score > progress["best_score"]:
        progress["best_score"] = score
    
    if score == total:
        progress["perfect_attempts"] += 1
    
    st.session_state.quiz_progress[story_slug] = progress

def render_confetti_animation():
    """Render confetti animation for perfect scores"""
    import streamlit as st
    st.markdown("""
    <style>
    @keyframes confetti-fall {
        0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
    }
    
    .confetti {
        position: fixed;
        top: -10px;
        left: 50%;
        width: 10px;
        height: 10px;
        background: #ff6b6b;
        animation: confetti-fall 3s linear infinite;
        z-index: 1000;
    }
    
    .confetti:nth-child(2n) { background: #4ecdc4; animation-delay: 0.5s; }
    .confetti:nth-child(3n) { background: #45b7d1; animation-delay: 1s; }
    .confetti:nth-child(4n) { background: #f9ca24; animation-delay: 1.5s; }
    .confetti:nth-child(5n) { background: #6c5ce7; animation-delay: 2s; }
    </style>
    
    <div class="confetti" style="left: 10%;"></div>
    <div class="confetti" style="left: 20%;"></div>
    <div class="confetti" style="left: 30%;"></div>
    <div class="confetti" style="left: 40%;"></div>
    <div class="confetti" style="left: 50%;"></div>
    <div class="confetti" style="left: 60%;"></div>
    <div class="confetti" style="left: 70%;"></div>
    <div class="confetti" style="left: 80%;"></div>
    <div class="confetti" style="left: 90%;"></div>
    """, unsafe_allow_html=True)

def get_encouragement_message(score: int, total: int, attempts: int) -> str:
    """Get an encouraging message based on performance"""
    percentage = (score / total) * 100 if total > 0 else 0
    
    if percentage == 100:
        messages = [
            "🎉 Perfect! You're a quiz champion!",
            "🌟 Outstanding! Every answer was correct!",
            "🏆 Amazing! You got everything right!",
            "✨ Brilliant! Perfect score achieved!"
        ]
    elif percentage >= 80:
        messages = [
            "🎊 Excellent work! Almost perfect!",
            "👏 Great job! You really know this story!",
            "🌈 Wonderful! Just a few small mistakes!",
            "⭐ Fantastic! You're doing great!"
        ]
    elif percentage >= 60:
        messages = [
        "👍 Good effort! Keep practicing!",
        "🎯 Nice try! You're getting better!",
        "📚 Well done! Room for improvement!",
        "💪 Keep it up! You're learning!"
        ]
    else:
        messages = [
            "🌱 Every expert was once a beginner!",
            "📖 Try reading the story again!",
            "🤔 Take your time and think carefully!",
            "🌟 Don't give up! You can do this!"
        ]
    
    if attempts > 1:
        messages.append(f"🔄 Attempt #{attempts} - You're persistent!")
    
    return random.choice(messages)

def render_quiz_enhanced(story: dict, questions: list, open_panel: bool):
    """Enhanced quiz component with improved feedback and features"""
    import streamlit as st
    slug = story.get("slug", "unknown")
    
    # Add enhanced quiz button styling
    st.markdown("""
    <style>
    .quiz-option-button {
        width: 100%;
        padding: 12px 16px;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 600;
        font-family: 'Comic Neue', 'Baloo 2', cursive;
        border: 2px solid transparent;
        background: linear-gradient(135deg, #FFB6C1, #87CEEB);
        color: #2E2A65;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        min-height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 8px 0;
    }
    .quiz-option-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,182,193,0.4);
        background: linear-gradient(135deg, #FF9AA2, #74C0FC);
        border-color: #FF6B9D;
        animation: glow 0.6s ease-in-out;
    }
    .quiz-option-button:active {
        transform: translateY(0px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    @keyframes glow {
        0% { box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        50% { box-shadow: 0 8px 30px rgba(255,107,157,0.6); }
        100% { box-shadow: 0 8px 25px rgba(255,182,193,0.4); }
    }
    /* Style radio buttons to look like our custom buttons */
    .stRadio > div > label > div[data-testid="stMarkdownContainer"] {
        background: linear-gradient(135deg, #FFB6C1, #87CEEB);
        border-radius: 20px;
        padding: 12px 16px;
        margin: 8px 0;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        font-family: 'Comic Neue', 'Baloo 2', cursive;
        font-weight: 600;
        color: #2E2A65;
    }
    .stRadio > div > label:hover > div[data-testid="stMarkdownContainer"] {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,182,193,0.4);
        background: linear-gradient(135deg, #FF9AA2, #74C0FC);
        border-color: #FF6B9D;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize quiz session state
    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {}
    
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    
    # Get user settings
    difficulty = st.session_state.get("quiz_difficulty", "Normal")
    settings = QUIZ_DIFFICULTIES[difficulty]
    
    if not open_panel:
        progress = get_quiz_progress(slug)
        
        # Show quiz start button with progress indicator
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button("🧠 Start Quiz", use_container_width=True):
                play_sound_effect("click")
                set_qp(cat=story.get("category", ""), pick=slug, quiz="1", _merge=False)
        
        with col2:
            if progress["completed"]:
                st.metric("Best", f"{progress['best_score']}/{progress['total']}")
        
        # Show quiz stats if completed before
        if progress["completed"]:
            with st.expander(f"📊 Quiz Stats", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Attempts", progress["attempts"])
                with col2:
                    st.metric("Perfect Scores", progress["perfect_attempts"])
                with col3:
                    best_percentage = (progress["best_score"] / progress["total"]) * 100 if progress["total"] > 0 else 0
                    st.metric("Best %", f"{best_percentage:.0f}%")
        
        return
    
    # Quiz panel is open
    with st.container():
        st.markdown('<div class="bt-card">', unsafe_allow_html=True)
        
        # Quiz header with difficulty indicator
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🧠 Quiz")
        with col2:
            st.markdown(f"*{difficulty}*")
        
        if not questions:
            st.info("No quiz available for this story yet.")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # Initialize answers tracking for this quiz session
        quiz_session_key = f"{slug}_current_session"
        if quiz_session_key not in st.session_state:
            st.session_state[quiz_session_key] = {
                "answers": {},
                "submitted": {},
                "start_time": None
            }
        
        session = st.session_state[quiz_session_key]
        total_questions = len(questions)
        
        # Time tracking for timed quizzes
        if settings["time_limit"] and session["start_time"] is None:
            import time
            session["start_time"] = time.time()
        
        # Render questions
        for i, q in enumerate(questions, 1):
            question_key = f"{slug}_q{i}"
            
            with st.container():
                st.markdown(f"**Question {i}/{total_questions}**")
                st.markdown(f"*{q['question']}*")
                
                # Radio buttons for options
                selected = st.radio(
                    "Choose your answer:",
                    q["options"],
                    key=f"{question_key}_radio",
                    label_visibility="collapsed"
                )
                
                # Play click sound when selection changes
                if selected != session["answers"].get(i):
                    play_sound_effect("click")
                
                session["answers"][i] = selected
                
                # Check answer button
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if st.button(f"Check Q{i}", key=f"{question_key}_check"):
                        play_sound_effect("click")
                        session["submitted"][i] = True
                
                # Show feedback if submitted
                if session["submitted"].get(i, False):
                    is_correct = selected == q["answer"]
                    
                    if is_correct:
                        st.success("✅ Correct!")
                        play_sound_effect("success")
                    else:
                        st.error(f"❌ Incorrect. {q.get('explanation', 'Try again!')}")
                        if settings["hints_enabled"] and "hint" in q:
                            st.info(f"💡 Hint: {q['hint']}")
                
                st.markdown("---")
        
        # Calculate score and show results
        submitted_count = len(session["submitted"])
        if submitted_count > 0:
            correct_count = sum(
                1 for i in session["submitted"].keys()
                if session["answers"].get(i) == questions[i-1]["answer"]
            )
            
            # Show current progress
            st.markdown(f"**Progress:** {submitted_count}/{total_questions} answered")
            st.progress(submitted_count / total_questions)
            
            if submitted_count == total_questions:
                # All questions answered - show final results
                st.markdown("---")
                st.markdown("### 🎯 Quiz Results")
                
                percentage = (correct_count / total_questions) * 100
                
                # Update progress tracking
                progress = get_quiz_progress(slug)
                update_quiz_progress(slug, correct_count, total_questions)
                
                # Score display
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Score", f"{correct_count}/{total_questions}")
                with col2:
                    st.metric("Percentage", f"{percentage:.0f}%")
                with col3:
                    st.metric("Attempt", progress["attempts"] + 1)
                
                # Encouraging message
                message = get_encouragement_message(correct_count, total_questions, progress["attempts"] + 1)
                st.markdown(f"**{message}**")
                
                # Perfect score celebration
                if correct_count == total_questions:
                    st.balloons()
                    render_confetti_animation()
                    
                    # Achievement badge
                    if progress["perfect_attempts"] == 0:  # First perfect score
                        st.markdown("🏅 **First Perfect Score Achievement Unlocked!**")
                
                # Action buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if settings["retry_allowed"] and st.button("🔄 Try Again", use_container_width=True):
                        # Reset quiz session
                        del st.session_state[quiz_session_key]
                        st.rerun()
                
                with col2:
                    if st.button("✅ Done", use_container_width=True):
                        play_sound_effect("click")
                        # Clean up session
                        if quiz_session_key in st.session_state:
                            del st.session_state[quiz_session_key]
                        set_qp(cat=story.get("category", ""), pick=slug, quiz=None, _merge=False)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_quiz_statistics():
    """Render overall quiz statistics across all stories"""
    import streamlit as st
    if "quiz_progress" not in st.session_state or not st.session_state.quiz_progress:
        st.info("No quiz data available yet. Complete some quizzes to see your statistics!")
        return
    
    progress_data = st.session_state.quiz_progress
    
    # Overall statistics
    total_quizzes = len(progress_data)
    completed_quizzes = sum(1 for p in progress_data.values() if p["completed"])
    total_attempts = sum(p["attempts"] for p in progress_data.values())
    perfect_scores = sum(p["perfect_attempts"] for p in progress_data.values())
    
    # Display stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Quizzes Completed", f"{completed_quizzes}/{total_quizzes}")
    with col2:
        st.metric("Total Attempts", total_attempts)
    with col3:
        st.metric("Perfect Scores", perfect_scores)
    with col4:
        completion_rate = (completed_quizzes / total_quizzes) * 100 if total_quizzes > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.0f}%")
    
    # Detailed breakdown
    if st.checkbox("Show detailed breakdown"):
        for story_slug, progress in progress_data.items():
            if progress["completed"]:
                with st.expander(f"📖 {story_slug.replace('-', ' ').title()}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Best Score:** {progress['best_score']}/{progress['total']}")
                    with col2:
                        st.write(f"**Attempts:** {progress['attempts']}")
                    with col3:
                        st.write(f"**Perfect Runs:** {progress['perfect_attempts']}")
