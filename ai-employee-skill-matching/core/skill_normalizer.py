# core/skill_normalizer.py
# Central skill normalization logic used by BOTH JD and employee skills.

SKILL_SYNONYMS = {
    "agile": ["agile", "agility"],
    "scrum": ["scrum", "scrum master"],
    "waterfall": ["waterfall"],
    "jira": ["jira", "jira tool"],
    "ms project": ["ms project", "microsoft project"],
    "asana": ["asana"],
    "kanban": ["kanban"],
    "excel": ["excel", "ms excel"],

    "stakeholder management": [
        "stakeholder management",
        "stakeholder communication",
        "stakeholder coordination"
    ],

    "risk management": [
        "risk management",
        "risk analysis",
        "risk mitigation"
    ],

    "financial management": [
        "financial management",
        "finance management",
        "budget management",
        "cost management"
    ],

    "vendor management": [
        "vendor management",
        "supplier management",
        "third party management"
    ],

    "communication": [
        "communication",
        "reporting",
        "presentation"
    ],

    "networking": [
        "networking",
        "enterprise networks",
        "ip data",
        "ip voice"
    ],

    "cloud": [
        "cloud",
        "aws",
        "azure",
        "gcp"
    ],

    "devops": [
        "devops",
        "ci/cd",
        "cicd",
        "docker",
        "kubernetes",
        "jenkins",
        "terraform"
    ],

    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "sql": ["sql"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "nlp": ["nlp", "natural language processing"],
    "testing": ["testing", "qa", "selenium", "postman"]
}

def normalize_skill(raw_skill: str):
    """
    Convert a raw skill phrase into its canonical form.
    Returns canonical skill or None if unknown.
    """
    if not raw_skill:
        return None

    s = raw_skill.lower().strip()

    for canonical, variants in SKILL_SYNONYMS.items():
        for v in variants:
            if v in s:
                return canonical

    return None


def normalize_skill_list(raw_skills):
    """
    Normalize a list OR comma-separated string of skills
    into a set of canonical skill names.
    """
    normalized = set()

    if isinstance(raw_skills, str):
        raw_list = raw_skills.split(",")
    else:
        raw_list = raw_skills

    for skill in raw_list:
        canonical = normalize_skill(skill)
        if canonical:
            normalized.add(canonical)

    return normalized
