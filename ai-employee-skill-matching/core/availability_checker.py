# core/availability_checker.py
# Computes availability score AND useful availability fields for the report.

from datetime import datetime
import pandas as pd

def availability_details(available_from):
    """
    Returns:
    - available_from_dt: datetime
    - days_to_available: int
    - soon_available_30d: bool
    - availability_score: int
    """

    # Convert whatever is in Excel into a proper datetime
    # This supports: datetime, "YYYY-MM-DD", Excel timestamp strings, etc.
    available_dt = pd.to_datetime(available_from, errors="coerce")

    # If date is missing/invalid, treat as far future (worst availability)
    if pd.isna(available_dt):
        days_to_available = 9999
    else:
        today = pd.Timestamp(datetime.today().date())
        days_to_available = int((available_dt.normalize() - today).days)

        # If already available (negative), clamp to 0
        if days_to_available < 0:
            days_to_available = 0

    # 30-day availability flag
    soon_30d = days_to_available <= 30

    # Availability score logic (same spirit as your old function)
    if days_to_available <= 30:
        score = 100
    elif days_to_available <= 90:
        score = 60
    else:
        score = 30

    return available_dt, days_to_available, soon_30d, score


def score_availability(available_from):
    """
    Backward compatible function (if other code calls it).
    """
    _, _, _, score = availability_details(available_from)
    return score
