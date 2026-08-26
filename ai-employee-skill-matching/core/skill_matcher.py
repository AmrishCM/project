# core/skill_matcher.py
# Improved skill matcher using canonical normalization.

from core.skill_normalizer import normalize_skill_list

def match_skills(employee_skills, required_skills):
    """
    Compare employee skills with JD required skills
    using canonical normalization.
    """

    # Normalize employee and JD skills into canonical sets
    emp_skills = normalize_skill_list(employee_skills)
    req_skills = normalize_skill_list(required_skills)

    matched_skills = emp_skills.intersection(req_skills)
    missing_skills = req_skills.difference(emp_skills)

    if not req_skills:
        match_percentage = 0.0
    else:
        match_percentage = (len(matched_skills) / len(req_skills)) * 100.0

    gap_percentage = 100.0 - match_percentage

    severity = (
        "Low" if gap_percentage <= 20 else
        "Medium" if gap_percentage <= 50 else
        "High"
    )

    return {
        "skill_match_percent": round(match_percentage, 2),
        "skill_gap_percent": round(gap_percentage, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "gap_severity": severity
    }
