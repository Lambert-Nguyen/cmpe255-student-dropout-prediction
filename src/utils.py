"""
Utility functions for CMPE 255 Student Dropout Prediction Project.
Reusable helpers for preprocessing, evaluation, and visualization.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    auc,
    accuracy_score,
    f1_score,
)
from sklearn.preprocessing import label_binarize
from itertools import cycle


# ── Consistent color scheme across all visualizations ──
TARGET_COLORS = {
    "Dropout": "#E24B4A",    # Red
    "Enrolled": "#EF9F27",   # Amber
    "Graduate": "#1D9E75",   # Green
}
TARGET_ORDER = ["Dropout", "Enrolled", "Graduate"]


def load_dataset(filepath: str = None) -> pd.DataFrame:
    """Load the UCI Student Dropout dataset from a local CSV or via ucimlrepo."""
    if filepath:
        df = pd.read_csv(filepath, sep=";")
        return df

    # Fallback: fetch from UCI repo
    from ucimlrepo import fetch_ucirepo
    dataset = fetch_ucirepo(id=697)
    df = pd.concat([dataset.data.features, dataset.data.targets], axis=1)
    return df


def plot_class_distribution(df: pd.DataFrame, target_col: str = "Target",
                            save_path: str = None):
    """Bar chart of target class distribution with counts and percentages."""
    counts = df[target_col].value_counts().reindex(TARGET_ORDER)
    total = len(df)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(counts.index, counts.values,
                  color=[TARGET_COLORS[c] for c in counts.index],
                  edgecolor="white", linewidth=0.5)

    for bar, count in zip(bars, counts.values):
        pct = count / total * 100
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                f"{count}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=11)

    ax.set_ylabel("Number of Students")
    ax.set_title("Target Class Distribution")
    ax.set_ylim(0, counts.max() * 1.15)
    sns.despine()
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_confusion_matrix(y_true, y_pred, model_name: str = "Model",
                          labels=None, save_path: str = None):
    """Plot a 3×3 confusion matrix heatmap."""
    if labels is None:
        labels = TARGET_ORDER

    cm = confusion_matrix(y_true, y_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"Confusion Matrix — {model_name}")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_roc_multiclass(y_true, y_score, classes=None, model_name: str = "Model",
                        save_path: str = None):
    """Plot One-vs-Rest ROC curves for a 3-class problem."""
    if classes is None:
        classes = TARGET_ORDER

    y_bin = label_binarize(y_true, classes=classes)
    n_classes = len(classes)
    colors = [TARGET_COLORS[c] for c in classes]

    fig, ax = plt.subplots(figsize=(8, 6))
    for i, (cls, color) in enumerate(zip(classes, colors)):
        fpr, tpr, _ = roc_curve(y_bin[:, i], y_score[:, i])
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=color, lw=2,
                label=f"{cls} (AUC = {roc_auc:.3f})")

    ax.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.5)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(f"ROC Curve (One-vs-Rest) — {model_name}")
    ax.legend(loc="lower right")
    sns.despine()
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def evaluate_model(y_true, y_pred, y_score=None, model_name: str = "Model",
                   save_dir: str = None):
    """Run full evaluation: print report, plot confusion matrix and ROC."""
    print(f"\n{'='*60}")
    print(f"  {model_name} — Evaluation Results")
    print(f"{'='*60}")
    print(classification_report(y_true, y_pred, target_names=TARGET_ORDER))

    cm_path = f"{save_dir}/{model_name.lower().replace(' ', '_')}_cm.png" if save_dir else None
    plot_confusion_matrix(y_true, y_pred, model_name, save_path=cm_path)

    if y_score is not None:
        roc_path = f"{save_dir}/{model_name.lower().replace(' ', '_')}_roc.png" if save_dir else None
        plot_roc_multiclass(y_true, y_score, model_name=model_name, save_path=roc_path)


def build_comparison_table(results: dict) -> pd.DataFrame:
    """
    Build a model comparison DataFrame from a results dict.

    Parameters
    ----------
    results : dict
        {model_name: {"accuracy": float, "f1_macro": float, "f1_weighted": float, ...}}

    Returns
    -------
    pd.DataFrame sorted by f1_macro descending
    """
    df = pd.DataFrame(results).T
    df.index.name = "Model"
    df = df.sort_values("f1_macro", ascending=False)
    return df.round(4)
