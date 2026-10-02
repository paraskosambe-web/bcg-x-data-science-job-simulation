# BCG X Data Science Virtual Experience – PowerCo Customer Churn Analysis

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.2%2B-orange.svg)](https://scikit-learn.org/)
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

## 📌 Project Overview

This project is completed as part of the **BCG X Data Science Virtual Experience**, focusing on customer churn analysis for **PowerCo**, a major energy utility provider.

PowerCo partnered with BCG X to investigate declining customer retention within its **Small & Medium Enterprise (SME)** customer segment. The initial business hypothesis proposed by PowerCo leadership was that customer churn was primarily driven by **price sensitivity**.

The project applies exploratory data analysis, feature engineering, and predictive modeling to investigate the factors associated with customer churn and develop a machine learning model for identifying customers at higher risk of churn.

### 🎯 Business Objective

The primary objectives of the analysis were to:

* Investigate the factors associated with customer churn.
* Evaluate whether price sensitivity is a major contributor to churn.
* Identify customer characteristics and behavioral patterns associated with churn.
* Engineer meaningful features from customer and pricing data.
* Develop a machine learning model to predict churn risk.
* Translate analytical findings into actionable business insights.

---

## 💡 Executive Summary

The analysis indicates that **price sensitivity alone does not appear to be the primary driver of customer churn**.

Although pricing-related variables show some relationship with churn, other customer characteristics and historical behavioral variables provide stronger predictive signals.

The analysis highlights the importance of **customer tenure, historical energy consumption, margin-related metrics, and contract-related characteristics** when assessing churn risk.

A **Random Forest Classifier** was developed as the predictive model and achieved approximately **90% overall accuracy** on the test evaluation data.

The findings suggest that customer retention strategies should consider a broader range of customer characteristics rather than relying exclusively on price-based interventions.

---

## 📊 Key Business Findings

### 1. Price Sensitivity

Price-related variables show some association with customer churn; however, their predictive contribution is relatively limited compared with several customer and consumption-related variables.

The analysis therefore does not support the hypothesis that price sensitivity is the sole or dominant explanation for customer churn.

### 2. Customer Tenure

Customer tenure emerged as an important factor in understanding churn behavior. The length of the customer relationship provides useful information when identifying customers who may be at higher risk of leaving.

### 3. Consumption History

Historical energy consumption, particularly information derived from the previous 12 months, provides meaningful predictive information for identifying potential churn.

### 4. Margin Metrics

Customer margin-related variables were among the important predictors in the trained model. These metrics can help identify high-value customer accounts where retention efforts may have greater business relevance.

### 5. Contract and Renewal Characteristics

Contract-related information and renewal periods provide additional context for understanding customer churn risk and can support targeted retention activities.

### 6. Predictive Model

A **Random Forest Classifier** was trained to predict customer churn.

The model achieved approximately:

**~90% overall test accuracy**

Model evaluation included classification metrics and ROC-based analysis to assess predictive performance.

---

## 🔍 Data Analysis Approach

The project follows a structured data science workflow:

```text
Business Understanding
        ↓
Data Exploration
        ↓
Data Cleaning
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
Feature Preparation
        ↓
Model Training
        ↓
Model Evaluation
        ↓
Feature Importance Analysis
        ↓
Business Insights
```

---

## 📂 Dataset

The project uses two primary datasets provided as part of the BCG X simulation:

### Client Data

`client_data.csv`

Contains customer-level information used to understand customer characteristics, consumption behavior, margins, contract information, and churn.

### Price Data

`price_data.csv`

Contains historical pricing information used to investigate the relationship between pricing patterns and customer churn.

---

## 📊 Data Pipeline & Directory Structure

```text
bcg-x-data-science-job-simulation/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── client_data.csv
│   │   └── price_data.csv
│   │
│   └── processed/
│       ├── clean_data_after_eda.csv
│       ├── clean_data_engineering.csv
│       └── data_for_prediction.csv
│
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_predictive_modeling.ipynb
│
├── reports/
│   ├── Executive_Summary_Slide.pdf
│   └── Executive_Summary_Slide.html
│
└── outputs/
    ├── feature_importances.png
    └── roc_curve.png
```

---

## 🔄 Data Pipeline

| Stage                  | Dataset                             | Description                                                                                                                                   |
| ---------------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Raw Input**          | `client_data.csv`, `price_data.csv` | Original customer and historical pricing records provided by PowerCo.                                                                         |
| **Cleaned**            | `clean_data_after_eda.csv`          | Dataset prepared after exploratory analysis, including data cleaning, duplicate handling, missing-value treatment, and data-type corrections. |
| **Feature Engineered** | `clean_data_engineering.csv`        | Dataset enriched with pricing variation metrics, peak/off-peak price differences, tenure-related features, and other derived variables.       |
| **Model Ready**        | `data_for_prediction.csv`           | Transformed dataset prepared for machine learning model training and prediction.                                                              |

---

## 🧹 Data Preparation

The data preparation process included:

* Inspecting dataset structure and data types.
* Identifying missing values.
* Checking for duplicate records.
* Handling data-quality issues.
* Converting variables into appropriate data types.
* Investigating distributions and relationships between variables.
* Preparing datasets for feature engineering and predictive modeling.

---

## ⚙️ Feature Engineering

Feature engineering was performed to transform the available customer and pricing information into variables that could provide stronger predictive signals.

The engineered features included information related to:

* Customer tenure.
* Historical energy consumption.
* Pricing variation.
* Peak and off-peak price differences.
* Customer margin.
* Contract-related characteristics.
* Other relevant customer and pricing attributes.

These engineered variables were subsequently prepared for use in the predictive modeling workflow.

---

## 🤖 Machine Learning Model

### Random Forest Classifier

A **Random Forest Classifier** was used for customer churn prediction.

Random Forest was selected because it can:

* Handle multiple numerical and categorical features.
* Capture non-linear relationships.
* Model interactions between variables.
* Provide feature importance information.
* Work effectively as a baseline classification approach for structured tabular data.

### Model Evaluation

The trained model was evaluated using test data.

Evaluation included:

* Accuracy
* Classification performance metrics
* ROC curve analysis
* Feature importance analysis

The model achieved approximately **90% overall accuracy** on the test evaluation data.

---

## 📈 Model Interpretability

Feature importance analysis was used to understand which variables contributed most to the model's churn predictions.

The analysis highlighted variables related to:

* Total net margin.
* Customer tenure.
* Historical consumption.
* Contract and renewal characteristics.
* Pricing-related behavior.

The feature importance results helped connect the machine learning output with the underlying business problem.

---

## 📉 Model Outputs

The project generates visual outputs to support model interpretation and evaluation.

### Feature Importance

`outputs/feature_importances.png`

Visualizes the relative importance of features used by the Random Forest model.

### ROC Curve

`outputs/roc_curve.png`

Provides a visual evaluation of the model's classification performance across different decision thresholds.

---

## 💼 Business Recommendations

Based on the analysis, customer retention strategies can consider:

* Monitoring customers approaching contract renewal periods.
* Identifying high-value accounts using margin-related metrics.
* Considering historical consumption behavior when assessing churn risk.
* Using customer tenure as an additional risk indicator.
* Combining pricing information with broader customer characteristics rather than relying exclusively on price sensitivity.
* Using predictive modeling to support targeted retention initiatives.

These recommendations are based on the analytical findings from the simulation dataset and should be considered within the broader business context.

---

## 📋 Project Deliverables

The completed project includes:

* Exploratory Data Analysis notebook.
* Feature Engineering notebook.
* Predictive Modeling notebook.
* Processed datasets.
* Feature importance visualization.
* ROC curve visualization.
* Executive summary presentation.
* HTML version of the executive report.

---

## 🛠️ Technology Stack

| Category                    | Technologies             |
| --------------------------- | ------------------------ |
| **Programming Language**    | Python 3.9+              |
| **Data Manipulation**       | Pandas, NumPy            |
| **Data Visualization**      | Matplotlib, Seaborn      |
| **Machine Learning**        | Scikit-Learn             |
| **Model**                   | Random Forest Classifier |
| **Development Environment** | Jupyter Notebook         |
| **Reporting**               | HTML5, CSS3, ReportLab   |
| **Version Control**         | Git / GitHub             |

---

## 📦 Python Libraries

The primary libraries used in the project include:

```text
pandas
numpy
matplotlib
seaborn
scikit-learn
jupyter
```

---

## 🚀 Setup & Execution

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/bcg-x-data-science-job-simulation.git
cd bcg-x-data-science-job-simulation
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook

```bash
jupyter notebook
```

Open the notebooks from the `notebooks/` directory and execute them in sequence.

---

## 📓 Notebook Structure

### `01_exploratory_data_analysis.ipynb`

Covers:

* Dataset inspection.
* Data quality checks.
* Missing-value analysis.
* Duplicate detection.
* Exploratory data analysis.
* Customer churn patterns.
* Pricing and consumption analysis.

### `02_feature_engineering.ipynb`

Covers:

* Creation of derived features.
* Pricing variation metrics.
* Peak/off-peak pricing differences.
* Tenure-related features.
* Preparation of variables for machine learning.

### `03_predictive_modeling.ipynb`

Covers:

* Data preparation.
* Train-test split.
* Random Forest model development.
* Model evaluation.
* Feature importance analysis.
* ROC curve analysis.

---

## 📊 Project Outcome

The project demonstrates an end-to-end data science workflow, from **business problem understanding and data exploration to feature engineering, machine learning, model evaluation, and business interpretation**.

The analysis provides evidence that churn risk should be examined using a combination of customer, consumption, margin, contract, and pricing characteristics rather than focusing exclusively on price sensitivity.

---

## 🎓 Virtual Experience

This project is completed as part of the:

**BCG X Data Science Virtual Experience Program**

The simulation provides practical exposure to applying data science techniques to a business problem involving customer churn, feature engineering, predictive modeling, and communicating analytical findings to stakeholders.

---

## 👨‍💻 Author

**Paras**

B.Sc. Computer Science Student | Aspiring Data Scientist

Areas of interest:

* Data Science
* Artificial Intelligence & Machine Learning
* Python
* SQL
* Data Analysis
* Predictive Modeling

---

## 📄 Disclaimer

This repository is created for educational and portfolio purposes based on the BCG X Data Science Virtual Experience. The analysis and conclusions presented are based on the datasets and business context provided within the simulation.
