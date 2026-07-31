import pandas as pd
import numpy as np




def detect_dataset(df):
    """
    Attempts to identify common datasets.
    """

    columns = {

        column.lower()

        for column in df.columns

    }

    if {

        "survived",

        "pclass",

        "sex",

        "age"

    }.issubset(columns):

        return "Titanic Survival Prediction"

    elif {

        "studytime",

        "absences",

        "g3"

    }.issubset(columns):

        return "Student Performance"

    elif {

        "sepal length (cm)",

        "petal length (cm)"

    }.issubset(columns):

        return "Iris Flower Classification"

    elif {

        "medv",

        "rm"

    }.issubset(columns):

        return "Boston Housing"

    return "Custom Dataset"



def collect_context(

        df,

        preprocessing_report,

        statistics,

        correlation_matrix,

        ml_results

):

    return {

        "dataset": {

            "name":

                detect_dataset(df),

            "rows":

                len(df),

            "columns":

                len(df.columns),

            "column_names":

                df.columns.tolist(),

            "numeric_columns":

                df.select_dtypes(

                    include=np.number

                ).columns.tolist(),

            "categorical_columns":

                df.select_dtypes(

                    exclude=np.number

                ).columns.tolist()

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


def analyze_dataset(context):
    """
    Performs a complete analysis of the uploaded dataset.
    """

    dataset = context["dataset"]

    rows = dataset["rows"]
    columns = dataset["columns"]

    numeric = len(dataset["numeric_columns"])
    categorical = len(dataset["categorical_columns"])

    if rows < 100:
        dataset_size = "Small"

    elif rows < 1000:
        dataset_size = "Medium"

    elif rows < 10000:
        dataset_size = "Large"

    else:
        dataset_size = "Very Large"

    

    if columns < 10:
        complexity = "Low"

    elif columns < 30:
        complexity = "Moderate"

    elif columns < 75:
        complexity = "High"

    else:
        complexity = "Very High"


    if numeric >= categorical:
        suitability = (
            "Well suited for statistical analysis "
            "and machine learning."
        )
    else:
        suitability = (
            "Contains many categorical attributes. "
            "Encoding techniques are important before "
            "training machine learning models."
        )

    return {

        "dataset_name": dataset["name"],

        "rows": rows,

        "columns": columns,

        "numeric_features": numeric,

        "categorical_features": categorical,

        "dataset_size": dataset_size,

        "complexity": complexity,

        "ml_suitability": suitability

    }


def analyze_data_quality(context):
    """
    Evaluates the quality of the dataset after preprocessing.
    """

    preprocessing = context["preprocessing"]

    duplicates = preprocessing.get("duplicates", {})
    missing = preprocessing.get("missing_values", {})
    outliers = preprocessing.get("outliers", {})
    encoding = preprocessing.get("encoding", {})
    scaling = preprocessing.get("scaling", {})

    duplicates_removed = duplicates.get(
        "duplicates_removed",
        0
    )

    remaining_missing = missing.get(
        "remaining_missing_values",
        0
    )

    total_outliers = sum(

        value.get("outliers", 0)

        for value in outliers.values()

    )

    encoding_method = encoding.get(
        "method",
        "Not Applied"
    )

    scaling_method = scaling.get(
        "method",
        "Not Applied"
    )

   

    score = 100

    score -= remaining_missing * 2
    score -= min(total_outliers, 20)

    if score < 0:
        score = 0

    if score >= 90:
        quality = "Excellent"

    elif score >= 75:
        quality = "Good"

    elif score >= 60:
        quality = "Fair"

    else:
        quality = "Poor"

    return {

        "quality": quality,

        "quality_score": score,

        "duplicates_removed": duplicates_removed,

        "remaining_missing": remaining_missing,

        "outliers_detected": total_outliers,

        "encoding_method": encoding_method,

        "scaling_method": scaling_method

    }


def analyze_statistics(context):
    """
    Analyzes descriptive statistics and
    generates meaningful observations.
    """

    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    statistics = context["statistics"]

    findings = []

    if not isinstance(statistics, dict):
        return findings

    for column, values in statistics.items():

        if not isinstance(values, dict):
            continue

        mean = safe_float(values.get("mean"))
        median = safe_float(values.get("median"))
        std = safe_float(
            values.get(
                "std",
                values.get("standard_deviation")
            )
        )

        minimum = safe_float(values.get("min"))
        maximum = safe_float(values.get("max"))

        observation = {
            "column": column,
            "mean": mean,
            "median": median,
            "std": std,
            "min": minimum,
            "max": maximum,
            "distribution": "Unknown",
            "variability": "Unknown"
        }

        # Distribution
        if mean is not None and median is not None:

            difference = abs(mean - median)

            if difference < 0.05:
                observation["distribution"] = "Approximately Symmetric"

            elif mean > median:
                observation["distribution"] = "Positively Skewed"

            else:
                observation["distribution"] = "Negatively Skewed"

        # Variability
        if std is not None:

            if std < 1:
                observation["variability"] = "Low"

            elif std < 10:
                observation["variability"] = "Moderate"

            else:
                observation["variability"] = "High"

        findings.append(observation)

    return findings


def analyze_correlations(context):
    """
    Identifies and ranks the strongest relationships
    between numerical features.
    """

    correlation_matrix = context["correlations"]

    if not isinstance(correlation_matrix, pd.DataFrame):
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

            value = float(
                correlation_matrix.loc[col1, col2]
            )

            strength = "Weak"

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

                "direction":

                    "Positive"

                    if value > 0

                    else "Negative"

            })

    findings.sort(

        key=lambda x: abs(x["correlation"]),

        reverse=True

    )

    return findings


def analyze_machine_learning(context):
    """
    Analyzes the trained machine learning model
    and interprets its performance.
    """

    ml = context.get("machine_learning")

    if not ml:
        return None

    algorithm = ml.get(
        "algorithm",
        "Not Selected"
    )

    metrics = ml.get(
        "metrics",
        {}
    )



    if algorithm.lower() == "k-means":

        problem_type = "Clustering"

    elif "Accuracy" in metrics:

        problem_type = "Classification"

    elif "R2 Score" in metrics:

        problem_type = "Regression"

    else:

        problem_type = "Unknown"

    

    performance = "Unknown"

    interpretation = ""

    confidence = "Low"

    if problem_type == "Classification":

        accuracy = metrics.get("Accuracy", 0)

        if accuracy >= 0.90:

            performance = "Excellent"
            confidence = "High"

        elif accuracy >= 0.80:

            performance = "Good"
            confidence = "Moderate"

        elif accuracy >= 0.70:

            performance = "Average"
            confidence = "Moderate"

        else:

            performance = "Needs Improvement"

        interpretation = (

            f"The model achieved an accuracy of "

            f"{accuracy:.2%}, indicating "

            f"{performance.lower()} "

            "classification performance."

        )

    elif problem_type == "Regression":

        r2 = metrics.get("R2 Score", 0)

        if r2 >= 0.90:

            performance = "Excellent"
            confidence = "High"

        elif r2 >= 0.75:

            performance = "Good"
            confidence = "Moderate"

        elif r2 >= 0.60:

            performance = "Average"
            confidence = "Moderate"

        else:

            performance = "Needs Improvement"

        interpretation = (

            f"The regression model achieved an "

            f"R² Score of {r2:.3f}, "

            f"indicating {performance.lower()} "

            "predictive capability."

        )

    elif problem_type == "Clustering":

        performance = "Completed"

        confidence = "Not Applicable"

        interpretation = (

            "The clustering algorithm successfully "

            "grouped similar observations into "

            "distinct clusters."

        )

    

    feature_importance = ml.get(
        "feature_importance",
        {}
    )

    return {

        "algorithm": algorithm,

        "problem_type": problem_type,

        "performance": performance,

        "confidence": confidence,

        "metrics": metrics,

        "feature_importance": feature_importance,

        "interpretation": interpretation

    }
# ------------------------------------
# Dataset Overview
# ------------------------------------

def generate_dataset_overview(context):
    """
    Generates a professional overview of the dataset.
    """

    dataset = analyze_dataset(context)

    overview = []

    overview.append(

        f"The uploaded dataset was identified as the "
        f"**{dataset['dataset_name']}** dataset."

    )

    overview.append(

        f"It contains **{dataset['rows']} records** and "
        f"**{dataset['columns']} original features**, "
        f"classifying it as a "
        f"**{dataset['dataset_size']}** dataset."

    )

    overview.append(

        f"The dataset consists of "
        f"**{dataset['numeric_features']} numerical** "
        f"and "
        f"**{dataset['categorical_features']} categorical** "
        f"features."

    )

    overview.append(

        f"The overall complexity is "
        f"**{dataset['complexity']}**, making it "
        f"{dataset['ml_suitability'].lower()}"

    )

    return " ".join(overview)


def generate_preprocessing_summary(context):
    """
    Generates a detailed summary of all
    preprocessing operations performed.
    """

    quality = analyze_data_quality(context)

    summary = []

  
   
    summary.append(

        f"The dataset achieved an overall "
        f"**{quality['quality']}** quality rating "
        f"with a score of "
        f"**{quality['quality_score']}/100**."

    )

  

    if quality["remaining_missing"] == 0:

        summary.append(

            "All missing values were successfully "
            "handled during preprocessing."

        )

    else:

        summary.append(

            f"{quality['remaining_missing']} missing "
            "values still remain and may require "
            "additional preprocessing."

        )

    
  

    if quality["duplicates_removed"] == 0:

        summary.append(

            "No duplicate records were detected."

        )

    else:

        summary.append(

            f"{quality['duplicates_removed']} duplicate "
            "records were removed."

        )

  

    if quality["encoding_method"] != "Not Applied":

        summary.append(

            f"Categorical variables were transformed "
            f"using **{quality['encoding_method']}**."

        )

    
    if quality["scaling_method"] != "Not Applied":

        summary.append(

            f"Numerical features were scaled using "
            f"**{quality['scaling_method']}**."

        )

  

    if quality["outliers_detected"] == 0:

        summary.append(

            "No significant outliers were detected."

        )

    else:

        summary.append(

            f"A total of "
            f"**{quality['outliers_detected']}** "
            "potential outliers were identified. "
            "These observations should be reviewed "
            "before deploying predictive models."

        )

    return " ".join(summary)

def generate_statistical_summary(context):
    """
    Generates meaningful statistical insights
    from the descriptive statistics.
    """

    statistics = analyze_statistics(context)

    if not statistics:

        return (
            "No numerical statistics were available "
            "for analysis."
        )

    summary = []


    summary.append(

        f"Statistical analysis was performed on "
        f"**{len(statistics)} numerical features**."

    )

  

    high_variability = [

        feature["column"]

        for feature in statistics

        if feature["variability"] == "High"

    ]

    if high_variability:

        summary.append(

            "The following features exhibit "
            "high variability: "

            + ", ".join(high_variability[:5])

            + "."

        )

   
    skewed = [

        feature["column"]

        for feature in statistics

        if feature["distribution"]
        != "Approximately Symmetric"

    ]

    if skewed:

        summary.append(

            "Several variables show skewed "
            "distributions, including "

            + ", ".join(skewed[:5])

            + "."

        )

 

    balanced = [

        feature["column"]

        for feature in statistics

        if feature["distribution"]
        == "Approximately Symmetric"

    ]

    if balanced:

        summary.append(

            "Features such as "

            + ", ".join(balanced[:5])

            + " display relatively "
            "balanced distributions."

        )

    return " ".join(summary)



def generate_correlation_summary(context):
    """
    Generates a professional summary of the
    correlation analysis.
    """

    correlations = analyze_correlations(context)

    if not correlations:

        return (
            "No meaningful correlations were "
            "identified among the numerical features."
        )

    summary = []

    summary.append(

        f"Correlation analysis identified "
        f"**{len(correlations)} meaningful "
        f"relationships** between numerical variables."

    )

   

    strongest = correlations[0]

    summary.append(

        f"The strongest "

        f"{strongest['direction'].lower()} "

        f"correlation was observed between "

        f"**{strongest['feature1']}** and "

        f"**{strongest['feature2']}** "

        f"with a coefficient of "

        f"**{strongest['correlation']}**, "

        f"indicating a "

        f"**{strongest['strength'].lower()}** "

        f"relationship."

    )


    positive = [

        c for c in correlations

        if c["direction"] == "Positive"

    ]

    if positive:

        summary.append(

            f"Approximately **{len(positive)}** "

            "positive relationships were identified, "

            "suggesting that several variables tend "

            "to increase together."

        )

    
    negative = [

        c for c in correlations

        if c["direction"] == "Negative"

    ]

    if negative:

        summary.append(

            f"Approximately **{len(negative)}** "

            "negative relationships were identified, "

            "indicating inverse relationships between "

            "multiple feature pairs."

        )

    summary.append(

        "These relationships can assist in feature "

        "selection, predictive modeling, and "

        "understanding the overall structure of "

        "the dataset."

    )

    return " ".join(summary)

def generate_machine_learning_summary(context):
    """
    Generates a professional summary of the
    machine learning model and its performance.
    """

    ml = analyze_machine_learning(context)

    if ml is None:

        return (
            "No machine learning model was trained "
            "for the uploaded dataset."
        )

    summary = []

   
    summary.append(

        f"The selected machine learning algorithm "
        f"was **{ml['algorithm']}**, which was "
        f"used for a **{ml['problem_type'].lower()}** task."

    )

   

    summary.append(

        f"The trained model demonstrated "
        f"**{ml['performance']}** performance "
        f"with **{ml['confidence']} confidence**."

    )

 
    summary.append(

        ml["interpretation"]

    )

    

    if ml["metrics"]:

        metric_text = []

        for metric, value in ml["metrics"].items():

            if isinstance(value, float):

                metric_text.append(

                    f"{metric}: {value:.3f}"

                )

            else:

                metric_text.append(

                    f"{metric}: {value}"

                )

        summary.append(

            "Performance metrics include "

            + ", ".join(metric_text)

            + "."

        )

   
    if ml["feature_importance"]:

        top_features = list(

            ml["feature_importance"].keys()

        )[:5]

        summary.append(

            "The most influential features include "

            + ", ".join(top_features)

            + "."

        )

    return " ".join(summary)


def generate_executive_summary(context):
    """
    Generates a concise executive summary of the
    complete analysis.
    """

    dataset = analyze_dataset(context)
    quality = analyze_data_quality(context)
    correlations = analyze_correlations(context)
    ml = analyze_machine_learning(context)

    summary = []

    

    summary.append(

        f"The analysis was successfully completed "
        f"on the **{dataset['dataset_name']}** dataset, "
        f"which contains **{dataset['rows']} records** "
        f"and **{dataset['columns']} features**."

    )

   

    summary.append(

        f"The preprocessing pipeline produced an "
        f"overall **{quality['quality']}** data quality "
        f"rating with a score of "
        f"**{quality['quality_score']}/100**."

    )

    
    if correlations:

        strongest = correlations[0]

        summary.append(

            f"The strongest relationship was found "
            f"between **{strongest['feature1']}** "
            f"and **{strongest['feature2']}**, "
            f"showing a "
            f"**{strongest['strength'].lower()} "
            f"{strongest['direction'].lower()} "
            f"correlation**."

        )

  
    if ml:

        summary.append(

            f"The **{ml['algorithm']}** model "

            f"delivered **{ml['performance'].lower()}** "

            f"performance for this "

            f"**{ml['problem_type'].lower()}** task."

        )

   
    summary.append(

        "Overall, the dataset is well prepared for "
        "exploratory analysis and predictive "
        "modeling, providing reliable insights for "
        "data-driven decision making."

    )

    return " ".join(summary)


def generate_recommendations(context):
    """
    Generates intelligent recommendations based on
    dataset quality, statistical analysis,
    correlations and machine learning results.
    """

    dataset = analyze_dataset(context)
    quality = analyze_data_quality(context)
    correlations = analyze_correlations(context)
    ml = analyze_machine_learning(context)

    recommendations = []

   
    if quality["remaining_missing"] > 0:

        recommendations.append(

            "Handle the remaining missing values "
            "before deploying predictive models."

        )

    else:

        recommendations.append(

            "The dataset is free from missing values "
            "and is suitable for further analysis."

        )

   

    if quality["outliers_detected"] > 20:

        recommendations.append(

            "Review the detected outliers, as they "
            "may significantly influence model "
            "performance."

        )

   
    if correlations:

        strongest = correlations[0]

        recommendations.append(

            f"Consider using **{strongest['feature1']}** "
            f"and **{strongest['feature2']}** during "
            "feature engineering because they exhibit "
            "a strong relationship."

        )


    if ml:

        if ml["performance"] == "Excellent":

            recommendations.append(

                "The trained model demonstrates strong "
                "predictive capability and can serve as "
                "a reliable baseline model."

            )

        elif ml["performance"] == "Good":

            recommendations.append(

                "Hyperparameter tuning may further "
                "improve the predictive performance."

            )

        elif ml["performance"] == "Average":

            recommendations.append(

                "Consider feature engineering and "
                "additional preprocessing to improve "
                "model accuracy."

            )

        else:

            recommendations.append(

                "Experiment with alternative machine "
                "learning algorithms and additional "
                "feature engineering."

            )

   

    if dataset["dataset_size"] == "Small":

        recommendations.append(

            "Collecting additional data may improve "
            "model generalization."

        )

    elif dataset["dataset_size"] == "Large":

        recommendations.append(

            "The dataset is sufficiently large for "
            "building robust predictive models."

        )

   
    recommendations.append(

        "Continue monitoring data quality and "
        "regularly validate model performance as "
        "new data becomes available."

    )

    return recommendations
def generate_ai_insights(
    df,
    preprocessing_report,
    statistics,
    correlation_matrix,
    ml_results
):
    """
    Main AI Insight Engine.
    """

    context = collect_context(
        df,
        preprocessing_report,
        statistics,
        correlation_matrix,
        ml_results
    )

    return {

        "dataset_overview":
            generate_dataset_overview(context),

        "preprocessing_summary":
            generate_preprocessing_summary(context),

        "statistical_summary":
            generate_statistical_summary(context),

        "correlation_summary":
            generate_correlation_summary(context),

        "machine_learning_summary":
            generate_machine_learning_summary(context),

        "executive_summary":
            generate_executive_summary(context),

        "recommendations":
            generate_recommendations(context)

    }