# core/certification_scorer.py

def score_certifications(employee_certs, preferred_certs):
    """
    Score certification match
    """
    if not employee_certs:
        return 0

    emp_certs = set(cert.strip().lower() for cert in employee_certs.split(","))
    pref_certs = set(cert.lower() for cert in preferred_certs)

    matched = emp_certs.intersection(pref_certs)

    if not pref_certs:
        return 0

    return (len(matched) / len(pref_certs)) * 100
