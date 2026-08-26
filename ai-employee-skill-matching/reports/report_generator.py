# reports/report_generator.py

import os

def generate_excel_report(df, output_path):
    """
    Generate final Excel report (sorted) into output_path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df_sorted = df.sort_values(by="final_match_score", ascending=False)

    # Write to Excel
    df_sorted.to_excel(output_path, index=False, engine="openpyxl")
