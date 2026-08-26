# services/employee_evaluator.py

import pandas as pd

from config.role_requirements import ROLE_REQUIREMENTS
from core.skill_matcher import match_skills
from core.experience_scorer import score_experience
from core.certification_scorer import score_certifications
from core.availability_checker import score_availability
from core.final_scorer import calculate_final_score
from training.training_recommender import recommend_training


def evaluate_employees(excel_path, target_role, project_location):
    """
    Evaluate bench employees against a target JD role
    """

    df = pd.read_excel(excel_path)

    role_req = ROLE_REQUIREMENTS.get(target_role)
    if not role_req:
        raise ValueError(f"No role requirements defined for {target_role}")

    results = []

    for _, row in df.iterrows():
        if row["role"] != target_role:
            continue

        # ---- Skill Matching ----
        skill_result = match_skills(
            row["skills"],
            role_req["required_skills"]
        )

        # ---- Experience ----
        experience_score = score_experience(
            row["experience_years"],
            role_req["min_experience"]
        )

        # ---- Certifications ----
        certification_score = score_certifications(
            str(row.get("certifications", "")),
            role_req["preferred_certifications"]
        )

        # ---- Relocation ----
        relocation_score = (
            100 if row["ready_to_relocate"] or
            row["current_location"] == project_location else 0
        )

        # ---- Availability ----
        availability_score = score_availability(row["available_from"])

        # ---- Training Recommendation ----
        training_plan = recommend_training(
            skill_result["missing_skills"],
            len(role_req["required_skills"])
        )

        # ---- Final AI Score ----
        final_score = calculate_final_score({
            "skills": skill_result["skill_match_percent"],
            "experience": experience_score,
            "certifications": certification_score,
            "relocation": relocation_score,
            "availability": availability_score
        })

        results.append({
            "emp_id": row["emp_id"],
            "name": row["name"],
            "role": row["role"],
            "final_match_score": final_score,
            "skill_match_percent": skill_result["skill_match_percent"],
            "experience_score": experience_score,
            "certification_score": round(certification_score, 2),
            "relocation_score": relocation_score,
            "availability_score": availability_score,
            "skill_gap_severity": training_plan["skill_gap_severity_level"],
            "skill_gap_severity_percent": training_plan["skill_gap_severity_percent"],
            "missing_skills": ", ".join(skill_result["missing_skills"]),
            "training_recommendations": "; ".join(training_plan["training_recommendations"])
        })

    return pd.DataFrame(results)
