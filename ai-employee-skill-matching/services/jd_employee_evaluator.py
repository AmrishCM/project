# services/jd_employee_evaluator.py
# JD-based evaluator that outputs the exact columns you requested.

import pandas as pd

from core.jd_parser import parse_jd
from core.skill_matcher import match_skills
from core.experience_scorer import score_experience
from core.certification_scorer import score_certifications
from core.availability_checker import availability_details
from core.final_scorer import calculate_final_score
from core.report_helpers import experience_bucket, final_match_band
from training.training_recommender import recommend_training


def evaluate_employees_from_jd(excel_path: str, jd_text: str):
    """
    Evaluate employees against free-text JD and return a DataFrame with
    the exact output schema (columns) you showed.
    """
    df = pd.read_excel(excel_path)

    # Parse JD into structured requirements
    jd_req = parse_jd(jd_text)

    results = []

    for _, row in df.iterrows():
        # Read raw employee fields safely
        emp_id = row.get("emp_id")
        name = row.get("name")
        role = row.get("role")
        current_location = str(row.get("current_location", "")).strip().title()
        exp_years = int(row.get("experience_years", 0) or 0)
        skills_raw = str(row.get("skills", "") or "")
        certs_raw = str(row.get("certifications", "") or "")

        # ------------------ Skill Matching ------------------
        # employee skills in Excel are comma-separated in your current code
        skill_result = match_skills(skills_raw, jd_req["required_skills"])
        skill_match_percent = skill_result["skill_match_percent"]
        missing_skills_list = skill_result["missing_skills"]
        missing_skills_str = ", ".join(missing_skills_list)
        missing_skills_count = len(missing_skills_list)

        # ------------------ Experience ------------------
        exp_score = score_experience(exp_years, jd_req["min_experience"])
        exp_bucket = experience_bucket(exp_years)

        # ------------------ Certifications ------------------
        cert_score = score_certifications(certs_raw, jd_req["preferred_certifications"])

        # ------------------ Relocation / Location ------------------
        # If JD contains locations, then:
        # - Score 100 if employee in allowed locations or ready_to_relocate = True
        # - Else 0
        ready_to_relocate = bool(row.get("ready_to_relocate", False))
        jd_locs = jd_req["locations"]

        if jd_locs:
            relocation_score = 100 if (ready_to_relocate or current_location in jd_locs) else 0
        else:
            # If JD doesn't specify location, don't penalize
            relocation_score = 100

        # ------------------ Availability ------------------
        available_from_raw = row.get("available_from")
        available_dt, days_to_available, soon_30d, availability_score = availability_details(available_from_raw)

        # ------------------ Training Plan ------------------
        training_plan = recommend_training(
            missing_skills_list,
            max(len(jd_req["required_skills"]), 1)
        )

        training_recos = training_plan["training_recommendations"]
        training_recos_str = "; ".join(training_recos)
        training_recos_count = len(training_recos)

        # ------------------ Final Score ------------------
        final_score = calculate_final_score({
            "skills": skill_match_percent,
            "experience": exp_score,
            "certifications": cert_score,
            "relocation": relocation_score,
            "availability": availability_score
        })

        band = final_match_band(final_score)

        # ------------------ Build EXACT output row ------------------
        results.append({
            "emp_id": emp_id,
            "name": name,
            "role": role,
            "current_location": current_location,
            "experience_years": exp_years,
            "experience_bucket": exp_bucket,
            "available_from": available_dt,                 # stored as datetime
            "days_to_available": days_to_available,
            "soon_available_30d": bool(soon_30d),
            "final_match_score": float(final_score),
            "final_match_band": band,
            "skill_match_percent": float(skill_match_percent),
            "experience_score": float(exp_score),
            "certification_score": round(float(cert_score), 2),
            "relocation_score": float(relocation_score),
            "availability_score": float(availability_score),
            "skill_gap_severity": training_plan["skill_gap_severity_level"],
            "skill_gap_severity_percent": float(training_plan["skill_gap_severity_percent"]),
            "missing_skills": missing_skills_str,
            "missing_skills_count": int(missing_skills_count),
            "training_recommendations": training_recos_str,
            "training_recos_count": int(training_recos_count),
            "skills": skills_raw,
            "certifications": certs_raw
        })

    out_df = pd.DataFrame(results)

    # Sort best to worst
    if not out_df.empty:
        out_df = out_df.sort_values(by="final_match_score", ascending=False)

    return out_df
