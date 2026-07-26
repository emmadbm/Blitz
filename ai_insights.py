import pandas as pd 
import numpy as np

def collect_context(
        df,
        preprocessing_report,statistics, correlation_matrix, ml_results):
    context= {

   

        "dataset": {

            "rows": len(df),

            "columns": len(df.columns),

            "numeric_columns":
                df.select_dtypes(
                    include=np.number
                ).columns.tolist(),

            "categorical_columns":
                df.select_dtypes(
                    exclude=np.number
                ).columns.tolist(),

            "column_names":
                df.columns.tolist()

        },

       

        "preprocessing": preprocessing_report,

     
        "statistics": statistics,

        

        "correlation_matrix": correlation_matrix,

        

        "machine_learning": ml_results

    }

    return context














import pandas as pd
import numpy as np


def collect_context(
        df,
        preprocessing_report,
        statistics,
        correlation_matrix,
        ml_results
):
    """
    Collects all information required by the AI
    Insight Engine.
    """

    context = {

        "dataset": {

            "rows": len(df),

            "columns": len(df.columns),

            "numeric_columns":
                df.select_dtypes(
                    include=np.number
                ).columns.tolist(),

            "categorical_columns":
                df.select_dtypes(
                    exclude=np.number
                ).columns.tolist(),

            "column_names":
                df.columns.tolist()

        },

        "preprocessing":
            preprocessing_report,

        "statistics":
            statistics,

        "correlations":
            correlation_matrix,

        "machine_learning":
            ml_results

    }

    return context


def analyze_dataset(context):
    """
    Evaluates dataset size and complexity.
    """

    rows = context["dataset"]["rows"]

    columns = context["dataset"]["columns"]

    numeric = len(
        context["dataset"]["numeric_columns"]
    )

    categorical = len(
        context["dataset"]["categorical_columns"]
    )

    # ------------------------
    # Dataset Size
    # ------------------------

    if rows < 100:

        dataset_size = "Small"

    elif rows < 1000:

        dataset_size = "Medium"

    else:

        dataset_size = "Large"

    # ------------------------
    # Dataset Complexity
    # ------------------------

    if columns < 10:

        complexity = "Low"

    elif columns < 30:

        complexity = "Moderate"

    else:

        complexity = "High"

    return {

        "dataset_size": dataset_size,

        "complexity": complexity,

        "rows": rows,

        "columns": columns,

        "numeric_features": numeric,

        "categorical_features": categorical

    }


def analyze_data_quality(context):
    """
    Evaluates preprocessing results.
    """

    preprocessing = context["preprocessing"]

    duplicates = preprocessing.get(
        "duplicates",
        {}
    )

    missing = preprocessing.get(
        "missing_values",
        {}
    )

    outliers = preprocessing.get(
        "outliers",
        {}
    )

    duplicate_count = duplicates.get(
        "duplicates_removed",
        0
    )

    remaining_missing = missing.get(
        "remaining_missing_values",
        0
    )

    total_outliers = sum(

        value["outliers"]

        for value in outliers.values()

    )

    # ------------------------
    # Overall Quality
    # ------------------------

    if remaining_missing == 0 and duplicate_count == 0:

        quality = "Excellent"

    elif remaining_missing <= 5:

        quality = "Good"

    else:

        quality = "Needs Improvement"

    return {

        "quality": quality,

        "duplicates_removed":
            duplicate_count,

        "remaining_missing":
            remaining_missing,

        "total_outliers":
            total_outliers

    }


def analyze_statistics(context):
    """
    Finds interesting statistical observations.
    """

    statistics = context["statistics"]

    findings = []

    if isinstance(statistics, dict):

        for column, values in statistics.items():

            if not isinstance(values, dict):

                continue

            mean = values.get("mean")

            median = values.get("median")

            std = values.get(
                "std",
                values.get("standard_deviation")
            )

            observation = {

                "column": column,

                "mean": mean,

                "median": median,

                "std": std

            }

            findings.append(
                observation
            )

    return findings


def analyze_correlations(context):
    """
    Extracts meaningful relationships from
    correlation matrix.
    """

    correlations = context["correlations"]

    findings = []

    if isinstance(correlations, pd.DataFrame):

        visited = set()

        for col1 in correlations.columns:

            for col2 in correlations.columns:

                if col1 == col2:

                    continue

                pair = tuple(

                    sorted(

                        [col1, col2]

                    )

                )

                if pair in visited:

                    continue

                visited.add(pair)

                value = correlations.loc[
                    col1,
                    col2
                ]

                if abs(value) >= 0.70:

                    findings.append({

                        "feature1": col1,

                        "feature2": col2,

                        "correlation":
                            round(
                                float(value),
                                2
                            ),

                        "strength":
                            "Strong",

                        "direction":

                            "Positive"

                            if value > 0

                            else "Negative"

                    })

    findings = sorted(

        findings,

        key=lambda x:

        abs(x["correlation"]),

        reverse=True

    )

    return findings

def analyze_machine_learning(context):
    """
    Evaluates machine learning performance and extracts
    meaningful observations.
    """

    ml = context.get("machine_learning")

    if not ml:
        return None

    algorithm = ml.get("algorithm", "Unknown Model")
    metrics = ml.get("metrics", {})

    performance = "Unknown"
    confidence = "Low"

    if "Accuracy" in metrics:

        accuracy = metrics["Accuracy"]

        if accuracy >= 0.90:
            performance = "Excellent"
            confidence = "High"

        elif accuracy >= 0.80:
            performance = "Good"
            confidence = "Moderate"

        else:
            performance = "Needs Improvement"

    elif "R2 Score" in metrics:

        r2 = metrics["R2 Score"]

        if r2 >= 0.85:
            performance = "Excellent"
            confidence = "High"

        elif r2 >= 0.70:
            performance = "Good"
            confidence = "Moderate"

        else:
            performance = "Needs Improvement"

    return {

        "algorithm": algorithm,

        "metrics": metrics,

        "performance": performance,

        "confidence": confidence

    }


def generate_key_findings(context):
    """
    Generates the most important observations from the dataset.
    """

    findings = []

    dataset = analyze_dataset(context)

    quality = analyze_data_quality(context)

    correlations = analyze_correlations(context)

    ml = analyze_machine_learning(context)

    # Dataset Size

    findings.append(

        f"The dataset contains {dataset['rows']} records and "
        f"{dataset['columns']} features, providing a "
        f"{dataset['dataset_size'].lower()} sized dataset "
        f"for analysis."

    )

    # Data Quality

    findings.append(

        f"The overall quality of the dataset is "
        f"{quality['quality'].lower()} after preprocessing."

    )

    # Correlations

    if correlations:

        strongest = correlations[0]

        findings.append(

            f"The strongest relationship was observed between "
            f"{strongest['feature1']} and "
            f"{strongest['feature2']} "
            f"(correlation = {strongest['correlation']})."

        )

    # Machine Learning

    if ml:

        findings.append(

            f"{ml['algorithm']} demonstrated "
            f"{ml['performance'].lower()} predictive performance."

        )

    return findings


def generate_recommendations(context):
    """
    Generates recommendations based on findings.
    """

    recommendations = []

    quality = analyze_data_quality(context)

    correlations = analyze_correlations(context)

    ml = analyze_machine_learning(context)

    # Missing Values

    if quality["remaining_missing"] > 0:

        recommendations.append(

            "Additional preprocessing is recommended to handle the remaining missing values."

        )

    # Outliers

    if quality["total_outliers"] > 20:

        recommendations.append(

            "Review the detected outliers before training predictive models, as they may influence model performance."

        )

    # Correlations

    if correlations:

        strongest = correlations[0]

        if strongest["direction"] == "Positive":

            recommendations.append(

                f"Leverage the strong relationship between "
                f"{strongest['feature1']} and "
                f"{strongest['feature2']} during decision making."

            )

        else:

            recommendations.append(

                f"Investigate the negative relationship between "
                f"{strongest['feature1']} and "
                f"{strongest['feature2']} to understand its impact."

            )

    # Machine Learning

    if ml:

        if ml["performance"] == "Excellent":

            recommendations.append(

                "The trained model demonstrates strong predictive capability and can be considered for future predictions."

            )

        elif ml["performance"] == "Needs Improvement":

            recommendations.append(

                "Consider feature engineering or experimenting with alternative algorithms to improve model performance."

            )

    return recommendations
def generate_executive_summary(context):
    """
    Generates a professional executive summary based on
    the overall analysis.
    """

    dataset = analyze_dataset(context)
    quality = analyze_data_quality(context)
    correlations = analyze_correlations(context)
    ml = analyze_machine_learning(context)

    summary = []

    # Dataset

    summary.append(

        f"The uploaded dataset contains {dataset['rows']} records "
        f"and {dataset['columns']} features, making it a "
        f"{dataset['dataset_size'].lower()} dataset suitable for "
        "exploratory analysis and predictive modeling."

    )

    # Data Quality

    if quality["quality"] == "Excellent":

        summary.append(

            "The dataset demonstrates excellent quality after preprocessing. "
            "Missing values have been handled successfully and duplicate "
            "records do not affect the analysis."

        )

    elif quality["quality"] == "Good":

        summary.append(

            "The dataset is generally clean and suitable for analysis, "
            "although minor preprocessing considerations remain."

        )

    else:

        summary.append(

            "The dataset requires additional preprocessing before reliable "
            "analysis and modeling can be performed."

        )

    # Correlation

    if correlations:

        strongest = correlations[0]

        summary.append(

            f"The strongest relationship exists between "
            f"{strongest['feature1']} and "
            f"{strongest['feature2']}, indicating an important "
            "pattern within the dataset."

        )

    # Machine Learning

    if ml:

        summary.append(

            f"The {ml['algorithm']} model achieved "
            f"{ml['performance'].lower()} predictive performance, "
            "indicating that meaningful relationships exist within "
            "the available features."

        )

    return " ".join(summary)


def generate_ai_insights(
        df,
        preprocessing_report,
        statistics,
        correlation_matrix,
        ml_results
):
    """
    Main AI Insight Generation Controller.
    """

    context = collect_context(
        df,
        preprocessing_report,
        statistics,
        correlation_matrix,
        ml_results
    )

    dataset_analysis = analyze_dataset(
        context
    )

    quality_analysis = analyze_data_quality(
        context
    )

    statistics_analysis = analyze_statistics(
        context
    )

    correlation_analysis = analyze_correlations(
        context
    )

    ml_analysis = analyze_machine_learning(
        context
    )

    key_findings = generate_key_findings(
        context
    )

    recommendations = generate_recommendations(
        context
    )

    executive_summary = generate_executive_summary(
        context
    )

    return {

        "dataset_analysis": dataset_analysis,

        "data_quality": quality_analysis,

        "statistics_analysis": statistics_analysis,

        "correlation_analysis": correlation_analysis,

        "machine_learning_analysis": ml_analysis,

        "executive_summary": executive_summary,

        "key_findings": key_findings,

        "recommendations": recommendations

    }