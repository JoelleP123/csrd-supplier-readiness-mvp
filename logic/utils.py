"""Helper utilities"""

from intake.intake_questions import QUESTION_TO_KEY

def normalize_answers(answers_by_question: dict) -> dict:
    """Convert question text to internal keys"""
    a = {}
    for q, ans in answers_by_question.items():
        key = QUESTION_TO_KEY.get(q)
        if key:
            a[key] = ans
    return a
