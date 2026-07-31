import os
import traceback
import pandas as pd

from flask import (
    Blueprint,
    jsonify,
    request
)

from werkzeug.utils import secure_filename

from visualization import generate_all_visualizations
from preprocessing import preprocess_dataset
from machine_learning import run_machine_learning
from ai_insights import generate_ai_insights




main = Blueprint(
    "main",
    __name__
)




UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)




SUPPORTED_EXTENSIONS = (
    ".csv",
    ".xlsx",
    ".xls"
)




def sanitize_dataframe(df):
    """
    Converts NaN values into empty strings
    so they can be safely converted into JSON.
    """

    return (
        df
        .replace({pd.NA: ""})
        .fillna("")
    )




def load_dataset(filepath):
    """
    Loads CSV or Excel datasets.
    """

    if filepath.endswith(".csv"):

        return pd.read_csv(
            filepath,
            sep=None,
            engine="python"
        )

    elif filepath.endswith((".xlsx", ".xls")):

        return pd.read_excel(
            filepath
        )

    raise ValueError(
        "Unsupported file format."
    )



def get_dataset_info(df):
    """
    Returns basic dataset information.
    """

    preview = (
        sanitize_dataframe(df)
        .head()
        .to_dict(
            orient="records"
        )
    )

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "column_names": list(df.columns),

        "preview": preview

    }




def get_validation_report(df):
    """
    Returns validation report.
    """

    return {

        "data_types": df.dtypes.astype(str).to_dict(),

        "missing_values": df.isnull().sum().to_dict(),

        "duplicate_rows": int(
            df.duplicated().sum()
        )

    }


def get_health_report(df):
    """
    Generates dataset health report.
    """

    total_missing = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    health_score = 100

    health_score -= min(
        total_missing * 2,
        30
    )

    health_score -= min(
        duplicate_rows * 5,
        20
    )

    health_score = max(
        0,
        health_score
    )

    if health_score >= 90:
        status = "Excellent"

    elif health_score >= 75:
        status = "Good"

    elif health_score >= 50:
        status = "Fair"

    else:
        status = "Poor"

    return {

        "status": status,

        "health_score": health_score,

        "total_missing_values": total_missing,

        "duplicate_rows": duplicate_rows

    }




def get_summary_statistics(df):
    """
    Returns dataset statistics.
    """

    summary = (

        df.describe(
            include="all"
        )

        .fillna("")

        .replace(
            [float("inf"), float("-inf")],
            ""
        )

    )

    return summary.to_dict()



def analyze_correlations(context):
    """
    Identifies and ranks the strongest relationships
    between numerical features.
    """

    correlation_matrix = context["correlations"]

    # Convert dictionary to DataFrame if needed
    if isinstance(correlation_matrix, dict):
        correlation_matrix = pd.DataFrame(correlation_matrix)

    if correlation_matrix.empty:
        return []

    findings = []
    visited = set()

    for col1 in correlation_matrix.columns:

        for col2 in correlation_matrix.columns:

            if col1 == col2:
                continue

            pair = tuple(sorted((col1, col2)))

            if pair in visited:
                continue

            visited.add(pair)

            try:
                value = float(correlation_matrix.loc[col1, col2])
            except (TypeError, ValueError):
                continue

            if pd.isna(value):
                continue

            if abs(value) >= 0.90:
                strength = "Very Strong"

            elif abs(value) >= 0.70:
                strength = "Strong"

            elif abs(value) >= 0.50:
                strength = "Moderate"

            elif abs(value) >= 0.30:
                strength = "Weak"

            else:
                continue

            findings.append({

                "feature1": col1,

                "feature2": col2,

                "correlation": round(value, 3),

                "strength": strength,

                "direction": (
                    "Positive"
                    if value > 0
                    else "Negative"
                )

            })

    findings.sort(
        key=lambda x: abs(x["correlation"]),
        reverse=True
    )

    return findings
def get_correlation_analysis(df):
    """
    Returns correlation analysis.
    """

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] < 2:
        return {
            "correlation_matrix": {},
            "strongest_correlation": {}
        }

    correlation_matrix = numeric_df.corr().round(2)

    correlation_matrix_dict = (
        correlation_matrix
        .fillna(0)
        .to_dict()
    )

    strongest = {}
    pairs = []

    columns = correlation_matrix.columns

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):

            value = correlation_matrix.iloc[i, j]

            pairs.append({
                "feature_1": columns[i],
                "feature_2": columns[j],
                "correlation": round(float(value), 2)
            })

    if pairs:
        strongest = max(
            pairs,
            key=lambda x: abs(x["correlation"])
        )

    return {
        "correlation_matrix": correlation_matrix_dict,
        "strongest_correlation": strongest
    }
@main.route("/upload", methods=["POST"])
def upload_file():

    try:

     
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

        filename = secure_filename(
            file.filename
        )

        if not filename.lower().endswith(
                SUPPORTED_EXTENSIONS
        ):

            return jsonify({

                "success": False,

                "message": "Unsupported file format."

            }), 400

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        

        df = load_dataset(
            filepath
        )

        df = sanitize_dataframe(
            df
        )


        processed_df, preprocessing_report = preprocess_dataset(
            df
        )

        preprocessing_report["preview"] = (

            sanitize_dataframe(
                processed_df
            )

            .head()

            .to_dict(
                orient="records"
            )

        )

       
        algorithm = request.form.get(
            "algorithm"
        )

        target_column = request.form.get(
            "target_column"
        )

        

        ml_result = None

        if algorithm:

            ml_result = run_machine_learning(

                processed_df,

                algorithm,

                target_column

            )

        dataset_info = get_dataset_info(
            df
        )

        validation = get_validation_report(
            df
        )

        health_report = get_health_report(
            df
        )

        summary_statistics = get_summary_statistics(
            df
        )

        correlation_analysis = get_correlation_analysis(df)
           

        ai_insights = generate_ai_insights(

            processed_df,

            preprocessing_report,

            summary_statistics,

            correlation_analysis["correlation_matrix"],

            ml_result

        )

        

        insights = []

        insights.append(
            f"Dataset contains {len(df)} rows and {len(df.columns)} columns."
        )

        if health_report["total_missing_values"] == 0:

            insights.append(
                "No missing values were found."
            )

        else:

            insights.append(

                f"{health_report['total_missing_values']} missing values detected."

            )

        insights.append(

            f"Dataset health is "

            f"{health_report['status']} "

            f"({health_report['health_score']}/100)."

        )

        if correlation_analysis["strongest_correlation"]:

            strongest = correlation_analysis["strongest_correlation"]

            insights.append(

                f"Strongest relationship found between "

                f"{strongest['feature_1']} and "

                f"{strongest['feature_2']} "

                f"(Correlation = {strongest['correlation']})."

            )

        
        charts = generate_all_visualizations(
            processed_df
        )

        

        return jsonify({

            "success": True,

            "filename": filename,

            "dataset_info": dataset_info,

            "validation": validation,

            "health_report": health_report,

            "analysis": {

                "summary_statistics": summary_statistics,

                "correlation_matrix":
                correlation_analysis["correlation_matrix"],

                "strongest_correlation":
                correlation_analysis["strongest_correlation"]

            },

            "preprocessing": preprocessing_report,

            "machine_learning": ml_result,

            "ai_insights": ai_insights,

            "insights": insights,

            "visualizations": charts

        })

    except Exception as e:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500