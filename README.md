# ⚡ Blitz – AI-Powered Data Analytics Platform

Blitz is an AI-powered data analytics platform that simplifies the process of exploring, cleaning, analyzing, visualizing, and interpreting datasets. It provides an interactive dashboard where users can upload CSV or Excel datasets, preprocess data, generate visualizations, apply machine learning algorithms, and receive automatically generated analytical insights.

The project was developed to make data analysis easier by combining data preprocessing, visualization, machine learning, and intelligent report generation into a single platform.

---

## Why "Blitz"?

The name **Blitz** represents the idea of **never missing the most important data point**.

The inspiration comes from the expression that a "blitz" is someone who misses the most important moment because it happens just after they leave. This project is built around the opposite idea—capturing every meaningful pattern, trend, and relationship within a dataset so that no valuable insight goes unnoticed.

Every uploaded dataset is processed, analyzed, and transformed into meaningful information that helps users make informed decisions.

---

# Features

### Dataset Upload
- Upload CSV files
- Upload Excel (.xlsx / .xls) files
- Automatic dataset preview

### Data Validation
- Missing value detection
- Duplicate row detection
- Data type validation
- Dataset health score generation

### Data Preprocessing
- Duplicate removal
- Missing value handling
- Feature scaling
- Feature encoding
- Outlier detection
- Dataset preprocessing summary

### Data Analysis
- Descriptive statistics
- Correlation analysis
- Strongest feature relationship detection

### Data Visualization
- Histograms
- Pie Charts
- Correlation Heatmaps
- Interactive dashboard visualization

### Machine Learning
Supported algorithms:

- Linear Regression
- Logistic Regression
- Decision Tree
- Random Forest
- K-Means Clustering

Each model generates relevant evaluation metrics based on the selected algorithm.

### AI Insights

Blitz automatically generates:

- Executive Summary
- Dataset Overview
- Data Quality Assessment
- Correlation Insights
- Machine Learning Interpretation
- Final Analytical Summary

> **Note:** Blitz generates AI-style insights using internally developed rule-based logic. It does **not** rely on external AI APIs or chatbot services.

---

# Technologies Used

## Backend

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn

## Frontend

- HTML5
- CSS3
- JavaScript

## Development Tools

- Visual Studio Code
- Git
- GitHub
- Postman

---

# Project Structure

```
Blitz/
│
├── backend/
│   ├── api.py
│   ├── preprocessing.py
│   ├── machine_learning.py
│   ├── visualization.py
│   ├── ai_insights.py
│   ├── uploads/
│   └── static/
│       └── charts/
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Blitz.git
```

Move into the project directory

```bash
cd Blitz
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

# Workflow

1. Upload a CSV or Excel dataset.
2. Select a Machine Learning algorithm.
3. Select the target column.
4. Click **Analyze Dataset**.
5. Blitz performs:
   - Data validation
   - Preprocessing
   - Statistical analysis
   - Visualization generation
   - Machine learning
   - AI insight generation
6. Results are displayed through an interactive dashboard.

---

# API Testing

The backend APIs were tested using **Postman** during development to verify:

- File upload
- Dataset validation
- Machine learning execution
- JSON responses
- Error handling

---

# Dashboard

The application dashboard displays:

- Dataset Information
- Dataset Health Report
- Preprocessing Summary
- Machine Learning Results
- AI Insights
- Charts and Visualizations

---

# Screenshots

Add screenshots here.

```
Home Page

Dashboard

Charts

Machine Learning Results

AI Insights
```

---

# Future Improvements

- Additional machine learning algorithms
- Time-series forecasting
- Interactive visualization filters
- PDF report generation
- User authentication
- Database integration
- Model comparison dashboard
- Export analysis reports

---

# Contributors

**Bhumika Mehra**

Computer Science and Engineering

---

# License

This project is intended for educational and academic purposes.