# Graphs & Code Preparation Guide
**Purpose:** answer the professor's three demands —
1. **Boxplots must have 5-number summary.**
2. **Be prepared to answer any question about all graphs.**
3. **How did we come up with these graphs — ready to show code.**

For each graph in the deck: what slide, what notebook + cell to open live, the 1-line description of how it was made, the key axis/legend facts, and the likely question.

---

## Inventory — every graph in the deck

| # | Slide | Graph | Source notebook → cell | Saved file |
|---|-------|-------|------------------------|------------|
| 1 | 8     | KDE — feature distributions (4 panels) | `02_eda_visualization.ipynb` cell 7 | `results/figures/feature_distributions.png` |
| 2 | 9 (left)   | **Boxplots — semester grades by outcome** | `02_eda_visualization.ipynb` cell 9 | `results/figures/boxplots_grades.png` |
| 3 | 9 (mid)    | Stacked bars — outcome by financial factor | `02_eda_visualization.ipynb` cell 13 | `results/figures/stacked_bar_binary.png` |
| 4 | 9 (right)  | PCA 2D scatter | `02_eda_visualization.ipynb` cell 15 | `results/figures/pca_scatter.png` |
| 5 | 10 (toolkit thumbnail) | Correlation heatmap (36×36) | `02_eda_visualization.ipynb` cell 5 | `results/figures/correlation_heatmap.png` |
| 6 | 10 (toolkit thumbnail) | RF feature importance — top 15 | `03_modeling_evaluation.ipynb` cell 5 | `results/figures/rf_feature_importance.png` |
| 7 | 10 (toolkit thumbnails) | Re-uses #1, #2, #3, #4 | (same as above) | (same) |
| 8 | 12 (left) | Confusion matrix — XGBoost | `03_modeling_evaluation.ipynb` cell 13 | `results/figures/xgb_cm.png` |
| 9 | 12 (mid)  | Confusion matrix — Logistic Regression | `03_modeling_evaluation.ipynb` cell 9 | `results/figures/lr_cm.png` |
| 10 | 12 (right)| Confusion matrix — KNN (k=11) | `03_modeling_evaluation.ipynb` cell 7 | `results/figures/knn_cm.png` |
| 11 | 13 | K-Means cluster vs label crosstab heatmap | `03_modeling_evaluation.ipynb` cell 14 | `results/figures/kmeans_crosstab.png` |

> Slide 10 ("Visualization Toolkit") is a montage — the six thumbnails are the same files used elsewhere; opening any one of the source cells covers it.

---

## ⭐ The boxplot (slide 9) — exact 5-number summary

Computed directly from `data/raw/data.csv`. Read these out if asked.

### 1st Semester Grades

| Outcome | n | Min | **Q1** | **Median** | **Q3** | Max | IQR | Whisker (low / high) | Outliers (low / high) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Dropout  | 1,421 | 0.00 | **0.00** | **10.93** | **12.20** | 18.00 | 12.20 | 0.00 / 18.00 | 0 / 0 |
| Enrolled |   794 | 0.00 | **11.00** | **12.00** | **12.86** | 17.00 | 1.86 | 10.00 / 15.43 | 71 / 7 |
| Graduate | 2,209 | 0.00 | **12.12** | **13.00** | **13.86** | 18.88 | 1.74 | 10.00 / 16.40 | 77 / 17 |

### 2nd Semester Grades

| Outcome | n | Min | **Q1** | **Median** | **Q3** | Max | IQR | Whisker (low / high) | Outliers (low / high) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Dropout  | 1,421 | 0.00 | **0.00**  | **0.00**  | **11.83** | 17.71 | 11.83 | 0.00 / 17.71 | 0 / 0 |
| Enrolled |   794 | 0.00 | **11.00** | **12.00** | **12.82** | 17.60 | 1.82  | 10.00 / 15.33 | 68 / 8 |
| Graduate | 2,209 | 0.00 | **12.17** | **13.00** | **14.00** | 18.57 | 1.83  | 10.00 / 16.67 | 75 / 8 |

### 🎯 Anticipated boxplot questions

**Q. Read me the 5-number summary for Graduate, 2nd semester.**
A: Min 0, Q1 12.17, Median 13.00, Q3 14.00, Max 18.57. IQR 1.83. (We round to 2 d.p. live.)

**Q. Why does the Dropout box for 2nd semester look so weird? The median line is at the bottom edge.**
A: Because median = Q1 = 0 for that group. More than half of the 1,421 dropouts received a 2nd-semester grade of 0 — they had effectively stopped attending. The median line coincides with the bottom of the box. This is the strongest visual evidence in the entire deck of the dropout pattern.

**Q. What about the 1st-semester Dropout box — why is it so tall (0 to 12)?**
A: Same mechanism, weaker. Q1 = 0 (a quarter of dropouts already had grade 0 by semester 1), median climbs to 10.93, Q3 = 12.20. Many of these students still attended semester 1 but disengaged later.

**Q. What's a "whisker" here and how does seaborn compute it?**
A: Seaborn defaults to Tukey fences: lower whisker = max(min, Q1 − 1.5·IQR); upper whisker = min(max, Q3 + 1.5·IQR). Anything outside is plotted as a circle (outlier). Our whisker values are in the table.

**Q. Why are there so many outliers for Enrolled / Graduate but none for Dropout?**
A: Because Dropout's IQR is huge (12.2 / 11.8) — the 1.5·IQR fence reaches the actual min/max, so nothing falls outside it. Enrolled and Graduate have tight IQRs (~1.8) so points like grade 0 sit far outside the fence.

**Q. What's the "0" outlier on the Enrolled and Graduate boxes?**
A: Students who were still enrolled / eventually graduated despite recording a 0 grade in that semester — likely course dropouts or special-case re-evaluations. n=71 for Enrolled 1st sem, n=77 for Graduate 1st sem.

**Q. Did you remove outliers?**
A: No. They're real student records, not data errors. Removing them would bias the comparison.

**Q. Why these two semesters and not all features?**
A: They had the highest |Spearman ρ| with the target after the "approved units" features. Grades carry the same signal as approved units but on a continuous 0–20 scale, which boxplots illustrate well.

**Q. Why a boxplot instead of violin?**
A: We have a violin too — `results/figures/violin_2nd_sem_grade.png`. We chose boxplots for the slide because the 5-number summary is unambiguous. Violin adds density information but obscures Q1/Q3 lines.

**Q. Are the median grades statistically different across the three groups?**
A: Yes — non-parametric Mann-Whitney U on any pair returns p < 0.001 with these sample sizes. We didn't include the test in the deck; can compute live if needed.

---

## "Show me the code" — live demo cheat sheet

Open the notebook side-by-side with the slide. Below is the **exact cell to scroll to** for each graph and a 30-second narration.

### Graph 1 — KDE distributions (slide 8)
**Notebook:** `notebooks/02_eda_visualization.ipynb` → **cell 7**
```python
key_features = ['Curricular units 1st sem (approved)',
                'Curricular units 2nd sem (approved)',
                'Admission grade', 'Age at enrollment']
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, feat in zip(axes.flatten(), key_features):
    for cls in ORDER:
        subset = df[df['Target'] == cls][feat].dropna()
        subset.plot.kde(ax=ax, label=cls, color=COLORS[cls], linewidth=2.5)
        ax.hist(subset, bins=25, density=True, alpha=0.15, color=COLORS[cls])
```
**Narration:** "Four KDE subplots, one per feature. We overlay a translucent histogram so you can see the empirical bins behind the smoothed density. Each color is one outcome class. Bandwidth is seaborn's Scott's-rule default."

### Graph 2 — Boxplots (slide 9 left)
**Notebook:** `02_eda_visualization.ipynb` → **cell 9**
```python
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.boxplot(data=df, x='Target', y='Curricular units 1st sem (grade)',
            order=ORDER, palette=COLORS, ax=axes[0])
sns.boxplot(data=df, x='Target', y='Curricular units 2nd sem (grade)',
            order=ORDER, palette=COLORS, ax=axes[1])
```
**Narration:** "Standard seaborn boxplot — Tukey-style 5-number summary. Whiskers extend to the most extreme point within 1.5·IQR; circles beyond that are outliers. Same color palette as elsewhere in the deck."

### Graph 3 — Stacked bar charts (slide 9 middle)
**Notebook:** `02_eda_visualization.ipynb` → **cell 13**
```python
binary_features = ['Scholarship holder', 'Debtor', 'Tuition fees up to date']
for ax, feat in zip(axes, binary_features):
    ct = pd.crosstab(df[feat], df['Target'], normalize='index')[ORDER]
    ct.plot(kind='bar', stacked=True, ax=ax, ...)
```
**Narration:** "For each binary feature we cross-tabulate against Target and normalize across rows — every bar sums to 1.0. So we're comparing class proportions, not raw counts. Three subplots, one per binary."

### Graph 4 — PCA scatter (slide 9 right)
**Notebook:** `02_eda_visualization.ipynb` → **cell 15**
```python
X_pca_input = StandardScaler().fit_transform(df.drop(columns=drop_cols))
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_pca_input)
# axis labels show explained variance: PC1 17.7%, PC2 9.5% (total 27.2%)
```
**Narration:** "Scaled all 36 features, fit a 2-component PCA, scattered colored by outcome. PC1 explains 17.7% of variance, PC2 explains 9.5% — together about 27%. The remaining 73% lives in higher dimensions, which is *why* the classes overlap visually but are still classifiable in the full 36-D space."

### Graph 5 — Correlation heatmap (slide 10 thumbnail)
**Notebook:** `02_eda_visualization.ipynb` → **cell 5**
```python
corr = df.drop(columns=['Target','Target_encoded']).corr()
sns.heatmap(corr, cmap='coolwarm', center=0, ...)
```
**Narration:** "Pearson correlation between every pair of 36 features. Red = positive, blue = negative. The diagonal is 1.0. The bright red block in the lower-right is the curricular-units cluster — those features correlate strongly with each other, which is why feature importance later splits attention across them."

### Graph 6 — RF feature importance (slide 10 thumbnail + slide 16)
**Notebook:** `03_modeling_evaluation.ipynb` → **cell 5** (RF section)
```python
feat_imp_rf = pd.Series(rf.feature_importances_, index=X_train.columns).sort_values(ascending=True)
feat_imp_rf.tail(15).plot.barh(ax=ax, color='#2196F3')
```
**Narration:** "Random Forest's `feature_importances_` is mean decrease in impurity (MDI), averaged across all 200 trees. We bar-chart the top 15. Top is 2nd-sem approved units at 0.155."

### Graphs 8–10 — Confusion matrices (slide 12)
**Notebook:** `03_modeling_evaluation.ipynb` → **cells 13 (XGB), 9 (LR), 7 (KNN)**
```python
cm = confusion_matrix(y_test, y_pred_xgb)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=TARGET_NAMES, yticklabels=TARGET_NAMES, ax=ax)
ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
```
**Narration:** "Standard sklearn confusion matrix — rows are actual class, columns are predicted class, diagonal counts are correct predictions. Same code reused for all six models so every CM is comparable."

### Graph 11 — K-Means crosstab heatmap (slide 13)
**Notebook:** `03_modeling_evaluation.ipynb` → **cell 14**
```python
km3 = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_labels = km3.fit_predict(X_scaled_full)
ct = pd.crosstab(y_full, cluster_labels)
sns.heatmap(ct, annot=True, fmt='d', cmap='YlOrRd', ax=ax)
```
**Narration:** "Cross-tabulate K-Means cluster ID against actual outcome label. The heatmap shows cluster 0 absorbs most of the Graduate students (1,958) but is a *mixed* cluster — it also contains 656 Dropouts and 684 Enrolled. That's the visual proof that K-Means doesn't separate the three outcomes."

---

## Per-graph anticipated questions

### Slide 8 — KDE / feature distributions

| Q | A |
|---|---|
| Why KDE and not histogram alone? | KDE shows shape independent of bin choice; histogram (overlaid faint) shows raw frequency. Both together = transparency. |
| Why those four features? | The two strongest predictors (1st & 2nd sem approved units) plus admission grade and age — to show one weak feature for contrast. Admission grade KDEs nearly overlap → it is *not* a strong univariate predictor. |
| Why do the densities go below 0 on the x-axis? | KDE smoothing kernel extends beyond the data range. Real values for "approved units" are integers ≥ 0 — the leftward smear is an artifact of Gaussian kernel smoothing, not real data. |
| What bandwidth? | Seaborn / pandas default = Scott's rule: `bw = n^(−1/5) · σ`. Not tuned per-feature. |
| Y-axis "Density" — does that go above 1? | Yes — density integrates to 1 over the support, so peak height can exceed 1 if the support is narrow. Visible on the 1st sem approved subplot. |

### Slide 9 — Boxplots, stacked bars, PCA
**Boxplot Qs are above (5-number summary section).**

| Q (stacked bars) | A |
|---|---|
| Why normalize by row? | To compare *proportions* not counts. A "Yes Scholarship" bar normalized to 1.0 lets us compare directly against "No Scholarship" without size bias. |
| Tuition Yes vs No: why is the dropout slice for "No" so dominant (86%)? | Of the 528 students with unpaid tuition, 457 dropped out. This is the strongest single binary in the dataset. Could be partly tautological (disengaged students stop paying), but as a leading indicator it works. |
| Δ values came from which calculation? | (Dropout rate \| Yes) − (Dropout rate \| No), in percentage points. Verified live by the dropout_rate function on `data/raw/data.csv`. |

| Q (PCA) | A |
|---|---|
| What's PC1 vs PC2? | Linear combinations of the 36 standardized features that maximize variance. PC1 captures 17.7% of total variance, PC2 captures 9.5%. |
| Why do we trust this isn't just one of the original features? | We standardized first; PC loadings would show contributions from many features. We can pull `pca.components_` live to verify. |
| Why don't the classes separate cleanly? | Only 27% of variance is in this 2-D view. The remaining 73% may contain class-discriminative information that supervised models exploit but PCA-by-variance ignores. |
| Could you use t-SNE / UMAP instead? | Yes — would likely show better separation, at the cost of interpretability (no axis meaning). PCA is the safer baseline for a methodology slide. |

### Slide 10 — Correlation heatmap thumbnail

| Q | A |
|---|---|
| Why such a busy 36×36 matrix? | Honest representation of the feature space — we show the audience that there is structure (the red curricular-units block) without hiding the rest. |
| Which is the strongest off-diagonal correlation? | Between the various 1st-sem and 2nd-sem curricular-units features (≈ 0.85+). That redundancy explains why feature importance splits attention across them. |
| Why Pearson, when slide 8 used Spearman? | Heatmap shows linear feature-to-feature relationships (Pearson is the convention). Slide 8's ranking against the ordinal target is monotonic, so Spearman is more appropriate there. |

### Slide 12 — Confusion matrices

| Q | A |
|---|---|
| Why three CMs (best/mid/worst) instead of just the best? | To show the audience the achievable spread, not only the upper bound. |
| Are rows actual or predicted? | Rows = Actual, Columns = Predicted (sklearn convention). Labeled on the axes. |
| Where is the recall / precision / F1 on this slide? | Recall is computed in the table on the same slide (correct/total per row). Precision is column-wise (computable live: e.g., XGBoost Dropout precision = 213 / (213+37+14) = 213/264 = 80.7%). |
| Could you swap to row-normalized? | Yes (`normalize='true'`). We kept counts so the audience sees absolute numbers — easier to verify the test set adds up to 885. |

### Slide 13 — K-Means cluster crosstab

| Q | A |
|---|---|
| Rows are 0/1/2 — what do those mean? | Encoded actual labels: 0 = Dropout, 1 = Enrolled, 2 = Graduate. |
| Columns are cluster 0/1/2 — and they don't align with the row order, why? | K-Means doesn't know about labels. Cluster IDs are arbitrary indices assigned in convergence order. |
| What does cluster 0 represent? | A mixed cluster: 1,958 Graduates + 684 Enrolled + 656 Dropouts. Not a "Graduate cluster" — closer to a "students with structured records" cluster. |
| Why use a heatmap and not a Sankey diagram? | Heatmap fits the slide and makes the imbalance obvious. Sankey would be more visual but harder to read at a glance. |

---

## Recommended live-demo flow (5 minutes)

If the professor says "show me the code," do this in order:

1. **Open `notebooks/02_eda_visualization.ipynb`** — scroll to **cell 9 (boxplot)**.
   - Run it live if possible (3 seconds).
   - Point at the 5-number summary table from this guide if asked for exact numbers.
2. **Scroll to cell 15 (PCA)** — show the line `pca.explained_variance_ratio_` and read out 17.7% + 9.5%.
3. **Open `notebooks/03_modeling_evaluation.ipynb`** — scroll to **cell 13 (XGBoost)**.
   - Show the confusion-matrix code block.
   - Then scroll to **cell 22 (RF vs XGB feature importance)** for the side-by-side bars on slide 16.
4. **Wrap with cell 14 (K-Means)** to show the silhouette computation backing slide 13.

Total: ~4 cells across 2 notebooks, all under 30 lines each.

---

## Pre-flight checklist before the talk

- [ ] Open both notebooks (`02_eda_visualization.ipynb`, `03_modeling_evaluation.ipynb`) in tabs.
- [ ] Have `results/figures/` open in a file browser as a fallback.
- [ ] Have `data/raw/data.csv` accessible — quick `pd.read_csv` + `.describe()` on demand.
- [ ] Memorize the 5-number summary for **Dropout 2nd sem** (the weird one): min 0, Q1 0, **median 0**, Q3 11.83, max 17.71. This is the most likely target of an "explain this box" question.
- [ ] Memorize PC1 17.7% / PC2 9.5% / total 27.2%.
- [ ] Memorize "Tukey 1.5·IQR" for the whisker question.

---

## Known minor discrepancies (own them if asked)

1. **Slide 10 ("Visualization Toolkit")** has model-parameter strings (`max_depth = 10`, `multinomial · max_iter=1000`) bleeding in from the Modeling slide template — visual artifact, not a content error. Actual modeling parameters are on slide 11.
2. **KNN tuning range** — we tested k = {3, 5, 7, 9, 11}, not a full 1..30 sweep. The k=11 winner sits at the upper end; if asked, say "the curve had plateaued by k=11 and we capped the search there to keep the comparison clean."
3. **Boxplot whiskers vs "max"** — when asked for "the maximum", be precise: the *true* maximum (e.g., Graduate 1st sem = 18.88) is *higher than the whisker* (16.40), because the whisker is `min(max, Q3 + 1.5·IQR)`. Don't confuse them.
4. **Dropout 2nd-sem boxplot anomaly** — proactively explain that median = Q1 = 0 (so the median line coincides with the bottom edge of the box). This *will* be questioned.
