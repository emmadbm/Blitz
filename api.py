import os
import pandas as pd
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

main = Blueprint("main", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")


@main.route("/")
def home():
    return jsonify({
        "message": "Welcome to Blitz API 🚀"
    })


@main.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "service": "Blitz API"
    })


@main.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected."
        }), 400

    filename = secure_filename(file.filename)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        # Read the uploaded file
        if filename.endswith(".csv"):
            df = pd.read_csv(filepath)

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(filepath)

        else:
            return jsonify({
                "success": False,
                "message": "Unsupported file format. Please upload a CSV or Excel file."
            }), 400

        
        dataset_info = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "preview": df.head().to_dict(orient="records")
        }

        
        validation = {
            "data_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum())
        }
        total_missing = int(df.isnull().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        health_score = 100

        health_score -= min(total_missing * 2, 30)
        health_score -= min(duplicate_rows * 5, 20  )

        health_score = max(0, health_score)
        if health_score >= 90:
           status = "Excellent"

        elif health_score >= 75:
           status = "Good"

        elif health_score >= 50:
           status = "Fair"

        else:
          status = "Poor"
        health_report = {
    "status": status,
    "health_score": health_score,
    "total_missing_values": total_missing,
    "duplicate_rows": duplicate_rows
}
        return jsonify({
            "success": True,
            "filename": filename,
            "dataset_info": dataset_info,
            "validation": validation,
            "health_report": health_report
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error processing the file: {str(e)}"
        }), 500