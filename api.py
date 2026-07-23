import os
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

    return jsonify({
        "success": True,
        "filename": filename,
        "message": "File uploaded successfully."
    })