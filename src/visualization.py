"""
visualization.py
----------------
Generates publication-quality visualizations of water requirement trends
per crop type, growth stage, season, model predictions, and feature importance.
Aggregations are computed in Spark before converting small summary tables to pandas.
"""

import os
from typing import List, Dict, Any
from pyspark.sql import DataFrame
from pyspark.sql.functions import avg, count, col
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.preprocessing import SCORE_COL, TARGET_COL


def set_plot_style():
    """Configures consistent seaborn and matplotlib aesthetics."""
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams.update({
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.titlesize": 14,
        "figure.dpi": 300,
    })


def generate_all_visualizations(
    df: DataFrame,
    val_preds: DataFrame,
    top_coefficients: List[Dict[str, Any]],
    output_dir: str = "outputs/plots"
) -> List[str]:
    """
    Computes all aggregated summaries in Spark, transfers small aggregate
    tables to pandas, and saves 6 high-resolution PNG visualizations.
    """
    print("\n" + "=" * 60)
    print("TASK 6: Generating Visualizations (outputs/plots/)")
    print("=" * 60)

    os.makedirs(output_dir, exist_ok=True)
    set_plot_style()
    generated_files = []

    # 1. Bar Chart: Mean water_requirement_score per Crop_Type
    print("-> Plot 1/6: Mean water requirement score per Crop_Type...")
    crop_mean_df = (
        df.groupBy("Crop_Type")
        .agg(avg(SCORE_COL).alias("mean_score"), count("*").alias("count"))
        .orderBy("mean_score", ascending=False)
        .toPandas()
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    palette = sns.color_palette("Blues_r", n_colors=len(crop_mean_df))
    bars = sns.barplot(
        data=crop_mean_df,
        x="Crop_Type",
        y="mean_score",
        palette=palette,
        ax=ax,
        edgecolor="black",
        linewidth=0.8
    )
    for p in bars.patches:
        ax.annotate(
            f"{p.get_height():.3f}",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center", va="bottom",
            xytext=(0, 4), textcoords="offset points",
            fontweight="bold", fontsize=10
        )
    ax.set_title("Mean Water Requirement Score by Crop Type (0=Low, 1=Medium, 2=High)")
    ax.set_xlabel("Crop Type")
    ax.set_ylabel("Mean Water Requirement Score")
    ax.set_ylim(0, max(crop_mean_df["mean_score"]) * 1.15)
    plt.tight_layout()
    p1 = os.path.join(output_dir, "bar_crop_type_water_requirement.png")
    plt.savefig(p1, bbox_inches="tight")
    plt.close()
    generated_files.append(p1)

    # 2. Stacked Bar Chart: Share of Low / Medium / High per Crop_Type
    print("-> Plot 2/6: Stacked bar chart of irrigation need share per Crop_Type...")
    crop_share_df = (
        df.groupBy("Crop_Type", TARGET_COL)
        .agg(count("*").alias("count"))
        .toPandas()
    )
    share_pivot = crop_share_df.pivot(index="Crop_Type", columns=TARGET_COL, values="count").fillna(0)
    for c in ["Low", "Medium", "High"]:
        if c not in share_pivot.columns:
            share_pivot[c] = 0
    share_pivot = share_pivot[["Low", "Medium", "High"]]
    share_pct = share_pivot.div(share_pivot.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(10, 5.5))
    colors = ["#2ca02c", "#ff7f0e", "#d62728"]  # Green, Orange, Red
    share_pct.plot(kind="bar", stacked=True, ax=ax, color=colors, edgecolor="black", linewidth=0.7)
    ax.set_title("Distribution of Irrigation Need Classes per Crop Type (%)")
    ax.set_xlabel("Crop Type")
    ax.set_ylabel("Percentage (%)")
    ax.set_ylim(0, 100)
    ax.legend(title="Irrigation Need", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=0)
    plt.tight_layout()
    p2 = os.path.join(output_dir, "stacked_bar_crop_irrigation_need.png")
    plt.savefig(p2, bbox_inches="tight")
    plt.close()
    generated_files.append(p2)

    # 3. Heatmap: Mean score by Crop_Type x Crop_Growth_Stage
    print("-> Plot 3/6: Heatmap of mean score by Crop_Type x Crop_Growth_Stage...")
    stage_df = (
        df.groupBy("Crop_Type", "Crop_Growth_Stage")
        .agg(avg(SCORE_COL).alias("mean_score"))
        .toPandas()
    )
    stage_pivot = stage_df.pivot(index="Crop_Type", columns="Crop_Growth_Stage", values="mean_score")

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(
        stage_pivot,
        annot=True,
        fmt=".3f",
        cmap="YlGnBu",
        linewidths=0.5,
        cbar_kws={"label": "Mean Water Requirement Score"},
        ax=ax
    )
    ax.set_title("Water Requirement Heatmap: Crop Type vs Growth Stage")
    ax.set_xlabel("Crop Growth Stage")
    ax.set_ylabel("Crop Type")
    plt.tight_layout()
    p3 = os.path.join(output_dir, "heatmap_crop_growth_stage.png")
    plt.savefig(p3, bbox_inches="tight")
    plt.close()
    generated_files.append(p3)

    # 4. Grouped Bar / Line Chart: Mean score by Crop_Type across Season
    print("-> Plot 4/6: Mean score by Crop_Type across Season...")
    season_df = (
        df.groupBy("Crop_Type", "Season")
        .agg(avg(SCORE_COL).alias("mean_score"))
        .toPandas()
    )

    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.barplot(
        data=season_df,
        x="Crop_Type",
        y="mean_score",
        hue="Season",
        palette="Set2",
        edgecolor="black",
        linewidth=0.7,
        ax=ax
    )
    ax.set_title("Seasonal Comparison of Mean Water Requirement per Crop")
    ax.set_xlabel("Crop Type")
    ax.set_ylabel("Mean Water Requirement Score")
    ax.legend(title="Season", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    p4 = os.path.join(output_dir, "crop_season_water_requirement.png")
    plt.savefig(p4, bbox_inches="tight")
    plt.close()
    generated_files.append(p4)

    # 5. Predicted vs Actual Mean Score per Crop_Type
    print("-> Plot 5/6: Predicted vs actual mean score per Crop_Type on Validation Set...")
    pred_actual_df = (
        val_preds.groupBy("Crop_Type")
        .agg(
            avg(SCORE_COL).alias("Actual Mean"),
            avg("raw_prediction").alias("Predicted Mean")
        )
        .toPandas()
    )
    pred_melted = pred_actual_df.melt(
        id_vars="Crop_Type",
        value_vars=["Actual Mean", "Predicted Mean"],
        var_name="Type",
        value_name="Score"
    )

    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.barplot(
        data=pred_melted,
        x="Crop_Type",
        y="Score",
        hue="Type",
        palette=["#1f77b4", "#ff7f0e"],
        edgecolor="black",
        linewidth=0.7,
        ax=ax
    )
    ax.set_title("Validation Set: Actual vs Predicted Mean Score by Crop Type")
    ax.set_xlabel("Crop Type")
    ax.set_ylabel("Score (0=Low, 1=Medium, 2=High)")
    ax.legend(title="", loc="upper right")
    plt.tight_layout()
    p5 = os.path.join(output_dir, "pred_vs_actual_crop_type.png")
    plt.savefig(p5, bbox_inches="tight")
    plt.close()
    generated_files.append(p5)

    # 6. Plot of Top Feature Coefficients
    print("-> Plot 6/6: Top feature coefficients bar chart...")
    coef_df = pd.DataFrame(top_coefficients)
    coef_df = coef_df.sort_values(by="abs_coefficient", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 7))
    bar_colors = ["#2b83ba" if c >= 0 else "#d7191c" for c in coef_df["coefficient"]]
    bars = ax.barh(coef_df["feature"], coef_df["coefficient"], color=bar_colors, edgecolor="black", linewidth=0.6)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.7)

    for bar, val in zip(bars, coef_df["coefficient"]):
        x_pos = bar.get_width()
        ha = "left" if x_pos >= 0 else "right"
        offset = 0.002 if x_pos >= 0 else -0.002
        ax.text(x_pos + offset, bar.get_y() + bar.get_height() / 2, f"{val:.4f}",
                va="center", ha=ha, fontsize=9, fontweight="bold")

    ax.set_title("Top 15 Standardized Model Coefficients (Blue = Positive, Red = Negative)")
    ax.set_xlabel("Standardized Coefficient Value")
    ax.set_ylabel("Feature")
    plt.tight_layout()
    p6 = os.path.join(output_dir, "top_feature_coefficients.png")
    plt.savefig(p6, bbox_inches="tight")
    plt.close()
    generated_files.append(p6)

    print(f"-> All 6 plots saved successfully to {output_dir}")
    return generated_files
