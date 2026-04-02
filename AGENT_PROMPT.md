# Agent Prompt — CMPE 255 Student Dropout Prediction Project

## Context

You are helping complete a CMPE 255 (Data Mining) class project at San José State University. The GitHub repo `CMPE255-Student-Dropout-Prediction` is already initialized with a README, 3 starter notebooks (with TODO placeholders), a `src/utils.py` helper file, and a `requirements.txt`. Your job is to fill in all the TODO sections with complete, working, production-quality code.

## Dataset

- **Name:** Predict Students' Dropout and Academic Success
- **Source:** UCI Machine Learning Repository, id=697
- **How to load:**
  ```python
  from ucimlrepo import fetch_ucirepo
  dataset = fetch_ucirepo(id=697)
  df = pd.concat([dataset.data.features, dataset.data.targets], axis=1)
  ```
- **Shape:** 4,424 rows × 37 columns (36 features + 1 target)
- **Target column:** `Target` — three classes: `Dropout`, `Enrolled`, `Graduate`
- **Missing values:** None
- **Feature types:** Mix of integer-coded categoricals and continuous numerics
- **Key features (by importance from prior research):**
  - `Curricular units 2nd sem (approved)` — strongest predictor
  - `Curricular units 2nd sem (grade)`
  - `Curricular units 1st sem (approved)`
  - `Curricular units 1st sem (grade)`
  - `Tuition fees up to date`
  - `Scholarship holder`
  - `Age at enrollment`
  - `Debtor`
  - `Admission grade`
  - `Previous qualification (grade)`
- **Class distribution is imbalanced:** Graduate (~50%) > Dropout (~32%) > Enrolled (~18%)

## Project Structure (already exists)

```
CMPE255-Student-Dropout-Prediction/
├── README.md                          ✅ Complete
├── .gitignore                         ✅ Complete
├── requirements.txt                   ✅ Complete
├── data/raw/                          (dataset goes here)
├── notebooks/
│   ├── 01_data_preprocessing.ipynb    🔧 Has structure, TODOs need filling
│   ├── 02_eda_visualization.ipynb     🔧 Has structure, TODOs need filling
│   └── 03_modeling_evaluation.ipynb   🔧 Has structure, TODOs need filling
├── src/
│   ├── __init__.py
│   └── utils.py                       ✅ Has helper functions (plot_confusion_matrix, plot_roc_multiclass, evaluate_model, build_comparison_table)
├── results/
│   ├── figures/                       (save all PNG charts here)
│   └── tables/                        (save CSV metric tables here)
└── presentation/
```

## Your Tasks

### Task 1: Complete `01_data_preprocessing.ipynb`

The skeleton is already in place. Fill in the existing TODO cells AND add any additional cells needed. The notebook should:

1. Load the dataset via `ucimlrepo` (cell already exists — just verify it works)
2. Inspect: `.info()`, `.describe()`, null check, target distribution (cells exist)
3. Encode target: map Dropout→0, Enrolled→1, Graduate→2 (cell exists)
4. **Add:** Feature type analysis — identify which columns are truly categorical (encoded as integers) vs truly numeric. Print a summary.
5. **Add:** Check for class imbalance, print percentages, and visualize with a bar chart
6. Normalize numeric features with StandardScaler (cell exists)
7. Train/test split 80/20 with stratification and random_state=42 (cell exists)
8. Save preprocessed CSVs (cell exists — also save the original `data.csv` to `data/raw/`)

**Important conventions:**
- Use `random_state=42` everywhere for reproducibility
- Use stratified splits to preserve class ratios
- Keep a copy of the unscaled data for EDA in notebook 02

### Task 2: Complete `02_eda_visualization.ipynb`

Fill in all TODO cells with complete, polished visualizations. This notebook should produce 8-10 publication-quality charts. Use this consistent color scheme throughout:

```python
COLORS = {'Dropout': '#E24B4A', 'Enrolled': '#EF9F27', 'Graduate': '#1D9E75'}
ORDER = ['Dropout', 'Enrolled', 'Graduate']
```

Required visualizations (each should be saved to `../results/figures/`):

1. **Target class distribution** — bar chart with counts and percentages labeled on bars
2. **Correlation heatmap** — full 36×36 matrix, use `coolwarm` cmap, `center=0`, `figsize=(18,14)`, annotate=False (too many features), but highlight top correlations in text below the chart
3. **Feature distributions by target** — 2×2 subplot grid of KDE/histogram overlays for: `Curricular units 1st sem (approved)`, `Curricular units 2nd sem (approved)`, `Admission grade`, `Age at enrollment`. Each colored by target class.
4. **Boxplots** — 1×2 subplot: 1st semester grades and 2nd semester grades by target class. These will show dramatic separation.
5. **Violin plots** — `Curricular units 2nd sem (grade)` by target class
6. **Stacked bar charts** — dropout/enrolled/graduate proportions by: Scholarship holder (0/1), Debtor (0/1), Tuition fees up to date (0/1). Use a 1×3 subplot.
7. **PCA 2D scatter** — project all 36 features to 2D, scatter plot colored by target class, with explained variance in axis labels
8. **Top correlated features with target** — compute point-biserial or Spearman correlation of each feature with the encoded target, show top 15 as a horizontal bar chart

**Formatting rules:**
- `plt.rcParams['figure.dpi'] = 120` for crisp charts
- `sns.set_style('whitegrid')`
- `sns.despine()` after every plot
- Every figure gets `fig.savefig(f'../results/figures/{name}.png', dpi=150, bbox_inches='tight')`
- Titles should be descriptive: "1st Semester Approved Units by Student Outcome" not "Boxplot 1"
- Use `plt.tight_layout()` before every save

### Task 3: Complete `03_modeling_evaluation.ipynb`

This is the most important notebook — it covers the 30-point Data Mining Techniques section and the 20-point Results & Evaluation section of the rubric.

#### Part A: Classification (6 models)

For EACH model, follow this exact pattern:

```python
# 1. Initialize and train
model = SomeClassifier(random_state=42, ...)
model.fit(X_train, y_train)

# 2. Predict
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)  # needed for ROC

# 3. Evaluate
print(classification_report(y_test, y_pred, target_names=TARGET_NAMES))

# 4. Confusion matrix (3×3 heatmap)
# Use sns.heatmap with annot=True, fmt='d', cmap='Blues'

# 5. ROC curve (One-vs-Rest, 3 classes)
# Use the plot_roc_multiclass function from src/utils.py

# 6. Cross-validation
cv_scores = cross_val_score(model, X_scaled_full, y_full, cv=5, scoring='f1_macro')
print(f'5-Fold CV F1 (macro): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}')

# 7. Store results for comparison table
results[model_name] = {
    'accuracy': accuracy_score(y_test, y_pred),
    'f1_macro': f1_score(y_test, y_pred, average='macro'),
    'f1_weighted': f1_score(y_test, y_pred, average='weighted'),
    'cv_f1_mean': cv_scores.mean(),
    'cv_f1_std': cv_scores.std()
}
```

**Models to implement:**

1. **Decision Tree** — `DecisionTreeClassifier(random_state=42, max_depth=10)`. Also visualize the tree (first 4 levels) using `sklearn.tree.plot_tree` or export as text.
2. **Random Forest** — `RandomForestClassifier(n_estimators=200, random_state=42)`. Extract and plot feature importance (top 15, horizontal bar chart).
3. **KNN** — Test k=3, 5, 7, 9, 11. Plot accuracy vs k to find optimal. Use the best k for final evaluation.
4. **Logistic Regression** — `LogisticRegression(max_iter=1000, random_state=42, multi_class='multinomial')`
5. **SVM** — `SVC(kernel='rbf', probability=True, random_state=42)`
6. **XGBoost** — `XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42, eval_metric='mlogloss')`. Also extract and plot feature importance.

#### Part B: Clustering (2 methods)

1. **K-Means:**
   - Run elbow method: k=2 through k=10, plot inertia
   - Run silhouette analysis: k=2 through k=10, plot silhouette scores
   - Pick best k (likely k=3), fit final model
   - Compare cluster assignments vs actual labels using a crosstab heatmap
   - Print silhouette score

2. **Hierarchical Clustering:**
   - Compute linkage matrix (Ward method) on a random sample of ~1000 points (full dataset makes dendrograms unreadable)
   - Plot dendrogram with truncation (`truncate_mode='lastp'`, `p=30`)
   - Cut at k=3, compare to actual labels

#### Part C: Association Rules (optional but impressive)

1. Bin numeric features into categories:
   - `Admission grade`: Low (<120), Medium (120-140), High (>140)
   - `Age at enrollment`: Young (<22), Mid (22-30), Mature (>30)
   - `Curricular units 1st sem (approved)`: Low (0-2), Medium (3-5), High (>5)
2. Select ~8-10 binary/binned features, one-hot encode
3. Apply Apriori (`min_support=0.05`)
4. Generate association rules (`min_threshold=0.6` for confidence)
5. Filter for rules where the consequent involves the Target
6. Display top 10 rules by lift

#### Part D: Model Comparison

1. Build a comparison DataFrame from the `results` dict using `build_comparison_table()` from `src/utils.py`
2. Display as a styled table (highlight best values in each column)
3. Save to `../results/tables/model_comparison.csv`
4. Create a grouped bar chart comparing all models' F1 (macro) scores
5. Save chart to `../results/figures/model_comparison.png`

#### Part E: Feature Importance

1. Extract feature importance from Random Forest AND XGBoost
2. Plot side-by-side (1×2 subplot): top 15 features from each model
3. Identify features that appear in BOTH top-10 lists — these are your "key findings"
4. Save to `../results/figures/feature_importance.png`

## Global Code Quality Rules

- Every cell should run without errors in Google Colab
- Add `# !pip install ucimlrepo imbalanced-learn xgboost mlxtend` as the first cell (commented out) in each notebook for Colab users
- Use `random_state=42` everywhere
- Import `warnings` and add `warnings.filterwarnings('ignore')` at the top
- Add markdown headers between sections for readability
- Print intermediate results so the notebook tells a story when read top-to-bottom
- Save every figure to `../results/figures/` with descriptive filenames
- Save metric tables to `../results/tables/`
- Use the helper functions from `src/utils.py` where available (import with `sys.path.insert(0, '../src')` then `from utils import *`)
- At the end of notebook 03, add a "Summary" markdown cell with key takeaways

## Do NOT:

- Do not modify README.md, .gitignore, or requirements.txt
- Do not change the notebook filenames
- Do not add new notebooks — all work goes in the existing three
- Do not use deep learning / neural networks — this is a data mining course focused on classical ML
- Do not overwrite src/utils.py unless you're adding new functions (append only)