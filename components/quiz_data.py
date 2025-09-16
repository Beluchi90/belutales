"""
Quiz questions data for BeluTales stories.
Add new stories and their quiz questions here.
"""

# Manually defined quiz questions for specific stories
QUIZZES = {
    "Nina and the Night Sky": [
        {
            "question": "Who is the main character in this story?",
            "options": ["Nina", "A Fox", "The Stars"],
            "answer": "Nina"
        },
        {
            "question": "What disappeared from the sky?",
            "options": ["The Sun", "The Moon", "The Stars"],
            "answer": "The Stars"
        },
        {
            "question": "What did Nina use to shine light into the sky?",
            "options": ["Lantern", "Torch", "Candle"],
            "answer": "Torch"
        }
    ],

    "The Boy and the Book That Could Fly": [
        {
            "question": "What could the book do?",
            "options": ["Talk", "Fly", "Glow"],
            "answer": "Fly"
        },
        {
            "question": "Who found the book?",
            "options": ["A girl", "The Boy", "The Teacher"],
            "answer": "The Boy"
        },
        {
            "question": "Where did the story take place?",
            "options": ["Library", "Forest", "Classroom"],
            "answer": "Library"
        }
    ],
}

# Default magical placeholder questions for stories without specific quizzes
DEFAULT_QUIZ = [
    {
        "question": "Did you enjoy this story?",
        "options": ["Yes, I loved it! ✨", "It was okay", "Not really"],
        "answer": "Yes, I loved it! ✨"
    },
    {
        "question": "Which character did you like most?",
        "options": ["The main character", "A friend", "A magical creature"],
        "answer": "The main character"
    },
    {
        "question": "What do you think happens next?",
        "options": ["They live happily ever after", "They go on another adventure", "They learn something new"],
        "answer": "They live happily ever after"
    }
]
