# training/training_recommender.py

TRAINING_CATALOG = {
    "agile": "Agile Project Management (2 weeks)",
    "scrum": "Scrum Master Certification Training (2 weeks)",
    "jira": "JIRA & Agile Tools Workshop (1 week)",
    "ms project": "Microsoft Project Advanced Planning (1 week)",
    "stakeholder management": "Stakeholder Communication & Governance (1 week)",
    "risk management": "Project Risk & Compliance Management (1 week)",
    "financial management": "Project Financial Control & Cost Optimization (1 week)",

    "aws": "AWS Solutions Architect Training (4 weeks)",
    "azure": "Microsoft Azure Architect Training (4 weeks)",
    "gcp": "Google Cloud Architect Training (4 weeks)",
    "cloudformation": "Infrastructure as Code with CloudFormation (2 weeks)",

    "machine learning": "Applied Machine Learning with Python (4 weeks)",
    "pandas": "Data Analysis with Pandas (1 week)",
    "tensorflow": "Deep Learning with TensorFlow (3 weeks)",

    "network security": "Enterprise Network Security Training (3 weeks)",
    "siem": "SIEM & SOC Operations (2 weeks)",
    "penetration testing": "Ethical Hacking & Pentesting (4 weeks)",
    "encryption": "Cryptography & Secure Systems (2 weeks)"
}


def recommend_training(missing_skills, total_required_skills):
    """
    Generate training plan and severity score
    """
    recommendations = []

    for skill in missing_skills:
        skill_key = skill.lower()
        training = TRAINING_CATALOG.get(
            skill_key,
            f"Self-paced training for {skill}"
        )
        recommendations.append(training)

    severity_percent = (len(missing_skills) / total_required_skills) * 100

    if severity_percent <= 20:
        severity_level = "Low"
    elif severity_percent <= 50:
        severity_level = "Medium"
    else:
        severity_level = "High"

    return {
        "training_recommendations": recommendations,
        "skill_gap_severity_percent": round(severity_percent, 2),
        "skill_gap_severity_level": severity_level
    }
