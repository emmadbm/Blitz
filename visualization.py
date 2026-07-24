import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


CHART_FOLDER = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(CHART_FOLDER, exist_ok=True)


def generate_histogram(df, column):
   

    if column not in df.columns:
        raise ValueError(f"{column} not found in dataset.")

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"{column} is not numeric.")

    plt.figure(figsize=(8, 5))

    plt.hist(
        df[column].dropna(),
        bins=10,
        edgecolor="black"
    )

    plt.title(f"Histogram of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    filename = f"{column}_histogram.png"
    filepath = os.path.join(CHART_FOLDER, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return filepath


def generate_pie_chart(df, column):


    if column not in df.columns:
        raise ValueError(f"{column} not found in dataset.")

    counts = df[column].value_counts()

    plt.figure(figsize=(7, 7))

    plt.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(f"{column} Distribution")

    filename = f"{column}_pie.png"
    filepath = os.path.join(CHART_FOLDER, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return filepath


def generate_heatmap(df):
   
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] < 2:
        raise ValueError("Not enough numeric columns for heatmap.")

    correlation = numeric_df.corr()

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        linewidths=0.5
    )

    plt.title("Correlation Heatmap")

    filename = "correlation_heatmap.png"
    filepath = os.path.join(CHART_FOLDER, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return filepath


def generate_all_visualizations(df):
    

    charts = {}

    
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    if numeric_columns:
        charts["histogram"] = generate_histogram(
            df,
            numeric_columns[0]
        )

    
    categorical_columns = df.select_dtypes(
        exclude=["number"]
    ).columns.tolist()

    if categorical_columns:
        charts["pie_chart"] = generate_pie_chart(
            df,
            categorical_columns[0]
        )

    if len(numeric_columns) >= 2:
        charts["heatmap"] = generate_heatmap(df)

    return charts