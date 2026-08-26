# main.py

from services.employee_evaluator import evaluate_employees
from reports.report_generator import generate_excel_report

# ------------------ CONFIG ------------------

EXCEL_PATH = "data/it_employees_sample.xlsx"
OUTPUT_REPORT = "data/processed_employee_scores.xlsx"

TARGET_ROLE = "Project Manager"
PROJECT_LOCATION = "Coimbatore"

# ------------------ RUN PIPELINE ------------------

def main():
    print("🔍 Evaluating bench employees for role:", TARGET_ROLE)

    evaluated_df = evaluate_employees(
        excel_path=EXCEL_PATH,
        target_role=TARGET_ROLE,
        project_location=PROJECT_LOCATION
    )

    if evaluated_df.empty:
        print("⚠️ No matching employees found for the role.")
        return

    generate_excel_report(
        evaluated_df,
        OUTPUT_REPORT
    )

    print("✅ Evaluation complete!")
    print("📊 Report generated at:", OUTPUT_REPORT)


if __name__ == "__main__":
    main()
