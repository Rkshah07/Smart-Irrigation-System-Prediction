"""
modeling.py
-----------
Handles model construction, hyperparameter tuning via CrossValidator,
training of pyspark.ml LinearRegression, feature importance extraction,
and model persistence.
"""

import os
from typing import Tuple, List, Dict, Any
from pyspark.sql import DataFrame
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.regression import LinearRegression, LinearRegressionModel
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import RegressionEvaluator
from src.preprocessing import SCORE_COL, build_feature_pipeline_stages


def train_linear_regression(
    train_df: DataFrame,
    use_cross_validation: bool = True,
    seed: int = 42
) -> Tuple[PipelineModel, LinearRegressionModel, Dict[str, Any]]:
    """
    Fits an end-to-end pyspark.ml Pipeline comprising preprocessing stages
    and LinearRegression on the training dataset.

    To optimize training throughput and prevent redundant re-computation across
    cross-validation folds, feature engineering stages are fitted once, feature
    vectors are cached, and hyperparameter tuning is conducted on prepped vectors.
    Finally, all stages are combined into a single unified PipelineModel.

    Returns:
        full_pipeline_model: The unified PipelineModel covering raw data to prediction
        best_lr_model: The underlying LinearRegressionModel
        best_params: Dictionary of chosen hyperparameters
    """
    print("\n" + "=" * 60)
    print("TASK 4: Building & Training Linear Regression Model")
    print("=" * 60)

    # 1. Build and fit feature engineering pipeline on train_df
    print("-> Fitting feature preprocessing stages (Imputer, StringIndexer, OHE, Scaler)...")
    feature_stages, assembler_inputs = build_feature_pipeline_stages()
    feature_pipeline = Pipeline(stages=feature_stages)
    feature_model = feature_pipeline.fit(train_df)

    # 2. Transform and cache feature vectors for modeling
    print("-> Transforming and caching training feature vectors for efficient tuning...")
    prepped_train = (
        feature_model.transform(train_df)
        .select("features", SCORE_COL)
        .cache()
    )
    prepped_count = prepped_train.count()
    print(f"   Prepped training samples cached: {prepped_count:,}")

    # 3. Estimator & Evaluator
    lr = LinearRegression(
        featuresCol="features",
        labelCol=SCORE_COL,
        predictionCol="raw_prediction",
        maxIter=50,
        solver="auto"
    )

    evaluator = RegressionEvaluator(
        predictionCol="raw_prediction",
        labelCol=SCORE_COL,
        metricName="rmse"
    )

    if use_cross_validation:
        print("-> Running 3-Fold Cross-Validation for hyperparameter tuning...")
        param_grid = (
            ParamGridBuilder()
            .addGrid(lr.regParam, [0.01, 0.1])
            .addGrid(lr.elasticNetParam, [0.0, 0.5])
            .build()
        )
        print(f"   Grid size: {len(param_grid)} candidates across 3 folds (seed={seed}, sequential execution)")

        cv = CrossValidator(
            estimator=lr,
            estimatorParamMaps=param_grid,
            evaluator=evaluator,
            numFolds=3,
            seed=seed,
            parallelism=1
        )
        print("   Fitting CrossValidator across folds...")
        cv_model = cv.fit(prepped_train)

        best_lr_model: LinearRegressionModel = cv_model.bestModel
        best_reg = best_lr_model.getRegParam()
        best_elastic = best_lr_model.getElasticNetParam()
        best_params = {
            "regParam": float(best_reg),
            "elasticNetParam": float(best_elastic),
            "tuning_method": "3-Fold CrossValidator"
        }
        print(f"-> Best Parameters Selected: regParam={best_reg}, elasticNetParam={best_elastic}")
    else:
        print("-> Using fixed optimal regularized LinearRegression parameters...")
        lr.setRegParam(0.01).setElasticNetParam(0.0)
        best_lr_model = lr.fit(prepped_train)
        best_params = {
            "regParam": 0.01,
            "elasticNetParam": 0.0,
            "tuning_method": "Pre-tuned Fixed Regularization"
        }

    # 4. Assemble the unified end-to-end PipelineModel
    full_pipeline_model = PipelineModel(stages=feature_model.stages + [best_lr_model])
    print("-> Assembled unified PipelineModel containing all preprocessing and regression stages.")

    # Free intermediate cached feature vectors
    try:
        prepped_train.unpersist()
    except Exception:
        pass

    return full_pipeline_model, best_lr_model, best_params


def extract_top_coefficients(
    fitted_pipeline: PipelineModel,
    lr_model: LinearRegressionModel,
    transformed_df: DataFrame,
    top_n: int = 15
) -> List[Dict[str, Any]]:
    """
    Extracts feature names from the DataFrame vector metadata and maps them
    to their trained LinearRegression coefficients, sorted by absolute magnitude.
    """
    print("\n--- Extracting Feature Coefficients ---")
    schema = transformed_df.schema
    if "unscaled_features" in schema.names and "ml_attr" in schema["unscaled_features"].metadata:
        features_meta = schema["unscaled_features"].metadata
    else:
        features_meta = schema["features"].metadata

    # Resolve feature names from ML attribute metadata
    names_by_idx = {}
    if "ml_attr" in features_meta and "attrs" in features_meta["ml_attr"]:
        attrs = features_meta["ml_attr"]["attrs"]
        for attr_type in ["numeric", "binary", "nominal"]:
            if attr_type in attrs:
                for entry in attrs[attr_type]:
                    names_by_idx[entry["idx"]] = entry["name"]

    coefficients = lr_model.coefficients.toArray()
    coef_records = []
    for idx, coef in enumerate(coefficients):
        feat_name = names_by_idx.get(idx, f"feature_{idx}")
        # Clean up readable feature name
        clean_name = feat_name.replace("_imputed", "").replace("_vec_", " = ").replace("_vec", "")
        coef_records.append({
            "index": idx,
            "feature": clean_name,
            "raw_name": feat_name,
            "coefficient": float(coef),
            "abs_coefficient": float(abs(coef))
        })

    coef_records.sort(key=lambda x: x["abs_coefficient"], reverse=True)
    top_coefficients = coef_records[:top_n]

    print(f"\nTop {top_n} Features by Absolute Coefficient Value:")
    print(f"{'Rank':<5} {'Feature Name':<45} {'Coefficient':>12} {'Abs Value':>12}")
    print("-" * 76)
    for i, rec in enumerate(top_coefficients, 1):
        print(f"{i:<5} {rec['feature']:<45} {rec['coefficient']:>12.5f} {rec['abs_coefficient']:>12.5f}")

    return top_coefficients


def save_pipeline_model(fitted_pipeline: PipelineModel, output_path: str) -> None:
    """
    Saves the trained pyspark.ml PipelineModel to disk.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    print(f"\n-> Saving fitted PipelineModel to: {output_path}")
    fitted_pipeline.write().overwrite().save(output_path)
    print("   Model saved successfully.")
