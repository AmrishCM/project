# web_app.py

import os
from datetime import datetime
from flask import Flask, request, jsonify, send_file, render_template

from services.jd_employee_evaluator import evaluate_employees_from_jd

APP_TITLE = "AI Employee Skill Matching"

EXCEL_PATH = "data/it_employees_sample.xlsx"
PROJECT_LOCATION = "Coimbatore"

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", title=APP_TITLE)


@app.route("/api/preview", methods=["POST"])
def preview():
    payload = request.get_json(force=True) or {}
    jd_text = payload.get("jd_text", "") or ""
    weights = payload.get("weights") or None

    if not jd_text.strip():
        return jsonify({"error": "JD text is required"}), 400

    df = evaluate_employees_from_jd(
        EXCEL_PATH,
        jd_text,
        project_location=PROJECT_LOCATION,
        weights_override=weights
    )

    # Return top 10 rows
    top = df.head(10).to_dict(orient="records")

    # KPIs
    resp = {
        "kpis": {
            "total_employees": int(len(df)),
            "top_score": float(df["final_match_score"].max()) if len(df) else 0,
            "avg_score": float(df["final_match_score"].mean()) if len(df) else 0,
            "soon_available_30d": int(df["soon_available_30d"].sum()) if len(df) else 0
        },
        "top10": top
    }
    return jsonify(resp)


@app.route("/api/generate_excel", methods=["POST"])
def generate_excel():
    payload = request.get_json(force=True) or {}
    jd_text = payload.get("jd_text", "") or ""
    weights = payload.get("weights") or None

    if not jd_text.strip():
        return jsonify({"error": "JD text is required"}), 400

    df = evaluate_employees_from_jd(
        EXCEL_PATH,
        jd_text,
        project_location=PROJECT_LOCATION,
        weights_override=weights
    )

    # Save report
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(REPORTS_DIR, f"jd_match_report_{ts}.xlsx")
    df.to_excel(out_path, index=False, engine="openpyxl")

    return jsonify({
        "report_path": out_path,
        "download_url": f"/download/{os.path.basename(out_path)}"
    })


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    path = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(path):
        return "File not found", 404
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
