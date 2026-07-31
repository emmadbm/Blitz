import pandas as pd

from pandas.api.types import (
    is_numeric_dtype,
    is_object_dtype,
    is_categorical_dtype
)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression
)

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.cluster import KMeans

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    silhouette_score
)

SUPPORTED_ALGORITHMS = {
    "linear regression",
    "logistic regression",
    "decision tree",
    "random forest",
    "k means"
}


def validate_algorithm(algorithm):
    """
    Validates selected algorithm.
    """

    if algorithm is None:

        raise ValueError(
            "Please select an algorithm."
        )

    algorithm = (
        algorithm
        .strip()
        .lower()
        .replace("-", " ")
        .replace("_", " ")
    )

    if algorithm not in SUPPORTED_ALGORITHMS:

        raise ValueError(
            f"Unsupported algorithm: {algorithm}"
        )

    return algorithm


def validate_target(df, target_column):
    """
    Validates target column.
    """

    if target_column is None:

        raise ValueError(
            "Target column is required."
        )

    if target_column not in df.columns:

        raise ValueError(
            f"Target column '{target_column}' not found."
        )


def detect_problem_type(y):
    """
    Detects Regression or Classification.
    """

    if (
        is_object_dtype(y)
        or is_categorical_dtype(y)
    ):

        return "classification"

    if (
        is_numeric_dtype(y)
        and y.nunique() <= 10
    ):

        return "classification"

    return "regression"


def prepare_dataset(df, target_column):
    """
    Splits dataset into features and target.
    """

    validate_target(
        df,
        target_column
    )

    X = df.drop(
        columns=[target_column]
    )

    y = df[target_column]

    X = pd.get_dummies(
        X,
        drop_first=True
    )

    if (
        is_object_dtype(y)
        or is_categorical_dtype(y)
    ):

        encoder = LabelEncoder()

        y = encoder.fit_transform(y)

    return X, y


def split_dataset(
        X,
        y,
        test_size=0.2,
        random_state=42
):

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state
    )
def evaluate_regression(
        y_true,
        predictions
):
    """
    Evaluates regression models.
    """

    mse = mean_squared_error(
        y_true,
        predictions
    )

    rmse = mse ** 0.5

    return {

        "task": "Regression",

        "MAE": round(
            mean_absolute_error(
                y_true,
                predictions
            ),
            4
        ),

        "MSE": round(
            mse,
            4
        ),

        "RMSE": round(
            rmse,
            4
        ),

        "R2 Score": round(
            r2_score(
                y_true,
                predictions
            ),
            4
        )

    }


def evaluate_classification(
        y_true,
        predictions
):
    """
    Evaluates classification models.
    """

    return {

        "task": "Classification",

        "Accuracy": round(
            accuracy_score(
                y_true,
                predictions
            ),
            4
        ),

        "Precision": round(
            precision_score(
                y_true,
                predictions,
                average="weighted",
                zero_division=0
            ),
            4
        ),

        "Recall": round(
            recall_score(
                y_true,
                predictions,
                average="weighted",
                zero_division=0
            ),
            4
        ),

        "F1 Score": round(
            f1_score(
                y_true,
                predictions,
                average="weighted",
                zero_division=0
            ),
            4
        )

    }


def get_feature_importance(
        model,
        feature_names
):
    """
    Returns sorted feature importance
    for tree-based models.
    """

    if not hasattr(
            model,
            "feature_importances_"
    ):

        return {}

    importance = {

        feature: round(
            float(score),
            4
        )

        for feature, score in zip(
            feature_names,
            model.feature_importances_
        )

    }

    importance = dict(

        sorted(

            importance.items(),

            key=lambda item: item[1],

            reverse=True

        )

    )

    return importance
def train_linear_regression(
        X_train,
        X_test,
        y_train,
        y_test
):
    """
    Train Linear Regression model.
    """

    model = LinearRegression()

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    return {

        "success": True,

        "algorithm": "Linear Regression",

        "task": "Regression",

        "metrics": evaluate_regression(
            y_test,
            predictions
        ),

        "predictions": predictions.tolist()

    }


def train_logistic_regression(
        X_train,
        X_test,
        y_train,
        y_test
):
    """
    Train Logistic Regression model.
    """

    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    return {

        "success": True,

        "algorithm": "Logistic Regression",

        "task": "Classification",

        "metrics": evaluate_classification(
            y_test,
            predictions
        ),

        "predictions": predictions.tolist()

    }


def train_decision_tree(
        X_train,
        X_test,
        y_train,
        y_test
):
    """
    Train Decision Tree Classifier.
    """

    model = DecisionTreeClassifier(
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    return {

        "success": True,

        "algorithm": "Decision Tree",

        "task": "Classification",

        "metrics": evaluate_classification(
            y_test,
            predictions
        ),

        "feature_importance": get_feature_importance(
            model,
            X_train.columns
        ),

        "predictions": predictions.tolist()

    }


def train_random_forest(
        X_train,
        X_test,
        y_train,
        y_test
):
    """
    Train Random Forest Classifier.
    """

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    return {

        "success": True,

        "algorithm": "Random Forest",

        "task": "Classification",

        "metrics": evaluate_classification(
            y_test,
            predictions
        ),

        "feature_importance": get_feature_importance(
            model,
            X_train.columns
        ),

        "predictions": predictions.tolist()

    }


def train_kmeans(
        X,
        clusters=3
):
    """
    Train K-Means Clustering model.
    """

    model = KMeans(
        n_clusters=clusters,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(
        X
    )

    score = silhouette_score(
        X,
        labels
    )

    return {

        "success": True,

        "algorithm": "K-Means",

        "task": "Clustering",

        "clusters": clusters,

        "silhouette_score": round(
            score,
            4
        ),

        "cluster_labels": labels.tolist(),

        "cluster_centers": model.cluster_centers_.tolist()

    }
def get_dataset_summary(
        X_train,
        X_test,
        y
):
    """
    Returns dataset summary.
    """

    return {

        "training_samples": len(X_train),

        "testing_samples": len(X_test),

        "total_samples": len(X_train) + len(X_test),

        "features": X_train.shape[1],

        "target_classes": int(
            len(pd.Series(y).unique())
        )

    }
def run_machine_learning(
        df,
        algorithm,
        target_column=None,
        test_size=0.2
):
    """
    Main Machine Learning Controller.
    """

    try:

        # ----------------------------
        # Validate Algorithm
        # ----------------------------

        algorithm = validate_algorithm(
            algorithm
        )

        # ----------------------------
        # K-Means (Unsupervised)
        # ----------------------------

        if algorithm == "k means":

            X = pd.get_dummies(
                df,
                drop_first=True
            )

            return train_kmeans(X)

        # ----------------------------
        # Validate Target
        # ----------------------------

        validate_target(
            df,
            target_column
        )

        X, y = prepare_dataset(
            df,
            target_column
        )

        problem_type = detect_problem_type(
            y
        )

        # ----------------------------
        # Linear Regression Validation
        # ----------------------------

        if (
                algorithm == "linear regression"
                and problem_type != "regression"
        ):

            raise ValueError(

                "Linear Regression requires a numeric target column."

            )

        # ----------------------------
        # Classification Validation
        # ----------------------------

        if (

                algorithm in {

                    "logistic regression",

                    "decision tree",

                    "random forest"

                }

                and

                problem_type != "classification"

        ):

            raise ValueError(

                "Selected target is continuous.\n"
                "Please use Linear Regression."

            )

        # ----------------------------
        # Train Test Split
        # ----------------------------

        X_train, X_test, y_train, y_test = split_dataset(

            X,

            y,

            test_size=test_size

        )
        dataset_summary = get_dataset_summary(
    X_train,
    X_test,
    y
)

        # ----------------------------
        # Run Selected Algorithm
        # ----------------------------

        if algorithm == "linear regression":

            return train_linear_regression(

                X_train,

                X_test,

                y_train,

                y_test

            )

        elif algorithm == "logistic regression":

            result = train_linear_regression(
                X_train,
                X_test,
                y_train,
                y_test
            )

            result["dataset_summary"] = dataset_summary

            return result

        elif algorithm == "decision tree":

            result = train_decision_tree(
                X_train,
                X_test,
                y_train,
                y_test
            )

            result["dataset_summary"] = dataset_summary

            return result

        elif algorithm == "random forest":

            result = train_random_forest(
                X_train,
                X_test,
                y_train,
                y_test
            )

            result["dataset_summary"] = dataset_summary

            return result
        elif algorithm == "k means":

             X = pd.get_dummies(
             df,
            drop_first=True
             )

             result = train_kmeans(X)

             result["dataset_summary"] = {

              "total_samples": len(df),

               "features": X.shape[1],

                "clusters": result["clusters"]

            }

        return result

    except Exception as error:

        return {

            "success": False,

            "error": str(error)

        }
