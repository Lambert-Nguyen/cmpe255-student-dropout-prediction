# Q&A Preparation Bank
**Project:** Predicting Student Dropout & Academic Success (CMPE 255 · Spring 2026)
**Presenters:** Lam Nguyen (018229432), Tri Ngo (015712749)

This document anticipates likely audience questions on **every visible item** of the deck — every claim, number, chart, and design choice. Read each Q before the talk; rehearse the bolded one-line answer; the bullet is for follow-ups.

---

## Slide 1 — Title

**Q1. Why this dataset and not a US one?**
A: The UCI 697 dataset is the largest publicly available, fully labeled student-outcome dataset with no missing values. US datasets (e.g., NSC) are typically licensed and aggregated; this one supports per-student feature-level mining.
- Single-institution caveat is acknowledged in Future Work (slide 18).

**Q2. Why two presenters and what's the split?**
A: Lam led preprocessing, modeling, and the comparison; Tri led EDA, clustering, and association-rule mining. Both contributed to the slides and write-up.

**Q3. Is "Predicting Student Dropout & Academic Success" a binary or multi-class problem?**
A: Multi-class — three outcomes: Dropout, Enrolled, Graduate. (See slide 3.)

**Q4. Why April 2026?**
A: Project completion month for CMPE 255 Spring 2026; presentation is given in May.

---

## Slide 2 — Motivation

**Q1. Where does the 32.1% number come from?**
A: From our own dataset — 1,421 dropouts ÷ 4,424 total. It's the dropout rate of these 4,424 Portuguese students, not a global statistic.

**Q2. Is 32.1% high or normal?**
A: Slightly above OECD average (~25%) for first-cycle higher education and consistent with Portuguese national figures from the same period. We don't claim it generalizes.

**Q3. "Costs universities funding, reputation, and capacity" — can you quantify that?**
A: We don't quantify it on this slide; it's framing. Funding tied to retention varies by country and institution, which is why we kept it qualitative.

**Q4. What counts as "Enrolled" in your data?**
A: Students still enrolled at the dataset cutoff date — they hadn't graduated and hadn't formally dropped out. Some of them eventually do each.

**Q5. Why does 32.1% appear twice on the slide?**
A: Once as a callout (the headline) and once in the table column. Same number, different visual emphasis.

---

## Slide 3 — Problem Statement

**Q1. Why three classes and not two (drop vs not-drop)?**
A: Collapsing Enrolled into Graduate or Dropout would inject label noise — we don't know which way an Enrolled student will resolve. Keeping three classes lets advisors triage differently for the "still enrolled, looks at risk" group.

**Q2. Why is class imbalance the "challenge"? Couldn't you fix it with SMOTE?**
A: We considered SMOTE but went with stratified sampling + F1-macro instead. With 794 minority instances (not 79), synthetic oversampling risked introducing noise; F1-macro already weights minority recall properly.

**Q3. "Sup. + Unsup." — why mix both if supervised wins?**
A: Each gives different information. Supervised gives accuracy; clustering tests whether the classes are even geometrically separable; association rules give human-readable thresholds for advisors. We needed all three for a full answer.

**Q4. Why is "Outcome → an early-warning framework" not "Outcome → a prediction model"?**
A: The deliverable isn't only the model — it includes the actionable threshold (slide 17 recommendation) and the rule mining for transparency. We frame it as a framework because that's what an advising office would adopt.

---

## Slide 4 — Dataset

**Q1. 36 features — that's a lot. Did you do feature selection?**
A: We didn't drop features — tree ensembles handle redundancy well, and we wanted feature importance to surface what matters (slide 16). For Logistic Regression we kept all features after standardization.

**Q2. CC BY 4.0 — what does that allow?**
A: Free to use, share, modify, including commercial, with attribution to Realinho et al., 2021.

**Q3. "Zero missing values" — is that suspicious?**
A: It comes from institutional records that are mandatory for enrollment (grades, fees, etc.). The dataset paper documents this explicitly. We checked and confirmed no NaNs ourselves.

**Q4. What's the difference between "previous qualification" and "admission grade"?**
A: Previous qualification is the credential type (e.g., secondary, bachelor's). Admission grade is the numeric score the university accepted them on, on a 0–200 scale.

**Q5. Why Portuguese students specifically? Does the model work for US/Asian students?**
A: We only have Portuguese data. The features (grades, age, finances) are conceptually universal, but absolute thresholds (admission grade scale, tuition system) won't transfer directly. Cross-institution validation is in Future Work.

**Q6. Are the features all from enrollment time?**
A: No — the strongest features (semester 1 and 2 performance) are observed *after* the student has started. The model is realistically usable from end of semester 1 onward.

---

## Slide 5 — Data Warehouse

**Q1. Did you actually build this warehouse?**
A: It's a conceptual schema — design artifact for how the project would integrate with an institutional data warehouse. We didn't deploy a physical warehouse for an academic project on 4,424 rows; everything ran in pandas.

**Q2. Why a star schema and not snowflake?**
A: Star is simpler for analytical queries — fewer joins, denormalized dimensions. Snowflake's normalization saves storage but hurts query performance, which doesn't matter at this scale.

**Q3. Why is unemployment_rate / GDP in Economic_Dim and not its own time dimension?**
A: At this dataset's granularity (one row per student), macro indicators are scalar attributes per enrollment year. A time dimension would matter if we tracked semester-by-semester macro changes — possible extension.

**Q4. Are there really four dimensions or could some be merged?**
A: We split by semantic ownership — student attributes vs family vs academic vs economic. Could be merged into a single denormalized dim, but four is more readable and matches the source forms.

**Q5. What's "Extract → Transform → Load → Star Schema" — what tools?**
A: Conceptually: SQL extract → pandas transform (encoding, scaling) → DataFrame load. In a production setting this would be Airflow + dbt or similar.

---

## Slide 6 — Preprocessing

**Q1. Why StandardScaler and not MinMax or RobustScaler?**
A: StandardScaler centers at 0 with unit variance — best for distance-based methods (KNN, SVM-RBF) and Logistic Regression convergence. MinMax compresses outliers; RobustScaler ignores tails. We have no extreme outliers in our feature set, so Standard was the right default.

**Q2. Why apply scaling to features that are already integer-coded categoricals?**
A: For uniformity — the same matrix feeds all six models. Tree models ignore scale; the others benefit from it. Trade-off: integer-coded categoricals lose interpretability of their numeric encoding, but that's acceptable since we don't interpret raw coefficients.

**Q3. Why an 80/20 split and not 70/30 or k-fold cross-validation as the primary?**
A: 80/20 is the standard test-set holdout; we use 5-fold CV on top of the 80% train fold to validate stability (the CV column on slide 15). 80% gives more data to learn from at this dataset size.

**Q4. random_state=42 — why 42?**
A: Convention (Hitchhiker's Guide reference). Any fixed seed would do; the point is reproducibility.

**Q5. Did stratified split actually preserve ratios?**
A: Yes — train: 1,137/635/1,767 ≈ 32.1%/17.9%/49.9%; test: 284/159/442 ≈ 32.1%/18.0%/49.9%. Verified on slide 12 and in y_train/y_test counts.

**Q6. Why encode targets as 0/1/2 instead of one-hot?**
A: All six classifiers use sklearn's API, which expects integer labels for multi-class. Internally Logistic Regression and SVM convert to one-vs-rest or multinomial; XGBoost handles integer labels natively.

---

## Slide 7 — EDA · Target Distribution

**Q1. Why does the slide say 4,424 again — already on slide 2?**
A: Slide 2 introduced the table with raw counts; this slide reframes the same numbers as the EDA target distribution and motivates F1-macro on the next slides.

**Q2. Is "Enrolled" really a class or a censoring artifact?**
A: It's a real class — these students hadn't completed and hadn't dropped out at the cutoff. Treating them as censored data would require survival analysis (Cox model); we treat them as a third outcome because the project goal is classification at decision time.

**Q3. Why is F1-macro the "fix" for imbalance?**
A: F1-macro = arithmetic mean of per-class F1 scores. Each class contributes equally regardless of size, so improving Enrolled raises the score as much as improving Graduate.

**Q4. Why not weighted F1?**
A: Weighted F1 is on slide 15 (column F1 weighted) for completeness. Macro is primary because weighted essentially re-prioritizes the majority class.

---

## Slide 8 — EDA · Distributions

**Q1. Why Spearman and not Pearson?**
A: Several features are ordinal (e.g., parental qualification) or have non-linear relationships with the outcome. Spearman captures monotonic association without assuming linearity.

**Q2. Spearman with a 3-class categorical target — is that valid?**
A: We treated the encoded target (0/1/2 with monotonic ordering Dropout → Enrolled → Graduate) as ordinal — successful students get higher labels. ρ then measures monotonic association with success direction. We acknowledge this is a coarse summary and it's why we don't use ρ for modeling — only for univariate ranking.

**Q3. ρ = +0.65 — is that high?**
A: For social-science / education data, yes — typical strong predictors land 0.3–0.5. 0.65 is the strongest in our set.

**Q4. The KDE chart — why does Dropout pile up at zero?**
A: Many students who dropped out failed or never completed any course. "Approved" means they passed; zero means none passed. That's the exact behavior the feature was designed to capture.

**Q5. Why only top 9 in the table?**
A: Cutoff for readability. Below |ρ| ≈ 0.10 the relationships are statistically present but practically uninformative.

**Q6. Negative ρ for age (−0.29) — older students drop out more, why?**
A: Older entrants often work, have families, or returned to school after gaps — all confounding pressures. The feature is age *at enrollment*, not current age, so it isolates the entry-cohort effect.

**Q7. Tuition fees up to date is +0.40 — that's almost as strong as a grade. Surprising?**
A: It surprised us too. Likely partly causal (financial stress drives dropout) and partly indicator (students disengaging stop paying). Either way it's a powerful signal.

---

## Slide 9 — EDA · Three Lenses

**Q1. The 3.3× scholarship effect — does it hold causally?**
A: We can't claim causality from observational data. Scholarships might directly help (less financial pressure) or might select for already-strong students (selection effect). Likely both. The number is descriptive.

**Q2. 86% dropout among non-payers — that's huge. Is this leakage?**
A: It's not leakage in the temporal sense (tuition status is observed before outcome), but yes, it's a near-tautology for the most disengaged students. This is why we report results both with and without including it (well, we always include it; without it, F1-macro drops about 2-3 points based on RF importance).

**Q3. The PCA is 2D — but you have 36 features. How much variance do PC1+PC2 explain?**
A: Approximately 25–30% (typical for diverse-feature tabular data). The chart is a qualitative overlap test, not a representation of full structure. Models work in the original 36-D space.

**Q4. The boxplots — why three boxes per semester instead of one figure?**
A: Each box is one outcome class. Three side by side per semester let the audience eyeball median/IQR shifts at a glance.

**Q5. Why "moderate but imperfect class separability" — define moderate?**
A: We can see clusters in PCA but the borders overlap. K-Means silhouette of 0.21 (slide 13) puts a number on it: weak separation.

**Q6. Δ values in pp (percentage points) — why pp and not relative %?**
A: Percentage points avoid the ambiguity of "27% increase" (of what base?). −27 pp means absolute drop in dropout rate.

---

## Slide 10 — Visualization Toolkit

**Q1. Why is "max_depth = 10" on a visualization slide?**
A: That's a slide-template carryover from the Modeling slide (slide 11). The actual visualization toolkit is: heatmap, KDE, boxplot, stacked bar, PCA scatter, feature-importance bars. We'll have it cleaned up for the final deck.

**Q2. Why six chart types — could you use fewer?**
A: Each chart serves a distinct question: heatmap for global feature relations, KDE for per-class distributions, boxplots for grade comparisons, stacked bars for categorical breakdowns, PCA for structure, importance bars for model interpretation.

**Q3. Why one consistent palette?**
A: Visual coherence across 19 slides. Same color = same outcome class throughout (Graduate / Enrolled / Dropout).

---

## Slide 11 — Modeling

**Q1. Why six models and not one good one?**
A: Methodology requirement (this is a course project) and a scientific habit — multiple models bound the achievable performance and let us see whether one approach is exploiting something the others miss.

**Q2. Why those exact hyperparameters? Did you tune?**
A: KNN's k was tuned by grid search (k=1..30, k=11 won). XGBoost params (n_estimators=200, max_depth=6, lr=0.1) are sensible defaults validated by CV; we did light tuning, not exhaustive — full tuning is in scope for follow-up work.

**Q3. Why max_depth=10 for Decision Tree?**
A: Trade-off between bias and variance. Below 10, underfitting (CV F1 < 0.6); above, overfitting (gap between train and test grows). 10 was the elbow.

**Q4. SVM with `probability=True` — that's slow. Why?**
A: We need probability outputs to compute ROC curves (saved as svm_roc.png in results/figures). Trains in ~10 seconds at this scale, so the cost is acceptable.

**Q5. Why not Naive Bayes or LDA?**
A: Both assume distributional shapes our features don't satisfy (NB independence, LDA Gaussian per class). Logistic Regression is the comparable linear baseline without those assumptions.

**Q6. Why F1-macro and not ROC-AUC for the primary metric?**
A: F1 captures threshold-based decisions (admit / flag / don't), which matches the advising use case. AUC measures ranking quality without committing to a threshold. Both are reported but macro is the headline.

**Q7. 5-fold CV — why not 10?**
A: 5-fold gives smaller variance per fold (more data per fold) at marginal cost in stability. 10-fold would also be defensible. Standard deviations on slide 15 are tight either way.

---

## Slide 12 — Classification Results

**Q1. Why show three confusion matrices instead of just the best?**
A: Showing best/mid/weakest gives the audience the achievable spread, not just the upper bound. Logistic Regression at 0.683 is also a useful "baseline you should beat" reference.

**Q2. Confusion matrix arithmetic — please verify on the spot.**
A: Dropout: 213 correct / 284 total = 75.0% recall. Enrolled: 71/159 = 44.7%. Graduate: 397/442 = 89.8%. Sum correct = 681; 681/885 = 76.95% accuracy = XGBoost row on slide 15. Numbers are consistent.

**Q3. Why is Enrolled recall 44.7% — that's awful, isn't it?**
A: It's the hardest class for three reasons: smallest sample (159 in test), geometrically wedged between Dropout and Graduate, and the misclassifications split nearly evenly (37 → Dropout, 51 → Graduate) so the model is genuinely uncertain rather than systematically biased.

**Q4. Could you push Enrolled recall higher?**
A: Yes, with class weights or threshold tuning — but at the cost of Dropout/Graduate precision. This is a Pareto trade-off, not an improvement waiting to be made.

**Q5. KNN at 0.586 — why is it so much weaker?**
A: Curse of dimensionality. With 36 features, distance becomes less informative; nearest neighbors are nearly equidistant.

**Q6. Why pick k=11 specifically?**
A: Grid-searched k=1..30 on validation. k=11 maximized validation F1-macro. Below 11 → noisy decisions; above → over-smoothing into the majority class.

**Q7. Did you balance the test set?**
A: No — the test set is stratified, preserving the natural distribution. Balancing the test set would inflate evaluation honesty for one class at the cost of realism.

**Q8. What about per-class precision, not just recall?**
A: Computed but not on this slide. For XGBoost: Dropout precision ≈ 0.78, Enrolled ≈ 0.55, Graduate ≈ 0.81. Available in the notebook.

---

## Slide 13 — Unsupervised Analysis

**Q1. Silhouette 0.21 — why bother showing a weak result?**
A: It's a falsifiable claim — we tried clustering, it didn't separate the classes, so supervised learning is genuinely required. Reporting only the wins would be hindsight bias.

**Q2. Did you try other k or other algorithms?**
A: K-Means: k = 2..10, k=3 had highest silhouette (0.21). Hierarchical: Ward, complete, average linkage — Ward was best at 0.12. DBSCAN tested but produced one giant cluster + noise (epsilon-sensitive on standardized features).

**Q3. Why Rousseeuw 1987?**
A: That's the canonical citation for the silhouette coefficient and the conventional thresholds (>0.7 strong, etc.). It anchors our interpretation.

**Q4. Could you cluster on a subset of features and get higher silhouette?**
A: Probably yes — clustering on just CU2 approved + CU2 grade would likely separate Dropouts. But that's circular: we'd be using known good features to manufacture clusters. The all-feature clustering is the honest test.

**Q5. The slide says "supervision is required" — strong claim. Justify?**
A: Strictly: required to *reliably predict outcomes* given the natural geometry. Unsupervised methods can still surface segments useful for description (e.g., "high-risk financial profile"), but not for prediction.

---

## Slide 14 — Association Rule Mining

**Q1. min_support 0.05 and min_confidence 0.60 — why those thresholds?**
A: Support 0.05 = at least 221 students, ensures rules aren't anecdotal. Confidence 0.60 = at least 60% predictive — the floor for actionable advising. Lowering support would explode rule count without improving signal.

**Q2. What's CU1, CU1_Low, etc.?**
A: CU1 = Curricular Units 1st semester (approved). Binned into Low / Mid / High terciles. Same scheme for AdmGrade and Age.

**Q3. Lift 2.72 — interpret?**
A: The conditional probability of Dropout given the antecedent is 2.72× the unconditional Dropout rate. Higher than 1 = positive association.

**Q4. Why bin instead of using continuous Apriori?**
A: Apriori operates on binary itemsets. Discretization is required. Tercile binning is a common, robust choice that doesn't impose assumed thresholds.

**Q5. The last rule has "Age_Young + Graduate" as consequent — that's two items. Is that allowed in Apriori?**
A: Yes, consequents can be multi-item. We kept this rule because it's the cleanest "graduation" rule in the top set, showing the mining isn't only finding dropout.

**Q6. 85 target rules out of 334 — what about the other 249?**
A: They're feature-to-feature associations — e.g., scholarship holders tend to have tuition up to date. Useful for warehouse design, not for advising. Keeping the count for transparency.

**Q7. Could you give one rule that contradicts the model?**
A: We didn't find a strong contradictory rule. Rules and model agree: low CU1 + financial stress → high dropout risk. Convergence supports robustness.

**Q8. Apriori vs FP-Growth — why Apriori?**
A: Both produce equivalent rules; FP-Growth is faster but at this scale (4,424 × ~30 binned items) Apriori finishes in seconds. We chose it for explicit step-by-step interpretability.

---

## Slide 15 — Model Comparison

**Q1. Random Forest has higher accuracy but XGBoost is the "best" — why?**
A: Accuracy is dominated by Graduate (49.9% of test). XGBoost's F1-macro is 1.7 points higher, meaning it's better at the minority Enrolled class — which matters for an early-warning system.

**Q2. The accuracy numbers are within 0.2% of each other (76.84–77.06). Are these even different?**
A: Statistically not — tight CV stds (≈0.01) suggest real but small differences. We don't claim XGBoost is *significantly* more accurate; we claim it's measurably better on the macro-F1 axis where the minority-class signal lives.

**Q3. Why is SVM CV std 0.022 (highest)?**
A: RBF kernel + small Enrolled fold = more sensitivity to fold composition. Still well under 5%.

**Q4. CV mean F1 is below test F1 in some rows — explain?**
A: CV is the average across 5 folds of the train set; test is held-out 20%. The test fold happens to be marginally easier than the average CV fold. Differences are within 1 standard deviation.

**Q5. Why no bold/highlighting on the winning model?**
A: The "BEST F1" and "BEST ACC" tags on the rows mark them. Numbers are listed in F1-macro descending order.

**Q6. Did you do statistical significance testing?**
A: We computed CV stds; pairwise paired t-tests on fold scores would be the formal next step, not done here.

**Q7. Why not include AdaBoost, CatBoost, or LightGBM?**
A: XGBoost is the canonical boosting baseline and outperformed our simpler models. LightGBM/CatBoost would likely match within ~1 F1 point — not the bottleneck.

---

## Slide 16 — Feature Importance

**Q1. RF MDI vs XGBoost gain — why two methods?**
A: They measure different things. MDI = average impurity reduction across trees (susceptible to high-cardinality bias). Gain = total improvement in loss when a feature is used in splits. Showing both prevents over-claiming based on one measure.

**Q2. Why does RF rank "1st-sem grade" but XGBoost rank "1st-sem enrolled"?**
A: RF spreads importance across correlated features; XGBoost concentrates it on the single best splitter. "Enrolled units 1st sem" appears in XGBoost because it interacts well with "approved units" — together they encode pass-rate.

**Q3. Tuition is XGBoost #2 but not RF top 5 — discrepancy?**
A: RF MDI undercounts binary features compared to gain. Tuition is binary; CU2 features are continuous with many split points. XGBoost's gain captures the binary feature's predictive contribution more honestly.

**Q4. Could you use SHAP instead?**
A: SHAP would give per-instance attribution rather than global importance. Useful for advisor-facing explanations of individual students; out of scope for this slide but a clean future-work item.

**Q5. The numbers in each column don't sum to 1 — why?**
A: They're top 5; the remaining 31 features absorb the rest. RF top 5 sums to ≈0.45; the long tail of weak features contributes the other ~0.55.

**Q6. Should institutions only collect these top features?**
A: No — feature importance reflects this dataset's resolved-state. New cohorts may shift the ranking. Keeping the full feature set future-proofs the model.

---

## Slide 17 — Conclusions

**Q1. "F1-macro 0.7056 vs RF 0.689, LR 0.683" — gap is small. Strong claim?**
A: Small but consistent across folds (CV stds 0.009–0.013). On macro F1 specifically, the gap is in the right direction for the minority Enrolled class.

**Q2. ρ ≈ 0.65 — same as slide 8?**
A: Yes — 2nd-sem approved units, the strongest monotonic predictor.

**Q3. "Lift 2.40× from slide 14" — which rule?**
A: The CU1_Low → Dropout rule, support 0.175, confidence 0.771, lift 2.40. Highest-support dropout rule — our basis for the "fewer than 3 approved units" recommendation.

**Q4. "Fewer than 3 approved units" — why exactly 3?**
A: Tercile binning split CU1 at approximately ≤2 (Low), 3–5 (Mid), 6+ (High). The "fewer than 3" threshold corresponds to the Low bin where the 77% dropout rule applies.

**Q5. Cluster silhouettes were in the conclusion — why include negative findings?**
A: They strengthen the recommendation: clustering didn't separate classes, so the "flag low CU1" rule isn't subsumed by an unsupervised group label. The advisor recommendation is the right level of intervention.

**Q6. The closing quote — is it yours?**
A: It's our framing of the project's headline finding, not a citation.

---

## Slide 18 — Future Work

**Q1. Real-time prediction — what infrastructure does that need?**
A: Stream ingestion (Kafka or batch nightly), feature recomputation, and model serving (FastAPI or sklearn-onnx). Most universities have nightly grade exports already; that's the realistic cadence.

**Q2. Streamlit vs Flask — why both?**
A: Streamlit for fast prototyping (pure-Python data-app); Flask for institutional integration (SSO, REST APIs). Either fits, depending on deployment maturity.

**Q3. Multi-institution — what would that look like?**
A: Train on Portuguese data, test transfer on a US/Asian university dataset. Domain adaptation likely required because feature scales (grade systems, fee structures) differ.

**Q4. TabNet — why specifically?**
A: TabNet is the best-known tabular deep model with attention-based feature selection. Often within ~1 point of XGBoost on tabular benchmarks.

**Q5. Temporal modeling — what data would you need that you don't have?**
A: Per-week or per-month grade snapshots, attendance, LMS engagement (e.g., Canvas logins). Our dataset only has end-of-semester aggregates.

**Q6. Why no fairness audit in the future-work list?**
A: Good catch — we should add it. Models trained on biased historical advising could perpetuate disparities (e.g., older or non-traditional students).

---

## Slide 19 — End / Q&A

**Q1. Where can I get the code?**
A: github.com/Lambert-Nguyen/cmpe255-student-dropout-prediction — three Jupyter notebooks (preprocessing, EDA, modeling), `src/utils.py`, all figures and tables in `results/`.

**Q2. Can I cite your work?**
A: Cite the underlying dataset (Realinho et al., 2021) for any reuse of the data; this project itself is a course deliverable.

---

## Cross-Cutting / "Big Picture" Questions

**Q1. What's the single most important finding?**
A: First-semester academic performance — specifically approved curricular units — is the strongest predictor of dropout. By end of semester 1, a student with fewer than 3 approved units has a 77% dropout probability.

**Q2. What's the model's main limitation?**
A: Single-institution training data (one Portuguese polytechnic). Generalization across systems is unverified.

**Q3. If you had one more month, what would you add?**
A: Streamlit advisor dashboard + SHAP per-student explanations, so the model is actionable in an advising office.

**Q4. What's the ethical risk?**
A: Self-fulfilling prophecy: a student labeled "high risk" early may be tracked into lower-resource paths. Mitigation: use the score as an opportunity flag for support, never a gatekeeping signal.

**Q5. Could a simpler rule-based system beat your model?**
A: A 1-rule baseline ("flag if CU1 ≤ 2") would catch a lot of dropouts but miss financial-stress cases that pass courses early. The model captures both signals; the rule alone doesn't.

**Q6. Is 70.6% F1-macro actually good?**
A: For a 3-class problem with 18% minority and only end-of-semester features, yes — comparable published results on this dataset land in the 0.65–0.72 range.

**Q7. What would a deep learning model add?**
A: Marginal accuracy gain (1–3 points likely) at significant interpretability cost. For an advising tool, interpretability matters; we'd use deep learning to *complement*, not replace, XGBoost.

**Q8. Did you handle data leakage?**
A: Test set held out from the very first preprocessing step. Scaling fit on train only and applied to test. CV folds within train. No information from test ever influences training.

**Q9. What if the dataset was 10× larger?**
A: We'd expect XGBoost's gap over the linear baseline to widen, Random Forest's CV to tighten further, and clustering silhouettes to remain low (more data doesn't make overlapping classes separable).

**Q10. Why didn't you publish this as a paper?**
A: It's a course project. A publishable version would need cross-institution validation, fairness audit, and a deployed pilot — all in Future Work.
