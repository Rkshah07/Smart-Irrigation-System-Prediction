"""
evaluation.py
-------------
Evaluates the Linear Regression model on training and validation splits.
Computes RMSE, R2, rounded classification accuracy, and confusion matrix,
and exports all metrics to outputs/metrics.json.
"""

import os
import json
from typing import Dict, Any, Tuple
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, round as spark_round, count
from pyspark.ml.evaluation import RegressionEvaluator
from src.preprocessing import SCORE_COL, TARGET_COL


def discretize_predictions(df: DataFrame) -> DataFrame:
    """
    Clips raw continuous predictions to [0.0, 2.0], rounds to the nearest
    integer score, and maps back to categorical labels (Low, Medium, High).
    """
    # 1. Clip predictions between 0.0 and 2.0
    clipped = (
        when(col("raw_prediction") < 0.0, 0.0)
        .when(col("raw_prediction") > 2.0, 2.0)
        .otherwise(col("raw_prediction"))
    )

    # 2. Round to nearest integer class (0, 1, 2)
    discrete_score = spark_round(clipped).cast("int")

    # 3. Map back to class labels
    pred_label = (
        when(discrete_score == 0, "Low")
        .when(discrete_score == 1, "Medium")
        .when(discrete_score == 2, "High")
        .otherwise("Low")
    )

    return (
        df.withColumn("clipped_prediction", clipped)
        .withColumn("discrete_score", discrete_score)
        .withColumn("predicted_class", pred_label)
    )


def evaluate_model(
    train_preds: DataFrame,
    val_preds: DataFrame,
    best_params: Dict[str, Any],
    output_json_path: str = "outputs/metrics.json"
) -> Dict[str, Any]:
    """
    Computes regression metrics (RMSE, R2) and classification metrics
    (Accuracy, Confusion Matrix) on train and validation sets.
    """
    print("\n" + "=" * 60)
    print("TASK 5: Evaluating Model Performance")
    print("=" * 60)

    # Regression evaluators
    rmse_eval = RegressionEvaluator(
        predictionCol="raw_prediction",
        labelCol=SCORE_COL,
        metricName="rmse"
    )
    r2_eval = RegressionEvaluator(
        predictionCol="raw_prediction",
        labelCol=SCORE_COL,
        metricName="r2"
    )
    mae_eval = RegressionEvaluator(
        predictionCol="raw_prediction",
        labelCol=SCORE_COL,
        metricName="mae"
    )

    train_rmse = float(rmse_eval.evaluate(train_preds))
    train_r2 = float(r2_eval.evaluate(train_preds))
    train_mae = float(mae_eval.evaluate(train_preds))

    val_rmse = float(rmse_eval.evaluate(val_preds))
    val_r2 = float(r2_eval.evaluate(val_preds))
    val_mae = float(mae_eval.evaluate(val_preds))

    print("\n--- Regression Metrics (Target: water_requirement_score) ---")
    print(f"  Training Set   -> RMSE: {train_rmse:.4f} | R2: {train_r2:.4f} | MAE: {train_mae:.4f}")
    print(f"  Validation Set -> RMSE: {val_rmse:.4f} | R2: {val_r2:.4f} | MAE: {val_mae:.4f}")

    # Overfitting / Underfitting Assessment
    delta_rmse = abs(val_rmse - train_rmse)
    delta_r2 = abs(val_r2 - train_r2)
    print(f"  Train/Val Gap  -> Delta RMSE: {delta_rmse:.4f} | Delta R2: {delta_r2:.4f}")
    if delta_rmse < 0.02 and delta_r2 < 0.02:
        print("  Status: Model generalizes consistently between train and validation (no severe overfitting).")
    elif val_rmse > train_rmse + 0.05:
        print("  Status: Model exhibits slight overfitting on training set.")

    # Discretized Classification Metrics
    val_discrete = discretize_predictions(val_preds)
    train_discrete = discretize_predictions(train_preds)

    val_total = val_discrete.count()
    val_correct = val_discrete.filter(col(TARGET_COL) == col("predicted_class")).count()
    val_accuracy = float(val_correct / val_total)

    train_total = train_discrete.count()
    train_correct = train_discrete.filter(col(TARGET_COL) == col("predicted_class")).count()
    train_accuracy = float(train_correct / train_total)

    print("\n--- Supplementary Discretized Classification Metrics ---")
    print(f"  Validation Rounded Accuracy: {val_accuracy:.4f} ({val_accuracy * 100:.2f}%)")
    print(f"  Training Rounded Accuracy:   {train_accuracy:.4f} ({train_accuracy * 100:.2f}%)")

    # Compute Confusion Matrix via Spark groupBy aggregation
    cm_rows = (
        val_discrete.groupBy(TARGET_COL, "predicted_class")
        .agg(count("*").alias("count"))
        .collect()
    )

    classes = ["Low", "Medium", "High"]
    cm_dict = {actual: {pred: 0 for pred in classes} for actual in classes}
    for row in cm_rows:
        act = row[TARGET_COL]
        prd = row["predicted_class"]
        if act in cm_dict and prd in cm_dict[act]:
            cm_dict[act][prd] = int(row["count"])

    print("\nConfusion Matrix (Validation Split):")
    print(f"{'Actual':<10} | " + " | ".join([f"{'Pred ' + c:>10}" for c in classes]))
    print("-" * 46)
    for act in classes:
        row_str = " | ".join([f"{cm_dict[act][prd]:>10,}" for prd in classes])
        print(f"{act:<10} | {row_str}")

    # Methodological limitation note
    model_limitation_note = (
        "Linear Regression treats the target as continuous, unbounded, and equidistant with homoscedastic errors. "
        "For an ordinal classification target (Low=0, Medium=1, High=2), standard Linear Regression may yield predictions "
        "beyond valid bounds (<0 or >2) and cannot model non-linear class decision boundaries or class imbalance "
        "as naturally as Ordinal Logistic Regression, Random Forests, or Gradient Boosted Decision Trees."
    )
    print(f"\n[METHODOLOGICAL NOTE]\n{model_limitation_note}")

    metrics_payload = {
        "model": "LinearRegression",
        "hyperparameters": best_params,
        "regression_metrics": {
            "validation": {
                "rmse": round(val_rmse, 5),
                "r2": round(val_r2, 5),
                "mae": round(val_mae, 5)
            },
            "training": {
                "rmse": round(train_rmse, 5),
                "r2": round(train_r2, 5),
                "mae": round(train_mae, 5)
            },
            "generalization_gap": {
                "delta_rmse": round(delta_rmse, 5),
                "delta_r2": round(delta_r2, 5)
            }
        },
        "classification_metrics": {
            "validation_accuracy": round(val_accuracy, 5),
            "training_accuracy": round(train_accuracy, 5),
            "confusion_matrix": cm_dict
        },
        "methodological_limitation_note": model_limitation_note
    }

    # Save to outputs/metrics.json
    os.makedirs(os.path.dirname(os.path.abspath(output_json_path)), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"\n-> Metrics successfully written to: {output_json_path}")

    return metrics_payload
