"""
Interactive quiz component for BeluTales stories.
Features colorful buttons, instant feedback, and kid-friendly design.
"""

import streamlit as st
from utils.quiz_utils import (
    load_quiz, check_answer, get_quiz_score, get_quiz_feedback,
    get_quiz_session, update_quiz_session, reset_quiz_session
)
import hashlib

def render_interactive_quiz(story: dict, selected_language: str = "English"):
    """
    Render an interactive quiz with colorful buttons and instant feedback.
    
    Args:
        story: The story dictionary containing title and other story data
        selected_language: The selected language for the quiz
    """
    # Generate story ID from title
    story_title = story.get("title", "")
    story_id = hashlib.md5(story_title.encode()).hexdigest()[:8]
    
    # Load quiz data
    quiz_data = load_quiz(story_id)
    
    if not quiz_data:
        # Fallback to default quiz if no specific quiz found
        quiz_data = {
            "story_id": story_id,
            "questions": [
                {
                    "q": "Did you enjoy this story?",
                    "options": ["Yes, I loved it! ✨", "It was okay", "Not really"],
                    "answer": "Yes, I loved it! ✨"
                },
                {
                    "q": "Which character did you like most?",
                    "options": ["The main character", "A friend", "A magical creature"],
                    "answer": "The main character"
                },
                {
                    "q": "What do you think happens next?",
                    "options": ["They live happily ever after", "They go on another adventure", "They learn something new"],
                    "answer": "They live happily ever after"
                }
            ]
        }
    
    # Get quiz session
    session = get_quiz_session(story_id)
    
    # Quiz styling
    quiz_css = """
    <style>
    .quiz-container {
        background: linear-gradient(135deg, 
            rgba(255, 182, 193, 0.15), 
            rgba(173, 216, 230, 0.15),
            rgba(255, 218, 185, 0.15));
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        border: 2px solid rgba(255, 182, 193, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .quiz-title {
        font-family: "Fredoka One", "Baloo 2", cursive;
        font-size: 2em;
        color: #2E2A65;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .question-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 2px solid rgba(255, 182, 193, 0.2);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    .question-text {
        font-family: "Baloo 2", cursive;
        font-size: 1.3em;
        color: #2E2A65;
        font-weight: 600;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .quiz-button {
        background: linear-gradient(135deg, #FFB6C1, #87CEEB);
        border: none;
        border-radius: 25px;
        padding: 12px 24px;
        margin: 8px;
        font-family: "Baloo 2", cursive;
        font-size: 1.1em;
        font-weight: 600;
        color: #2E2A65;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        min-width: 200px;
    }
    
    .quiz-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }
    
    .quiz-button.correct {
        background: linear-gradient(135deg, #90EE90, #32CD32);
        color: white;
        animation: correctPulse 0.6s ease;
    }
    
    .quiz-button.incorrect {
        background: linear-gradient(135deg, #FFB6C1, #FF69B4);
        color: white;
        animation: incorrectShake 0.6s ease;
    }
    
    @keyframes correctPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes incorrectShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .feedback-message {
        font-family: "Baloo 2", cursive;
        font-size: 1.2em;
        font-weight: 600;
        text-align: center;
        margin: 10px 0;
        padding: 10px;
        border-radius: 10px;
    }
    
    .feedback-correct {
        color: #228B22;
        background: rgba(144, 238, 144, 0.2);
    }
    
    .feedback-incorrect {
        color: #DC143C;
        background: rgba(255, 182, 193, 0.2);
    }
    
    .score-display {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 4px 16px rgba(255, 215, 0, 0.3);
    }
    
    .score-text {
        font-family: "Fredoka One", cursive;
        font-size: 1.5em;
        color: #2E2A65;
        margin: 0;
    }
    </style>
    """
    
    # Wrap quiz in collapsible expander
    with st.expander("🎯 Interactive Quiz Time!", expanded=False):
        st.markdown(quiz_css, unsafe_allow_html=True)
        
        # Quiz container
        st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="quiz-title">🎯 Interactive Quiz Time! 🎯</h2>', unsafe_allow_html=True)
        
        questions = quiz_data.get("questions", [])
        
        if not questions:
            st.info("No quiz questions available for this story yet! ✨")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # Display each question
        for i, question in enumerate(questions):
            question_text = question.get("q", "")
            options = question.get("options", [])
            correct_answer = question.get("answer", "")
            
            # Question card
            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="question-text">Question {i+1}: {question_text}</div>', unsafe_allow_html=True)
            
            # Check if this question has been answered
            question_key = str(i)
            user_answer = session["answers"].get(question_key)
            is_correct = user_answer == correct_answer if user_answer else None
            
            # Display options as buttons
            cols = st.columns(len(options))
            for j, option in enumerate(options):
                with cols[j]:
                    button_key = f"quiz_q{i}_opt{j}_{story_id}"
                    
                    # Determine button style
                    button_class = "quiz-button"
                    if user_answer == option:
                        if is_correct:
                            button_class += " correct"
                        else:
                            button_class += " incorrect"
                    
                    # Create button
                    if st.button(option, key=button_key, use_container_width=True):
                        # Update session with answer
                        update_quiz_session(story_id, question_key, option, option == correct_answer)
                        st.rerun()
            
            # Show feedback if answered
            if user_answer:
                if is_correct:
                    st.markdown('<div class="feedback-message feedback-correct">✅ Correct! Great job! 🎉</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="feedback-message feedback-incorrect">❌ Oops, try again! 💪</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show final score
        if session["answers"]:
            score, total = session["score"], session["total"]
            message, emoji = get_quiz_feedback(score, total)
            
            st.markdown('<div class="score-display">', unsafe_allow_html=True)
            st.markdown(f'<div class="score-text">{emoji} {message}</div>', unsafe_allow_html=True)
            st.markdown(f'<p>Score: {score}/{total}</p>', unsafe_allow_html=True)
            
            # Reset button
            if st.button("🔄 Try Again", key=f"reset_quiz_{story_id}"):
                reset_quiz_session(story_id)
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
