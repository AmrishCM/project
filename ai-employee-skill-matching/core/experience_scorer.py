# core/experience_scorer.py

def score_experience(employee_exp, min_required_exp):
    """
    Score experience strictly based on JD requirement
    """
    if employee_exp >= min_required_exp:
        return 100
    elif employee_exp >= min_required_exp * 0.7:
        return 60
    else:
        return 20
