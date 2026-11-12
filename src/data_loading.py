"""
data_loading.py
---------------
Handles discovery, loading, and initial exploratory inspection of the
Smart Irrigation System dataset CSV files.
"""

import os
from typing import Tuple, Dict, Any
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, count, when


def resolve_data_paths(base_dir: str = None) -> Dict[str, str]:
    """
    Locates the train, test, and sample_submission CSV files across common
    project directory layouts.
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    candidate_dirs = [
        os.path.join(base_dir, "..", "data"),
        os.path.join(base_dir, "..", "..", "irrigation_dataset"),
        os.path.join(base_dir, "data"),
        os.path.join(base_dir, "irrigation_dataset"),
        r"D:\cluster project\irrigation_dataset",
        r"D:\cluster project\smart_irrigation\data",
    ]

    found_dir = None
    for d in candidate_dirs:
        norm_d = os.path.abspath(d)
        if os.path.exists(norm_d) and os.path.exists(os.path.join(norm_d, "train.csv")):
            found_dir = norm_d
            break

    if not found_dir:
        raise FileNotFoundError(
            f"Could not locate dataset in any candidate path: {[os.path.abspath(d) for d in candidate_dirs]}"
        )

    return {
        "train": os.path.join(found_dir, "train.csv"),
        "test": os.path.join(found_dir, "test.csv"),
        "sample_submission": os.path.join(found_dir, "sample_submission.csv"),
        "directory": found_dir
    }


def load_datasets(spark: SparkSession, data_paths: Dict[str, str]) -> Tuple[DataFrame, DataFrame, DataFrame]:
    """
    Loads train.csv, test.csv, and sample_submission.csv with header=True and inferSchema=True.
    """
    print(f"\n" + "=" * 60)
    print(f"TASK 1: Loading Datasets into Spark from: {data_paths['directory']}")
    print("=" * 60)

    train_df = spark.read.csv(data_paths["train"], header=True, inferSchema=True)
    test_df = spark.read.csv(data_paths["test"], header=True, inferSchema=True)
    sub_df = spark.read.csv(data_paths["sample_submission"], header=True, inferSchema=True)

    train_count = train_df.count()
    test_count = test_df.count()
    sub_count = sub_df.count()

    print(f"-> Train rows: {train_count:,} | Columns: {len(train_df.columns)}")
    print(f"-> Test rows:  {test_count:,} | Columns: {len(test_df.columns)}")
    print(f"-> Sample sub: {sub_count:,} | Columns: {len(sub_df.columns)}")

    print("\n--- Train Schema ---")
    train_df.printSchema()

    print("\n--- Target Class Distribution (Irrigation_Need) in train.csv ---")
    dist_df = train_df.groupBy("Irrigation_Need").count().orderBy("count", ascending=False)
    dist_df.show()

    return train_df, test_df, sub_df


def inspect_null_counts(df: DataFrame, df_name: str = "Dataset") -> Dict[str, int]:
    """
    Computes and reports null counts per column in a Spark DataFrame.
    """
    print(f"\n--- Null Count Inspection for {df_name} ---")
    null_exprs = [count(when(col(c).isNull() | (col(c) == "NaN"), c)).alias(c) for c in df.columns]
    null_row = df.select(null_exprs).collect()[0].asDict()

    has_nulls = False
    for col_name, n_count in null_row.items():
        if n_count > 0:
            print(f"  [NULL ALERT] Column '{col_name}': {n_count:,} missing values")
            has_nulls = True

    if not has_nulls:
        print(f"  All {len(df.columns)} columns in {df_name} have 0 null values.")

    return null_row
