#!/usr/bin/env python3
"""
AI Personal Coach — Baseline Modeling Pipeline (K3: Data Lead)
Reproducible training & evaluation of Logistic Regression and LightGBM models.
Dataset: data-research/oulad_synthetic_processed.csv (3,250 samples)
Target: churn_90d (Binary proxy label)
"""

import os
from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
import lightgbm as lgb


def run_baseline_modeling():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir.parent / "oulad_synthetic_processed.csv"

    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at {data_path}")

    print(f"[*] Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"[*] Dataset shape: {df.shape}")

    # Feature selection matching K3 scope
    drop_cols = ["student_id", "exam_type", "grade", "sub_segment", "churn_90d"]
    feature_cols = [col for col in df.columns if col not in drop_cols]
    target_col = "churn_90d"

    X = df[feature_cols]
    y = df[target_col]

    print(f"[*] Features ({len(feature_cols)}): {feature_cols}")
    print(f"[*] Target class distribution:\n{y.value_counts(normalize=True).round(4) * 100}%")

    # Reproducible train-test split (75% train / 25% test, stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "LightGBM Classifier": lgb.LGBMClassifier(
            n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42, verbose=-1
        ),
    }

    metrics_list = []
    trained_models = {}

    for name, model in models.items():
        print(f"\n[*] Training {name}...")
        model.fit(X_train, y_train)
        trained_models[name] = model

        probs = model.predict_proba(X_test)[:, 1]
        preds = model.predict(X_test)

        roc_auc = roc_auc_score(y_test, probs)
        pr_auc = average_precision_score(y_test, probs)
        f1 = f1_score(y_test, preds)
        precision = precision_score(y_test, preds)
        recall = recall_score(y_test, preds)
        acc = accuracy_score(y_test, preds)
        loss = log_loss(y_test, probs)
        cm = confusion_matrix(y_test, preds)

        metrics_list.append({
            "Model": name,
            "ROC-AUC": round(roc_auc, 4),
            "PR-AUC": round(pr_auc, 4),
            "F1-Score": round(f1, 4),
            "Precision": round(precision, 4),
            "Recall": round(recall, 4),
            "Accuracy": round(acc, 4),
            "LogLoss": round(loss, 4),
            "TN": int(cm[0, 0]),
            "FP": int(cm[0, 1]),
            "FN": int(cm[1, 0]),
            "TP": int(cm[1, 1]),
        })

        # Save confusion matrix plot
        plt.figure(figsize=(5, 4))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["Retained (0)", "Churn (1)"],
            yticklabels=["Retained (0)", "Churn (1)"],
        )
        plt.title(f"Confusion Matrix — {name}")
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.tight_layout()

        safe_name = name.lower().split()[0]
        cm_path = base_dir / f"confusion_matrix_{safe_name}.png"
        plt.savefig(cm_path, dpi=300)
        plt.close()
        print(f"  -> Saved CM plot to {cm_path.name}")

    results_df = pd.DataFrame(metrics_list)
    results_csv = base_dir / "baseline_results.csv"
    results_df.to_csv(results_csv, index=False)
    print(f"\n[*] Saved benchmark results to {results_csv.name}:\n")
    print(results_df.to_string(index=False))

    # Feature Importance for LightGBM
    lgb_model = trained_models["LightGBM Classifier"]
    importance_df = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": lgb_model.feature_importances_,
    }).sort_values(by="Importance", ascending=False)
    print("\n[*] LightGBM Feature Importances:")
    print(importance_df.to_string(index=False))

    # Serialize trained models for inference / pipeline use
    joblib.dump(trained_models["LightGBM Classifier"], base_dir / "lightgbm_model.joblib")
    joblib.dump(trained_models["Logistic Regression"], base_dir / "logistic_model.joblib")
    print(f"[*] Serialized model artifacts to {base_dir}")

    return results_df


if __name__ == "__main__":
    run_baseline_modeling()
