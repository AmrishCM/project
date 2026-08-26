# core/report_helpers.py
# Helper functions to match your report format exactly.

def experience_bucket(exp_years: int) -> str:
    """
    Buckets similar to your sample:
    - 0-2, 3-5, 6-10, 11-15, 16+
    """
    if exp_years is None:
        return "Unknown"

    if exp_years <= 2:
        return "0-2"
    if exp_years <= 5:
        return "3-5"
    if exp_years <= 10:
        return "6-10"
    if exp_years <= 15:
        return "11-15"
    return "16+"

def final_match_band(score: float) -> str:
    """
    Bands like:
    - Excellent (80-100)
    - Good (60-79)
    - Average (40-59)
    - Poor (<40)
    """
    if score >= 80:
        return "Excellent (80-100)"
    if score >= 60:
        return "Good (60-79)"
    if score >= 40:
        return "Average (40-59)"
    return "Poor (<40)"
