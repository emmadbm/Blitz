from flask import Blueprint, jsonify

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({
        "message": "Welcome to Blitz API 🚀"
    })
@main.route("/health")
def health():
    return {
        "status": "OK",
        "service": "Blitz API"
    }