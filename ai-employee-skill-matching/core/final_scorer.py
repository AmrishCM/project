# core/final_scorer.py

from config.weights import WEIGHTS

def calculate_final_score(scores):
    """
    Combine all dimension scores using weighted average
    """
    final_score = (
        scores["skills"] * WEIGHTS["skills"] +
        scores["experience"] * WEIGHTS["experience"] +
        scores["certifications"] * WEIGHTS["certifications"] +
        scores["relocation"] * WEIGHTS["relocation"] +
        scores["availability"] * WEIGHTS["availability"]
    )

    return round(final_score, 2)
