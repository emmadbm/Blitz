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
        if filename.endswith(".csv"):
            df= pd.read_csv(filepath)
        elif filename.endswith(".xlsx",".xsl"):
            df= pd.read_excel(filepath)
        else:
            return jsonify({
                "success": False,
                "message": "Unsupported file format. Please upload a CSV or Excel file."
            }), 400
        return jsonify({
            "success": True,
            "filename": filename,
            "rows":len(df),
            "columns":len(df.columns),
            "columns_names":list(df.columns),
             "preview": df.head().to_dict(orient="records")
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error processing the file: {str(e)}"
        }), 500