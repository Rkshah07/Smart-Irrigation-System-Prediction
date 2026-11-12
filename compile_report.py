"""
compile_report.py
-----------------
Standalone script to execute build_pdf_report and compile
outputs/INT315_Smart_Irrigation_Report.pdf cleanly.
"""

import os
import sys
import json
import pandas as pd

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.report_generator import build_pdf_report

def main():
    metrics_path = os.path.join(current_dir, "outputs", "metrics.json")
    timing_path = os.path.join(current_dir, "outputs", "cluster_timing.csv")
    plots_dir = os.path.join(current_dir, "outputs", "plots")
    screenshots_dir = os.path.join(current_dir, "outputs", "screenshots")
    pdf_out = os.path.join(current_dir, "outputs", "INT315_Smart_Irrigation_Report.pdf")

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    timing_df = pd.read_csv(timing_path) if os.path.exists(timing_path) else None

    # Load top coefficients from powerbi_data/model_coefficients.csv
    coeffs_path = os.path.join(current_dir, "outputs", "dashboard", "powerbi_data", "model_coefficients.csv")
    if os.path.exists(coeffs_path):
        c_df = pd.read_csv(coeffs_path)
        top_coeffs = c_df.to_dict(orient="records")
    else:
        top_coeffs = metrics.get("top_coefficients", [])

    print(f"Loaded {len(top_coeffs)} top coefficients.")
    print("Compiling PDF report...")
    res = build_pdf_report(
        metrics=metrics,
        top_coefficients=top_coeffs,
        timing_df=timing_df,
        plots_dir=plots_dir,
        screenshots_dir=screenshots_dir,
        output_pdf_path=pdf_out
    )
    print("Successfully built:", res)

if __name__ == "__main__":
    main()
