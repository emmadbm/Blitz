import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder




def remove_duplicates(df):
    """
    Removes duplicate rows from the dataset.
    Returns the cleaned dataframe and statistics.
    """

    original_rows = len(df)

    df = df.drop_duplicates()

    new_rows = len(df)

    return df, {
        "original_rows": original_rows,
        "duplicates_removed": original_rows - new_rows,
        "remaining_rows": new_rows
    }




def handle_missing_values(df, strategy="mean"):
    """
    Handles missing values.

    Strategies:
    mean
    median
    mode
    drop
    """

    df = df.copy()

    if strategy == "drop":
        df = df.dropna()

    else:

        numeric_columns = df.select_dtypes(include=["number"]).columns
        categorical_columns = df.select_dtypes(exclude=["number"]).columns

        # Numeric columns
        for col in numeric_columns:

            if strategy == "mean":
                df[col] = df[col].fillna(df[col].mean())

            elif strategy == "median":
                df[col] = df[col].fillna(df[col].median())

            elif strategy == "mode":
                df[col] = df[col].fillna(df[col].mode()[0])

        # Categorical columns always filled with mode
        for col in categorical_columns:

            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

    missing_after = int(df.isnull().sum().sum())

    return df, {
        "strategy": strategy,
        "remaining_missing_values": missing_after
    }


def detect_outliers(df):
    """
    Detects outliers using the IQR method.
    """

    report = {}

    numeric_columns = df.select_dtypes(include=["number"]).columns

    for col in numeric_columns:

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower) | (df[col] > upper)]

        report[col] = {
            "outliers": len(outliers)
        }

    return report



def scale_features(df, method="standard"):
    """
    Scaling methods:

    standard
    minmax
    """

    df = df.copy()

    numeric_columns = df.select_dtypes(include=["number"]).columns

    if len(numeric_columns) == 0:
        return df

    if method == "standard":
        scaler = StandardScaler()

    elif method == "minmax":
        scaler = MinMaxScaler()

    else:
        raise ValueError("Invalid scaling method.")

    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df



def encode_features(df, method="onehot"):
    """
    Encoding methods:

    onehot
    label
    """

    df = df.copy()

    categorical_columns = df.select_dtypes(exclude=["number"]).columns

    if method == "onehot":

        df = pd.get_dummies(
            df,
            columns=categorical_columns,
            drop_first=True
        )

    elif method == "label":

        encoder = LabelEncoder()

        for col in categorical_columns:
            df[col] = encoder.fit_transform(df[col].astype(str))

    else:
        raise ValueError("Invalid encoding method.")

    return df




def preprocess_dataset(
        df,
        missing_strategy="mean",
        scaling_method="standard",
        encoding_method="onehot",
        remove_duplicate_rows=True
):
  
    report = {}

    # Remove duplicates
    if remove_duplicate_rows:
        df, duplicate_report = remove_duplicates(df)
        report["duplicates"] = duplicate_report

    # Handle missing values
    df, missing_report = handle_missing_values(
        df,
        strategy=missing_strategy
    )
    report["missing_values"] = missing_report

    # Detect outliers
    report["outliers"] = detect_outliers(df)

    # Scale features
    df = scale_features(
        df,
        method=scaling_method
    )
    report["scaling"] = {"method": scaling_method}

    # Encode categorical features
    df = encode_features(
        df,
        method=encoding_method
    )
    report["encoding"] = {"method": encoding_method}

    report["final_shape"] = {
        "rows": df.shape[0],
        "columns": df.shape[1]
    }

    return df, report