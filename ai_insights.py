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