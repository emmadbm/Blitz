import os
import pandas as pd
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from visualization import generate_all_visualizations

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
            df = pd.read_csv(filepath, sep=None, engine="python")

        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(filepath)

        else:
            return jsonify({
                "success": False,
                "message": "Unsupported file format. Please upload CSV or Excel."
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
        health_score -= min(duplicate_rows * 5, 20)

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

    

        summary_statistics = (
            df.describe(include="all")
            .fillna("")
            .to_dict()
        )


        numeric_df = df.select_dtypes(include=["number"])

        correlation_matrix_dict = {}
        strongest_correlation = {}

        if numeric_df.shape[1] >= 2:

            correlation_matrix = numeric_df.corr().round(2)

            correlation_matrix_dict = correlation_matrix.to_dict()

            corr_pairs = []

            columns = correlation_matrix.columns

            for i in range(len(columns)):
                for j in range(i + 1, len(columns)):

                    value = correlation_matrix.iloc[i, j]

                    corr_pairs.append({
                        "feature_1": columns[i],
                        "feature_2": columns[j],
                        "correlation": round(float(value), 2)
                    })

            if corr_pairs:

                strongest_correlation = max(
                    corr_pairs,
                    key=lambda x: abs(x["correlation"])
                )

        
        analysis = {
            "summary_statistics": summary_statistics,
            "correlation_matrix": correlation_matrix_dict,
            "strongest_correlation": strongest_correlation,
        }

        insights = []

        insights.append(
            f"Dataset contains {len(df)} rows and {len(df.columns)} columns."
       )

        if total_missing == 0:
          insights.append("No missing values were found.")
        else:
              insights.append(f"{total_missing} missing values detected.")

        insights.append(
            f"Dataset health is {status} ({health_score}/100)."
        )


        if strongest_correlation:
            insights.append(
                f"Strongest relationship found between "
                f"{strongest_correlation['feature_1']} and "
                f"{strongest_correlation['feature_2']} "
                f"(Correlation = {strongest_correlation['correlation']})."
            )
        charts = generate_all_visualizations(df)
        return jsonify({
            "success": True,
            "filename": filename,
            "dataset_info": dataset_info,
            "validation": validation,
            "health_report": health_report,
            "analysis": analysis,
            "insights": insights,
            "visualizations": charts
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": f"Error processing the file: {str(e)}"
        }), 500