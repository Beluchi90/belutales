"""
Quiz component for BeluTales stories.
Handles quiz display and interaction with magical kid-friendly styling.
Uses layered fallback approach to ensure every story has 3 quiz questions.
"""

import streamlit as st
from .quiz_data import QUIZZES, DEFAULT_QUIZ


def render_quiz_section(story: dict, selected_language: str = "English"):
    """
    Render the quiz section with kid-friendly styling in a collapsible expander.
    Uses layered fallback approach: story.quiz -> QUIZZES[title] -> DEFAULT_QUIZ
    
    Args:
        story: The story dictionary containing title and optional quiz field
        selected_language: The selected language for the quiz
    """
    # Initialize quiz session state
    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {}

    if "stars" not in st.session_state:
        st.session_state.stars = 0
    
    story_title = story.get("title", "")
    
    # Layered fallback approach to get exactly 3 quiz questions
    quiz_questions = []
    
    # Layer 1: Check if story object contains a quiz field
    if story.get("quiz") and len(story["quiz"]) >= 3:
        quiz_questions = story["quiz"][:3]  # Take first 3 questions
    # Layer 2: Check if story title exists in QUIZZES
    elif story_title in QUIZZES and len(QUIZZES[story_title]) >= 3:
        quiz_questions = QUIZZES[story_title][:3]  # Take first 3 questions
    # Layer 3: Fall back to DEFAULT_QUIZ (always has exactly 3 questions)
    else:
        quiz_questions = DEFAULT_QUIZ
    
    # Wrap quiz in collapsible expander
    with st.expander("✨ Quiz Time!", expanded=False):
        # Add quiz styling CSS
        quiz_css = """
        <style>
        /* Quiz container styling - magical and kid-friendly */
        .quiz-container {
            background: linear-gradient(135deg, 
                rgba(255, 182, 193, 0.15), 
                rgba(255, 218, 185, 0.15), 
                rgba(221, 160, 221, 0.15), 
                rgba(173, 216, 230, 0.15)) !important;
            border: 3px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 25px !important;
            padding: 2rem !important;
            margin: 1.5rem 0 !important;
            backdrop-filter: blur(15px) !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2), 
                        0 6px 20px rgba(255, 182, 193, 0.3),
                        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
            position: relative !important;
            overflow: hidden !important;
            animation: gentleGlow 3s ease-in-out infinite alternate !important;
        }
        
        /* Magical glow animation */
        @keyframes gentleGlow {
            0% { box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2), 
                             0 6px 20px rgba(255, 182, 193, 0.3),
                             inset 0 1px 0 rgba(255, 255, 255, 0.3); }
            100% { box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2), 
                               0 6px 20px rgba(255, 182, 193, 0.5),
                               inset 0 1px 0 rgba(255, 255, 255, 0.5); }
        }
        
        /* Quiz title styling - magical and playful */
        .quiz-title {
            text-align: center !important;
            font-family: "Baloo 2", "Comic Neue", sans-serif !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #ff6ec4 !important;
            text-shadow: 0 4px 8px rgba(255, 110, 196, 0.4), 
                         0 2px 4px rgba(0, 0, 0, 0.2) !important;
            margin-bottom: 1.5rem !important;
            letter-spacing: 1px !important;
            animation: magicalBounce 2s ease-in-out infinite !important;
        }
        
        /* Magical bounce animation for title */
        @keyframes magicalBounce {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-3px) scale(1.02); }
        }
        
        /* Question styling */
        .quiz-question {
            font-family: "Baloo 2", "Comic Neue", sans-serif !important;
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            color: #2c3e50 !important;
            margin-bottom: 1rem !important;
            padding: 1rem !important;
            background: rgba(255, 255, 255, 0.7) !important;
            border-radius: 15px !important;
            border-left: 5px solid #ff6ec4 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* Answer button styling */
        .quiz-answer-btn {
            background: linear-gradient(135deg, #ff9a9e, #fecfef) !important;
            border: 2px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 20px !important;
            padding: 0.8rem 1.5rem !important;
            margin: 0.5rem 0 !important;
            font-family: "Baloo 2", "Comic Neue", sans-serif !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #2c3e50 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            position: relative !important;
            overflow: hidden !important;
            box-shadow: 0 4px 15px rgba(255, 154, 158, 0.3) !important;
        }
        
        .quiz-answer-btn:hover {
            transform: translateY(-2px) scale(1.02) !important;
            background: linear-gradient(135deg, #ff8a8e, #febfef) !important;
            box-shadow: 0 6px 20px rgba(255, 154, 158, 0.5) !important;
        }
        
        .quiz-answer-btn::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: -100% !important;
            width: 100% !important;
            height: 100% !important;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent) !important;
            transition: left 0.5s ease !important;
        }
        
        .quiz-answer-btn:hover::before {
            left: 100% !important;
        }
        
        /* Check answers button styling */
        .quiz-check-btn {
            background: linear-gradient(135deg, #a8e6cf, #88d8c0) !important;
            border: 2px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 25px !important;
            padding: 1rem 2rem !important;
            margin: 1.5rem auto !important;
            font-family: "Baloo 2", "Comic Neue", sans-serif !important;
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            color: #2c3e50 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            display: block !important;
            box-shadow: 0 6px 20px rgba(168, 230, 207, 0.4) !important;
        }
        
        .quiz-check-btn:hover {
            transform: translateY(-3px) scale(1.05) !important;
            background: linear-gradient(135deg, #b8f6df, #98e8d0) !important;
            box-shadow: 0 8px 25px rgba(168, 230, 207, 0.6) !important;
        }
        
        /* Results styling */
        .quiz-results {
            text-align: center !important;
            padding: 1.5rem !important;
            margin-top: 1rem !important;
            background: rgba(255, 255, 255, 0.9) !important;
            border-radius: 20px !important;
            border: 3px solid #ff6ec4 !important;
        }
        
        .quiz-score {
            font-family: "Baloo 2", "Comic Neue", sans-serif !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            color: #ff6ec4 !important;
            margin-bottom: 1rem !important;
        }
        
        .quiz-stars {
            font-size: 2rem !important;
            margin: 0.5rem !important;
            animation: magicalBounce 1s ease-in-out infinite !important;
        }
        
        /* Accessibility improvements */
        @media (prefers-reduced-motion: reduce) {
            .quiz-title, .quiz-stars {
                animation: none !important;
            }
            .quiz-answer-btn:hover {
                transform: none !important;
            }
        }
        </style>
        """
        
        st.markdown(quiz_css, unsafe_allow_html=True)
        
        # Quiz container
        st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
        
        # Quiz title
        st.markdown('<h2 class="quiz-title">✨ Quiz Time! ✨</h2>', unsafe_allow_html=True)
        
        # Display exactly 3 questions (quiz_questions is guaranteed to have 3 questions)
        questions_to_show = quiz_questions[:3]  # Take first 3 questions
        
        # Initialize answers for this story
        story_key = f"quiz_answers_{story_title.replace(' ', '_').lower()}"
        if story_key not in st.session_state:
            st.session_state[story_key] = {}
        
        # Display questions
        for i, question_data in enumerate(questions_to_show):
            question_text = question_data["question"]
            options = question_data["options"]
            correct_answer = question_data["answer"]
            
            st.markdown(f'<div class="quiz-question">Question {i+1}: {question_text}</div>', unsafe_allow_html=True)
            
            # Radio button for answers
            selected_answer = st.radio(
                f"Choose your answer:",
                options,
                key=f"quiz_q{i}_{story_title.replace(' ', '_').lower()}",
                index=None
            )
            
            # Store the answer
            if selected_answer is not None:
                st.session_state[story_key][f"q{i}"] = {
                    "selected": selected_answer,
                    "correct": correct_answer
                }
        
        # Check answers button
        if st.button("🎯 Check My Answers!", key=f"check_quiz_{story_title.replace(' ', '_').lower()}", use_container_width=True):
            # Calculate score
            score = 0
            total_questions = len(questions_to_show)
            
            for i in range(total_questions):
                if f"q{i}" in st.session_state[story_key]:
                    user_answer = st.session_state[story_key][f"q{i}"]["selected"]
                    correct_answer = st.session_state[story_key][f"q{i}"]["correct"]
                    if user_answer == correct_answer:
                        score += 1

            # Store score
            st.session_state.quiz_scores[story_title] = score
            
            # Display results
            st.markdown('<div class="quiz-results">', unsafe_allow_html=True)
            st.markdown(f'<div class="quiz-score">You got {score} out of {total_questions} correct! 🎉</div>', unsafe_allow_html=True)
            
            # Display stars based on score
            stars = "⭐" * score
            if score == total_questions:
                stars += " 🌟 Perfect! 🌟"
            elif score >= total_questions * 0.7:
                stars += " 🌟 Great job! 🌟"
            elif score >= total_questions * 0.5:
                stars += " 🌟 Good try! 🌟"
            else:
                stars += " 🌟 Keep practicing! 🌟"
            
            st.markdown(f'<div class="quiz-stars">{stars}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)