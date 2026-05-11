# Predicting Student Dropout and Academic Success

## CMPE 255 — Data Mining | Spring 2026 | San José State University

A data mining project that applies classification and clustering techniques to predict whether university students will **dropout**, remain **enrolled**, or **graduate** — enabling early intervention for at-risk students.

## Team

| Name       | SJSU ID   |
| ---------- | --------- |
| Lam Nguyen | 018229432 |
| Tri Ngo    | 015712749 |

## Problem Statement

Higher education dropout is a significant challenge for students and institutions alike. This project uses machine learning to identify students at risk of dropping out based on enrollment-time data, demographics, socio-economic factors, and first/second-semester academic performance.

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
├── LICENSE
├── .gitignore
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── data.csv                    # Original UCI dataset
│   ├── X_unscaled.csv                  # Pre-split engineered features
│   ├── X_scaled_full.csv               # Scaled full feature matrix
│   ├── X_train.csv / X_test.csv        # Train/test feature splits
│   └── y_full.csv / y_train.csv / y_test.csv
├── notebooks/
│   ├── 01_data_preprocessing.ipynb     # Cleaning, encoding, scaling, train/test split
│   ├── 02_eda_visualization.ipynb      # Exploratory analysis & charts
│   └── 03_modeling_evaluation.ipynb    # Classification, clustering, evaluation
├── src/
│   └── utils.py                        # Reusable helper functions
├── results/
│   ├── figures/                        # Saved charts (PNG)
│   └── tables/
│       └── model_comparison.csv        # Cross-model metrics
└── presentation/
    ├── Final_CMPE255_Student_Dropout_Prediction.pptx
    ├── Graphs_and_Code_Prep.md / .pdf
    ├── QA_bank.md / .pdf
    └── build_slides.py
```

## Methods

### Data Mining Techniques

**Classification:**

- Logistic Regression
- K-Nearest Neighbors (KNN)
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- Gradient Boosting (XGBoost)

**Clustering:**

- K-Means (with elbow + silhouette analysis)
- Hierarchical Clustering (Agglomerative, dendrogram)

**Dimensionality Reduction:**

- PCA (for 2-D visualization of cluster separability)

### Evaluation Metrics

- Accuracy, Precision, Recall, F1-Score (per-class and macro-averaged)
- Confusion Matrix (3×3)
- ROC-AUC (One-vs-Rest)
- Silhouette Score (clustering)
- 5-Fold Cross-Validation

## Results

Test-set performance across all classifiers (see [results/tables/model_comparison.csv](results/tables/model_comparison.csv)):

| Model               | Accuracy   | F1 (macro) | F1 (weighted) | CV F1 (mean ± std)    |
| ------------------- | ---------- | ---------- | ------------- | --------------------- |
| **Random Forest**   | **0.7706** | 0.6887     | 0.7548        | 0.6956 ± 0.0087       |
| **XGBoost**         | 0.7695     | **0.7056** | **0.7634**    | **0.7136 ± 0.0131**   |
| Logistic Regression | 0.7684     | 0.6826     | 0.7531        | 0.6782 ± 0.0089       |
| SVM                 | 0.7593     | 0.6797     | 0.7466        | 0.6798 ± 0.0220       |
| Decision Tree       | 0.7119     | 0.6346     | 0.7052        | 0.6443 ± 0.0101       |
| KNN                 | 0.6949     | 0.5860     | 0.6694        | 0.6036 ± 0.0094       |

**XGBoost** is the strongest overall, with the highest macro/weighted F1 and best cross-validated F1, indicating the most balanced performance across the three classes (notably the minority *Enrolled* class). Tree ensembles consistently outperform distance-based KNN.

Key visualizations are saved under [results/figures/](results/figures/) (confusion matrices, ROC curves, feature importance, K-Means elbow/silhouette, hierarchical dendrogram, PCA scatter).

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Lambert-Nguyen/cmpe255-student-dropout-prediction.git
cd cmpe255-student-dropout-prediction
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Get the dataset

The dataset is already included at [data/raw/data.csv](data/raw/data.csv). To re-fetch from UCI:

```python
from ucimlrepo import fetch_ucirepo
ds = fetch_ucirepo(id=697)
```

### 4. Run the notebooks

Open in **Jupyter Notebook** or **Google Colab** and run in order:

1. [notebooks/01_data_preprocessing.ipynb](notebooks/01_data_preprocessing.ipynb)
2. [notebooks/02_eda_visualization.ipynb](notebooks/02_eda_visualization.ipynb)
3. [notebooks/03_modeling_evaluation.ipynb](notebooks/03_modeling_evaluation.ipynb)

## References

1. Realinho, V., Vieira Martins, M., Machado, J., & Baptista, L. (2021). *Predict Students' Dropout and Academic Success* [Dataset]. UCI Machine Learning Repository.
2. Martins, M.V., Tolledo, D., Machado, J., Baptista, L.M.T., & Realinho, V. (2021). Early prediction of student's performance in higher education: a case study. *Trends and Applications in Information Systems and Technologies (WorldCIST 2021)*.

## License

Released under the [MIT License](LICENSE).
