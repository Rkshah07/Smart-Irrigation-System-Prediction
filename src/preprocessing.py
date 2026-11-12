"""
preprocessing.py
----------------
Defines data cleaning, ordinal target mapping, robust missing value handling,
and feature encoding using a unified pyspark.ml Pipeline.
"""

from typing import List, Tuple, Dict, Any
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import (
    Imputer,
    StringIndexer,
    OneHotEncoder,
    VectorAssembler,
    StandardScaler
)

# Feature definitions
SENSOR_NUMERIC_COLS = [
    "Soil_Moisture",
    "Soil_pH",
    "Organic_Carbon",
    "Electrical_Conductivity",
    "Humidity"
]

OTHER_NUMERIC_COLS = [
    "Rainfall_mm",
    "Sunlight_Hours",
    "Wind_Speed_kmh",
    "Field_Area_hectare",
    "Previous_Irrigation_mm"
]

NUMERIC_COLS = SENSOR_NUMERIC_COLS + OTHER_NUMERIC_COLS

CATEGORICAL_COLS = [
    "Soil_Type",
    "Crop_Type",
    "Crop_Growth_Stage",
    "Season",
    "Irrigation_Type",
    "Water_Source",
    "Mulching_Used",
    "Region"
]

TARGET_COL = "Irrigation_Need"
SCORE_COL = "water_requirement_score"

# Ordinal score mapping: Low=0, Medium=1, High=2
LABEL_TO_SCORE = {"Low": 0.0, "Medium": 1.0, "High": 2.0}
SCORE_TO_LABEL = {0: "Low", 1: "Medium", 2: "High"}


def add_target_score(df: DataFrame) -> DataFrame:
    """
    Maps categorical Irrigation_Need (Low, Medium, High) to an ordinal
    numeric target `water_requirement_score` (0.0, 1.0, 2.0).
    """
    if TARGET_COL not in df.columns:
        return df

    return df.withColumn(
        SCORE_COL,
        when(col(TARGET_COL) == "Low", 0.0)
        .when(col(TARGET_COL) == "Medium", 1.0)
        .when(col(TARGET_COL) == "High", 2.0)
        .otherwise(0.0)
    )


def fill_categorical_missing(df: DataFrame, cat_cols: List[str] = CATEGORICAL_COLS) -> DataFrame:
    """
    Replaces any null or NaN values in categorical columns with 'Unknown'.
    """
    fill_dict = {c: "Unknown" for c in cat_cols if c in df.columns}
    return df.na.fill(fill_dict)


def build_feature_pipeline_stages() -> Tuple[List[Any], List[str]]:
    """
    Constructs the pyspark.ml feature engineering pipeline stages:
    1. Imputer (median strategy) for all numeric sensor and environmental features.
    2. StringIndexer (handleInvalid='keep') for all categorical features.
    3. OneHotEncoder for indexed categorical features.
    4. VectorAssembler combining numeric + one-hot encoded features.
    5. StandardScaler standardizing feature scales.

    Returns:
        stages: List of pyspark.ml Transformer / Estimator stages
        feature_metadata: Helper list of stage names
    """
    stages = []

    # 1. Median Imputer for numeric columns
    imputed_num_cols = [f"{c}_imputed" for c in NUMERIC_COLS]
    imputer = Imputer(
        inputCols=NUMERIC_COLS,
        outputCols=imputed_num_cols,
        strategy="median"
    )
    stages.append(imputer)

    # 2. StringIndexer for all categorical columns
    indexed_cat_cols = [f"{c}_idx" for c in CATEGORICAL_COLS]
    indexers = [
        StringIndexer(inputCol=c, outputCol=f"{c}_idx", handleInvalid="keep")
        for c in CATEGORICAL_COLS
    ]
    stages.extend(indexers)

    # 3. OneHotEncoder for indexed categorical columns
    encoded_cat_cols = [f"{c}_vec" for c in CATEGORICAL_COLS]
    ohe = OneHotEncoder(
        inputCols=indexed_cat_cols,
        outputCols=encoded_cat_cols,
        handleInvalid="keep"
    )
    stages.append(ohe)

    # 4. VectorAssembler
    assembler_inputs = imputed_num_cols + encoded_cat_cols
    assembler = VectorAssembler(
        inputCols=assembler_inputs,
        outputCol="unscaled_features",
        handleInvalid="keep"
    )
    stages.append(assembler)

    # 5. StandardScaler
    scaler = StandardScaler(
        inputCol="unscaled_features",
        outputCol="features",
        withStd=True,
        withMean=False
    )
    stages.append(scaler)

    return stages, assembler_inputs
