"""
Quiz utilities for BeluTales interactive quiz system.
Handles quiz loading, answer checking, and scoring.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import streamlit as st

@st.cache_data(show_spinner=False, ttl=3600)
def load_quiz(story_id: str) -> Optional[Dict]:
    """
    Load quiz data for the given story from stories/quizzes.json.
    
    Args:
        story_id: The story identifier (e.g., "the_fox_who_forgot_how_to_sneak")
        
    Returns:
        Dictionary containing quiz data or None if not found
    """
    try:
        quizzes_file = Path("stories/quizzes.json")
        if not quizzes_file.exists():
            return None
            
        with open(quizzes_file, "r", encoding="utf-8") as f:
            quizzes = json.load(f)
            
        # Find quiz for this story
        for quiz in quizzes:
            if quiz.get("story_id") == story_id:
                return quiz
                
        return None
        
    except Exception as e:
        st.error(f"Error loading quiz: {e}")
        return None

def check_answer(question: Dict, selected: str) -> bool:
    """
    Check if the selected answer is correct for a given question.
    
    Args:
        question: Dictionary containing question data with 'answer' field
        selected: The selected answer string
        
    Returns:
        True if correct, False otherwise
    """
    try:
        correct_answer = question.get("answer", "")
        return selected == correct_answer
    except Exception:
        return False

def get_quiz_score(quiz_data: Dict, user_answers: Dict) -> Tuple[int, int]:
    """
    Calculate the user's quiz score.
    
    Args:
        quiz_data: The quiz data dictionary
        user_answers: Dictionary mapping question indices to selected answers
        
    Returns:
        Tuple of (correct_count, total_questions)
    """
    try:
        questions = quiz_data.get("questions", [])
        total_questions = len(questions)
        correct_count = 0
        
        for i, question in enumerate(questions):
            if str(i) in user_answers:
                selected = user_answers[str(i)]
                if check_answer(question, selected):
                    correct_count += 1
                    
        return correct_count, total_questions
        
    except Exception:
        return 0, 0

def get_quiz_feedback(score: int, total: int) -> Tuple[str, str]:
    """
    Get feedback message and emoji based on quiz score.
    
    Args:
        score: Number of correct answers
        total: Total number of questions
        
    Returns:
        Tuple of (message, emoji)
    """
    if total == 0:
        return "No questions available", "❓"
    
    percentage = (score / total) * 100
    
    if percentage == 100:
        return "🌟 Perfect! You know this story!", "🌟"
    elif percentage >= 80:
        return f"🎉 Excellent! You got {score}/{total} right!", "🎉"
    elif percentage >= 60:
        return f"👍 Good job! You got {score}/{total} right!", "👍"
    elif percentage >= 40:
        return f"💪 Nice try! You got {score}/{total} right!", "💪"
    else:
        return f"📚 Keep reading! You got {score}/{total} right!", "📚"

def create_quiz_session_key(story_id: str) -> str:
    """
    Create a unique session key for quiz state.
    
    Args:
        story_id: The story identifier
        
    Returns:
        Unique session key string
    """
    return f"quiz_session_{story_id}"

def get_quiz_session(story_id: str) -> Dict:
    """
    Get or create quiz session state for a story.
    
    Args:
        story_id: The story identifier
        
    Returns:
        Dictionary containing quiz session state
    """
    session_key = create_quiz_session_key(story_id)
    
    if session_key not in st.session_state:
        st.session_state[session_key] = {
            "answers": {},
            "completed": False,
            "score": 0,
            "total": 0
        }
    
    return st.session_state[session_key]

def update_quiz_session(story_id: str, question_idx: str, answer: str, is_correct: bool):
    """
    Update quiz session with a new answer.
    
    Args:
        story_id: The story identifier
        question_idx: Question index as string
        answer: Selected answer
        is_correct: Whether the answer is correct
    """
    session = get_quiz_session(story_id)
    session["answers"][question_idx] = answer
    
    # Recalculate score
    quiz_data = load_quiz(story_id)
    if quiz_data:
        score, total = get_quiz_score(quiz_data, session["answers"])
        session["score"] = score
        session["total"] = total

def reset_quiz_session(story_id: str):
    """
    Reset quiz session for a story.
    
    Args:
        story_id: The story identifier
    """
    session_key = create_quiz_session_key(story_id)
    if session_key in st.session_state:
        del st.session_state[session_key]
