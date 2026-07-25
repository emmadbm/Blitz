import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

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


def prepare_dataset(df, target_column):
    """
    Separates features and target column.
    """

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found.")

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X = pd.get_dummies(X, drop_first=True)

    return X, y


def split_dataset(
        X,
        y,
        test_size=0.2,
        random_state=42
):
    """
    Splits dataset into train and test sets.
    """

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
    Returns regression metrics.
    """

    mse = mean_squared_error(
        y_true,
        predictions
    )

    return {

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
            mse ** 0.5,
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
    Returns classification metrics.
    """

    return {

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
    Returns feature importance for tree models.
    """

    if not hasattr(model, "feature_importances_"):
        return {}

    importance = {}

    for feature, value in zip(
            feature_names,
            model.feature_importances_
    ):

        importance[feature] = round(
            float(value),
            4
        )

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

    metrics = evaluate_regression(
        y_test,
        predictions
    )

    return {
        "algorithm": "Linear Regression",
        "metrics": metrics,
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

    metrics = evaluate_classification(
        y_test,
        predictions
    )

    return {
        "algorithm": "Logistic Regression",
        "metrics": metrics,
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

    metrics = evaluate_classification(
        y_test,
        predictions
    )

    feature_importance = get_feature_importance(
        model,
        X_train.columns
    )

    return {
        "algorithm": "Decision Tree",
        "metrics": metrics,
        "feature_importance": feature_importance,
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

    metrics = evaluate_classification(
        y_test,
        predictions
    )

    feature_importance = get_feature_importance(
        model,
        X_train.columns
    )

    return {
        "algorithm": "Random Forest",
        "metrics": metrics,
        "feature_importance": feature_importance,
        "predictions": predictions.tolist()
    }


def train_kmeans(
        X,
        clusters=3
):
    """
    Train K-Means clustering model.
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
        "algorithm": "K-Means",
        "clusters": clusters,
        "silhouette_score": round(
            score,
            4
        ),
        "cluster_labels": labels.tolist(),
        "cluster_centers": model.cluster_centers_.tolist()
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

    if algorithm is None:
        raise ValueError("Algorithm is required.")

    # Normalize algorithm name
    algorithm = (
        algorithm.strip()
        .lower()
        .replace("-", " ")
        .replace("_", " ")
    )

    # -------------------------------
    # K-Means (Unsupervised Learning)
    # -------------------------------
    if algorithm == "k means":

        X = pd.get_dummies(
            df,
            drop_first=True
        )

        return train_kmeans(X)

    # --------------------------------
    # Supervised Learning
    # --------------------------------
    if target_column is None:
        raise ValueError(
            "Target column is required for supervised learning."
        )

    X, y = prepare_dataset(
        df,
        target_column
    )

    X_train, X_test, y_train, y_test = split_dataset(
        X,
        y,
        test_size=test_size
    )

    # -------------------------------
    # Linear Regression
    # -------------------------------
    if algorithm == "linear regression":

        return train_linear_regression(
            X_train,
            X_test,
            y_train,
            y_test
        )

    # -------------------------------
    # Logistic Regression
    # -------------------------------
    elif algorithm == "logistic regression":

        return train_logistic_regression(
            X_train,
            X_test,
            y_train,
            y_test
        )

    # -------------------------------
    # Decision Tree
    # -------------------------------
    elif algorithm == "decision tree":

        return train_decision_tree(
            X_train,
            X_test,
            y_train,
            y_test
        )

    # -------------------------------
    # Random Forest
    # -------------------------------
    elif algorithm == "random forest":

        return train_random_forest(
            X_train,
            X_test,
            y_train,
            y_test
        )

    # -------------------------------
    # Invalid Algorithm
    # -------------------------------
    else:

        raise ValueError(
            f"Unsupported algorithm: {algorithm}"
        )