"""
REST API routes for the Secret Santa application.
"""
import os
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, Response, current_app

from src.parsers import EmployeeParser, AssignmentParser
from src.services import SecretSantaService, ExportService, AssignmentError
from src.validators import AssignmentInputValidator

api_bp = Blueprint("api", __name__, url_prefix="/api")

employee_parser = EmployeeParser()
assignment_parser = AssignmentParser()
santa_service = SecretSantaService()
export_service = ExportService()
validator = AssignmentInputValidator()


# ─────────────────────────────────────────
# Health check
# ─────────────────────────────────────────
@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})


# ─────────────────────────────────────────
# Generate assignments (upload CSV / XLSX)
# ─────────────────────────────────────────
@api_bp.route("/assignments/generate", methods=["POST"])
def generate_assignments():
    """
    Expects multipart/form-data with:
      - employees_file: CSV or XLSX with columns Employee_Name, Employee_EmailID
      - previous_file (optional): CSV with previous year's assignments
      - year (optional): integer year label (defaults to current year)
      - format (optional): "json" | "csv" | "xml"  (default: "json")
    """
    if "employees_file" not in request.files:
        return jsonify({"error": "employees_file is required"}), 400

    emp_file = request.files["employees_file"]
    year = int(request.form.get("year", datetime.now(timezone.utc).year))
    fmt = request.form.get("format", "json").lower()

    # ── Save temp file ──────────────────────────────
    tmp_path = f"/tmp/employees_{year}{os.path.splitext(emp_file.filename)[1]}"
    emp_file.save(tmp_path)

    try:
        employees = employee_parser.parse_file(tmp_path)
    except (FileNotFoundError, ValueError) as e:
        return jsonify({"error": str(e)}), 422

    # ── Optional previous assignments ───────────────
    previous_assignments = None
    if "previous_file" in request.files:
        prev_file = request.files["previous_file"]
        prev_path = f"/tmp/previous_{year}.csv"
        prev_file.save(prev_path)
        try:
            previous_assignments = assignment_parser.parse_file(prev_path)
        except (FileNotFoundError, ValueError) as e:
            return jsonify({"error": f"Previous file error: {e}"}), 422

    # ── Validate ────────────────────────────────────
    errors = validator.validate(employees, previous_assignments)
    if errors:
        return jsonify({"errors": errors}), 422

    # ── Generate ────────────────────────────────────
    try:
        assignments = santa_service.generate(employees, previous_assignments)
    except AssignmentError as e:
        return jsonify({"error": str(e)}), 500

    # ── Persist to MongoDB if available ─────────────
    mongo = current_app.config.get("MONGO_SERVICE")
    doc_id = None
    if mongo:
        try:
            doc_id = mongo.save_assignments(assignments, year)
        except Exception:
            pass  # DB unavailable — still return results

    # ── Respond in requested format ─────────────────
    if fmt == "csv":
        csv_str = export_service.to_csv(assignments)
        return Response(csv_str, mimetype="text/csv",
                        headers={"Content-Disposition": f"attachment; filename=secret_santa_{year}.csv"})

    if fmt == "xml":
        xml_str = export_service.to_xml(assignments)
        return Response(xml_str, mimetype="application/xml")

    return jsonify({
        "year": year,
        "total": len(assignments),
        "mongo_id": doc_id,
        "assignments": [a.to_dict() for a in assignments],
    })


# ─────────────────────────────────────────
# Retrieve saved assignments by year
# ─────────────────────────────────────────
@api_bp.route("/assignments/<int:year>", methods=["GET"])
def get_assignments(year: int):
    mongo = current_app.config.get("MONGO_SERVICE")
    if not mongo:
        return jsonify({"error": "MongoDB not configured"}), 503

    assignments = mongo.get_assignments_by_year(year)
    if assignments is None:
        return jsonify({"error": f"No assignments found for year {year}"}), 404

    fmt = request.args.get("format", "json").lower()
    if fmt == "csv":
        return Response(export_service.to_csv(assignments), mimetype="text/csv")
    if fmt == "xml":
        return Response(export_service.to_xml(assignments), mimetype="application/xml")

    return jsonify({
        "year": year,
        "total": len(assignments),
        "assignments": [a.to_dict() for a in assignments],
    })


# ─────────────────────────────────────────
# List all years that have assignments
# ─────────────────────────────────────────
@api_bp.route("/assignments/years", methods=["GET"])
def list_years():
    mongo = current_app.config.get("MONGO_SERVICE")
    if not mongo:
        return jsonify({"error": "MongoDB not configured"}), 503
    return jsonify({"years": mongo.list_years()})


# ─────────────────────────────────────────
# Error handlers
# ─────────────────────────────────────────
@api_bp.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@api_bp.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405
