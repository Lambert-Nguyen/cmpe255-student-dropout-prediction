# Predicting Student Dropout and Academic Success

## CMPE 255 — Data Mining | Spring 2026 | San José State University

A data mining project that applies classification and clustering techniques to predict whether university students will **dropout**, remain **enrolled**, or **graduate** — enabling early intervention for at-risk students.

## Team

| Name | SJSU ID |
|------|---------|
| Lam Nguyen| 018229432 |
| Tri Ngo | 015712749 |

## Problem Statement

Higher education dropout is a significant challenge for students and institutions alike. This project uses machine learning to identify students at risk of dropping out based on enrollment-time data, demographics, socio-economic factors, and first-semester academic performance.

**Research Question:** Can we predict a student's academic outcome (Dropout / Enrolled / Graduate) early enough to enable targeted intervention?

## Dataset

**Source:** [UCI Machine Learning Repository — Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success) (ID: 697)

- **Instances:** 4,424 students
- **Features:** 36 (demographic, academic, socio-economic)
- **Target:** 3-class — Dropout, Enrolled, Graduate
- **Missing Values:** None
- **License:** CC BY 4.0

**Citation:**
> Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021). Predict Students' Dropout and Academic Success [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89.

## Project Structure

```
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   └── raw/                            # Original UCI dataset
│       └── data.csv
├── notebooks/
│   ├── 01_data_preprocessing.ipynb     # Data cleaning, encoding, normalization
│   ├── 02_eda_visualization.ipynb      # Exploratory analysis & charts
│   └── 03_modeling_evaluation.ipynb    # Classification, clustering, evaluation
├── src/
│   └── utils.py                        # Reusable helper functions
├── results/
│   ├── figures/                        # Saved charts (PNG/PDF)
│   └── tables/                         # Saved metric tables (CSV)
└── presentation/
    └── CMPE255_Project.pptx            # Final presentation slides
```

## Methods

### Data Mining Techniques

**Classification:**
- Decision Tree
- Random Forest
- K-Nearest Neighbors (KNN)
- Logistic Regression
- Support Vector Machine (SVM)
- Gradient Boosting (XGBoost)

**Clustering:**
- K-Means
- Hierarchical Clustering (Agglomerative)

**Association Rules (Exploratory):**
- Apriori algorithm on binned features

### Evaluation Metrics

- Accuracy, Precision, Recall, F1-Score (per-class and macro-averaged)
- Confusion Matrix (3×3)
- ROC-AUC (One-vs-Rest)
- Silhouette Score (clustering)
- 5-Fold Cross-Validation

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Lambert-Nguyen/cmpe255-student-dropout-prediction.git
cd CMPE255-Student-Dropout-Prediction
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the dataset

```bash
pip install ucimlrepo
```

Or download manually from [UCI](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success) and place `data.csv` in `data/raw/`.

### 4. Run the notebooks

Open in **Google Colab** or **Jupyter Notebook** and run in order:

1. `01_data_preprocessing.ipynb`
2. `02_eda_visualization.ipynb`
3. `03_modeling_evaluation.ipynb`

## Key Findings

_To be updated after analysis._

## References

1. Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021). *Predict Students' Dropout and Academic Success* [Dataset]. UCI Machine Learning Repository.
2. Martins, M.V., Tolledo, D., Machado, J., Baptista, L.M.T., & Realinho, V. (2021). Early prediction of student's performance in higher education: a case study. *Trends and Applications in Information Systems and Technologies (WorldCIST 2021)*.
