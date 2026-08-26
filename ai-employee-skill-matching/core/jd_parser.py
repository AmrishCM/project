# core/jd_parser.py
# This module converts a long free-text JD into structured requirements.
# It supports "any JD size" by using keyword extraction + a skills dictionary.

import re
from core.skill_normalizer import normalize_skill_list


# A simple skill dictionary (you can expand anytime)
# Key = canonical skill, Values = possible phrases in JDs
SKILL_SYNONYMS = {
    "agile": ["agile"],
    "scrum": ["scrum"],
    "waterfall": ["waterfall"],
    "jira": ["jira"],
    "ms project": ["ms project", "microsoft project"],
    "asana": ["asana"],
    "kanban": ["kanban"],
    "excel": ["excel"],
    "stakeholder management": ["stakeholder management", "stakeholder"],
    "risk management": ["risk management", "risk"],
    "financial management": ["financial management", "budget", "cost", "financial"],
    "vendor management": ["vendor management", "vendor"],
    "communication": ["communication", "reporting"],
    "networking": ["networking", "enterprise networks", "ip data", "ip voice"],
    "cloud": ["cloud", "aws", "azure", "gcp"],
    "devops": ["devops", "ci/cd", "cicd", "docker", "kubernetes", "jenkins", "terraform"],
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "sql": ["sql"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "nlp": ["nlp", "natural language processing"],
    "testing": ["testing", "qa", "selenium", "postman"],
}

# Certifications dictionary
CERTS = ["pmp", "csm", "prince2", "itil", "cissp", "ceh"]

def _clean(text: str) -> str:
    # Lowercase + normalize spaces
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_experience_range(jd_text: str):
    """
    Extract experience range like "10–15 years" or "10-15 years"
    Returns (min_exp, max_exp) or (None, None) if not found.
    """
    t = _clean(jd_text)
    m = re.search(r"(\d+)\s*[–-]\s*(\d+)\s*years", t)
    if m:
        return int(m.group(1)), int(m.group(2))

    # Also support single value like "10 years"
    m2 = re.search(r"(\d+)\s*years", t)
    if m2:
        v = int(m2.group(1))
        return v, v

    return None, None

def extract_locations(jd_text: str):
    """
    Extract locations like "Chennai, Coimbatore"
    Very simple pattern: last section often contains Location line.
    """
    t = _clean(jd_text)
    # Try to find line containing "location"
    m = re.search(r"location\s*(.*)", t)
    if not m:
        return []

    loc_part = m.group(1)
    # Split by comma
    locs = [x.strip().title() for x in loc_part.split(",") if x.strip()]
    return locs

def extract_certs(jd_text: str):
    """
    Extract certifications mentioned in JD.
    """
    t = _clean(jd_text)
    found = []
    for c in CERTS:
        if c in t:
            found.append(c.upper() if c != "prince2" else "PRINCE2")
    # normalize some
    normalized = []
    for c in found:
        if c == "CSM":
            normalized.append("CSM")
        elif c == "PMP":
            normalized.append("PMP")
        elif c == "ITIL":
            normalized.append("ITIL")
        elif c == "PRINCE2":
            normalized.append("PRINCE2")
        elif c == "CISSP":
            normalized.append("CISSP")
        elif c == "CEH":
            normalized.append("CEH")
    return list(dict.fromkeys(normalized))  # unique preserve order

def extract_required_skills(jd_text: str):
    """
    Extract required skills from JD using SKILL_SYNONYMS.
    Output: list of canonical skills (matching your skill_matcher normalization)
    """
    t = _clean(jd_text)
    required = []

    for canonical, phrases in SKILL_SYNONYMS.items():
        for p in phrases:
            if p in t:
                required.append(canonical)
                break

    # Remove duplicates, keep order
    return list(dict.fromkeys(required))

def parse_jd(jd_text: str):
    """
    Main function: returns requirements dict.
    """
    min_exp, max_exp = extract_experience_range(jd_text)
    skills = list(normalize_skill_list(extract_required_skills(jd_text)))
    certs = extract_certs(jd_text)
    locations = extract_locations(jd_text)

    return {
        "required_skills": skills,
        "min_experience": min_exp if min_exp is not None else 0,
        "max_experience": max_exp if max_exp is not None else 100,
        "preferred_certifications": certs,
        "locations": locations
    }
