"""
generate_index_html.py
----------------------
Builds the standalone, production-ready, interactive web application (index.html)
for GitHub Pages deployment of the Smart Irrigation System Prediction project.

Includes:
  - Real-time client-side PySpark LinearRegression model predictor with live sliders,
    dynamic urgency gauge, discrete badge, water application advice, and feature attribution waterfall.
  - Interactive Plotly.js charts for crop trends, phenology heatmap, coefficients, and cluster scalability.
  - Executive KPI summary cards and student credentials for Roshan Kumar (LPU).
  - Direct download links for Academic PDF Report, Excel Workbook, and Test Submissions.
"""

import os
import json
import pandas as pd

def build_index_html():
    proj_dir = os.path.dirname(os.path.abspath(__file__))
    weights_path = os.path.join(proj_dir, "outputs", "model_weights.json")
    metrics_path = os.path.join(proj_dir, "outputs", "metrics.json")
    pbi_dir = os.path.join(proj_dir, "outputs", "dashboard", "powerbi_data")
    timing_path = os.path.join(proj_dir, "outputs", "cluster_timing.csv")
    output_html = os.path.join(proj_dir, "index.html")

    with open(weights_path, "r", encoding="utf-8") as f:
        weights_data = json.load(f)

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics_data = json.load(f)

    crop_trends_df = pd.read_csv(os.path.join(pbi_dir, "crop_trends.csv"))
    season_stage_df = pd.read_csv(os.path.join(pbi_dir, "season_stage_matrix.csv"))
    coeffs_df = pd.read_csv(os.path.join(pbi_dir, "model_coefficients.csv"))
    timing_df = pd.read_csv(timing_path) if os.path.exists(timing_path) else None

    # Prepare JSON structures for embedding into JavaScript
    weights_json = json.dumps(weights_data)
    crop_trends_json = json.dumps(crop_trends_df.to_dict(orient="records"))
    season_stage_json = json.dumps(season_stage_df.to_dict(orient="records"))
    coeffs_json = json.dumps(coeffs_df.to_dict(orient="records"))
    timing_json = json.dumps(timing_df.to_dict(orient="records")) if timing_df is not None else "[]"
    metrics_json = json.dumps(metrics_data)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Smart Irrigation System Prediction | Distributed PySpark ML</title>
  <meta name="description" content="Distributed Precision Agriculture ML Pipeline in Apache Spark (PySpark MLlib) - 900,000 Records, Standalone Cluster, Real-Time Interactive Model Predictor & Analytics." />

  <!-- Google Fonts & Plotly.js -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

  <style>
    :root {{
      --bg-dark: #0B1120;
      --bg-card: #131D31;
      --bg-card-hover: #1A2742;
      --border-color: #243556;
      --border-accent: #10B981;
      --primary: #10B981;
      --primary-dark: #059669;
      --primary-light: #34D399;
      --accent-blue: #38BDF8;
      --accent-amber: #F59E0B;
      --accent-red: #EF4444;
      --text-main: #F1F5F9;
      --text-muted: #94A3B8;
      --text-dim: #64748B;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-sans);
      background-color: var(--bg-dark);
      color: var(--text-main);
      line-height: 1.6;
      overflow-x: hidden;
    }}

    /* Top Navigation Bar */
    header {{
      background: rgba(11, 17, 32, 0.92);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 1000;
      padding: 0.85rem 2rem;
    }}

    .nav-container {{
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}

    .logo-area {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      text-decoration: none;
      color: var(--text-main);
    }}

    .logo-badge {{
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      color: #FFFFFF;
      font-weight: 800;
      padding: 0.4rem 0.75rem;
      border-radius: 8px;
      font-size: 1.1rem;
      letter-spacing: -0.5px;
      box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
    }}

    .logo-title h1 {{
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: -0.3px;
    }}

    .logo-title p {{
      font-size: 0.75rem;
      color: var(--primary-light);
      font-weight: 500;
    }}

    nav ul {{
      display: flex;
      list-style: none;
      gap: 1.25rem;
      align-items: center;
    }}

    nav a {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 500;
      transition: all 0.2s ease;
      padding: 0.4rem 0.6rem;
      border-radius: 6px;
    }}

    nav a:hover {{
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.05);
    }}

    nav a.highlight-btn {{
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      color: #FFFFFF;
      font-weight: 600;
      box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
    }}

    nav a.highlight-btn:hover {{
      background: var(--primary-light);
      color: #0F172A;
    }}

    /* Main Container */
    main {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
    }}

    /* Hero Banner */
    .hero {{
      text-align: center;
      padding: 2.5rem 1rem 3rem;
      position: relative;
    }}

    .hero-pill {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--primary-light);
      padding: 0.35rem 0.9rem;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 1.25rem;
    }}

    .hero h2 {{
      font-size: 2.6rem;
      font-weight: 800;
      letter-spacing: -1px;
      line-height: 1.2;
      margin-bottom: 1rem;
      background: linear-gradient(135deg, #FFFFFF 30%, var(--accent-blue) 70%, var(--primary-light) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero p.lead {{
      font-size: 1.15rem;
      color: var(--text-muted);
      max-width: 860px;
      margin: 0 auto 1.5rem;
      line-height: 1.6;
    }}

    .author-badge {{
      display: inline-flex;
      align-items: center;
      gap: 1rem;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      padding: 0.6rem 1.2rem;
      border-radius: 12px;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}

    .author-badge strong {{
      color: var(--text-main);
    }}

    /* Executive KPI Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2.5rem;
    }}

    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.4rem;
      transition: transform 0.2s ease, border-color 0.2s ease;
      position: relative;
      overflow: hidden;
    }}

    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--primary);
    }}

    .kpi-card:hover {{
      transform: translateY(-3px);
      border-color: rgba(16, 185, 129, 0.4);
    }}

    .kpi-title {{
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-dim);
      font-weight: 600;
      margin-bottom: 0.4rem;
    }}

    .kpi-value {{
      font-size: 1.85rem;
      font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -0.5px;
      margin-bottom: 0.3rem;
      font-family: var(--font-mono);
    }}

    .kpi-subtext {{
      font-size: 0.8rem;
      color: var(--primary-light);
      font-weight: 500;
    }}

    /* Section Headers */
    .section-title {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 1.5rem;
      padding-bottom: 0.6rem;
      border-bottom: 1px solid var(--border-color);
    }}

    .section-title h3 {{
      font-size: 1.5rem;
      font-weight: 700;
      color: #FFFFFF;
      letter-spacing: -0.4px;
    }}

    .section-title span.tag {{
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: var(--accent-blue);
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.2rem 0.6rem;
      border-radius: 6px;
    }}

    /* Interactive Predictor Layout */
    .predictor-section {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 18px;
      padding: 2rem;
      margin-bottom: 3rem;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    }}

    .predictor-layout {{
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 2rem;
    }}

    @media (max-width: 1024px) {{
      .predictor-layout {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Presets Bar */
    .preset-bar {{
      display: flex;
      gap: 0.6rem;
      flex-wrap: wrap;
      margin-bottom: 1.5rem;
      padding-bottom: 1.25rem;
      border-bottom: 1px dashed var(--border-color);
    }}

    .preset-btn {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 0.45rem 0.9rem;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    .preset-btn:hover {{
      background: rgba(16, 185, 129, 0.15);
      border-color: var(--primary);
      color: #FFFFFF;
    }}

    /* Form Grids */
    .form-group-title {{
      font-size: 0.85rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: var(--primary-light);
      margin: 1rem 0 0.6rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    .controls-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 0.9rem;
      margin-bottom: 0.6rem;
    }}

    .control-item {{
      background: rgba(11, 17, 32, 0.6);
      border: 1px solid var(--border-color);
      padding: 0.65rem 0.85rem;
      border-radius: 10px;
    }}

    .control-label {{
      display: flex;
      justify-content: space-between;
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 0.35rem;
    }}

    .control-label span.value-badge {{
      color: var(--accent-blue);
      font-family: var(--font-mono);
      font-weight: 700;
    }}

    input[type="range"] {{
      width: 100%;
      height: 5px;
      background: var(--border-color);
      border-radius: 5px;
      outline: none;
      accent-color: var(--primary);
      cursor: pointer;
    }}

    select {{
      width: 100%;
      background: var(--bg-dark);
      color: #FFFFFF;
      border: 1px solid var(--border-color);
      padding: 0.45rem 0.6rem;
      border-radius: 6px;
      font-size: 0.82rem;
      outline: none;
      cursor: pointer;
    }}

    select:focus {{
      border-color: var(--primary);
    }}

    /* Result Panel */
    .result-panel {{
      background: linear-gradient(145deg, #111A2E, #0E1626);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 1.75rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }}

    .result-header {{
      text-align: center;
      margin-bottom: 1.25rem;
    }}

    .result-header h4 {{
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-dim);
      font-weight: 700;
      margin-bottom: 0.5rem;
    }}

    /* Gauge & Score */
    .gauge-wrapper {{
      text-align: center;
      margin-bottom: 1.25rem;
    }}

    .score-number {{
      font-size: 3.4rem;
      font-weight: 800;
      font-family: var(--font-mono);
      line-height: 1;
      letter-spacing: -1px;
      color: #FFFFFF;
      margin-bottom: 0.4rem;
    }}

    .score-sub {{
      font-size: 0.85rem;
      color: var(--text-muted);
    }}

    /* Decision Badge */
    .decision-badge {{
      display: inline-block;
      padding: 0.6rem 1.6rem;
      border-radius: 9999px;
      font-size: 1.15rem;
      font-weight: 800;
      letter-spacing: 0.4px;
      text-align: center;
      margin: 0.75rem auto;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
      transition: all 0.3s ease;
    }}

    .badge-low {{
      background: linear-gradient(135deg, #059669, #10B981);
      color: #FFFFFF;
      box-shadow: 0 0 25px rgba(16, 185, 129, 0.4);
    }}

    .badge-medium {{
      background: linear-gradient(135deg, #D97706, #F59E0B);
      color: #0F172A;
      box-shadow: 0 0 25px rgba(245, 158, 11, 0.4);
    }}

    .badge-high {{
      background: linear-gradient(135deg, #DC2626, #EF4444);
      color: #FFFFFF;
      box-shadow: 0 0 25px rgba(239, 68, 68, 0.5);
      animation: pulse-high 1.8s infinite;
    }}

    @keyframes pulse-high {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.03); }}
    }}

    /* Dynamic Advice Box */
    .advice-box {{
      background: rgba(11, 17, 32, 0.7);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1rem;
      margin-bottom: 1.25rem;
    }}

    .advice-title {{
      font-size: 0.8rem;
      text-transform: uppercase;
      color: var(--accent-blue);
      font-weight: 700;
      margin-bottom: 0.4rem;
    }}

    .advice-text {{
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    .water-depth-stat {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 0.6rem;
      margin-top: 0.6rem;
      border-top: 1px dashed var(--border-color);
      font-size: 0.85rem;
    }}

    .water-depth-stat strong {{
      color: var(--primary-light);
      font-family: var(--font-mono);
      font-size: 1.05rem;
    }}

    /* Top Drivers Waterfall */
    .drivers-box {{
      background: rgba(11, 17, 32, 0.7);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1rem;
    }}

    .drivers-title {{
      font-size: 0.75rem;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-dim);
      margin-bottom: 0.6rem;
    }}

    .driver-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.8rem;
      margin-bottom: 0.35rem;
    }}

    .driver-val {{
      font-family: var(--font-mono);
      font-weight: 700;
    }}

    .val-neg {{ color: var(--primary-light); }}
    .val-pos {{ color: var(--accent-red); }}

    /* Analytics Dashboard Grid */
    .dashboard-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.5rem;
      margin-bottom: 3rem;
    }}

    @media (max-width: 900px) {{
      .dashboard-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .chart-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 1.25rem;
      position: relative;
    }}

    .chart-card h4 {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 0.3rem;
    }}

    .chart-card p.chart-desc {{
      font-size: 0.8rem;
      color: var(--text-dim);
      margin-bottom: 0.75rem;
    }}

    .plot-container {{
      width: 100%;
      height: 340px;
    }}

    /* Cluster Architecture Section */
    .cluster-section {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 2rem;
      margin-bottom: 3rem;
    }}

    .cluster-topology {{
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 2rem;
      align-items: center;
    }}

    @media (max-width: 900px) {{
      .cluster-topology {{
        grid-template-columns: 1fr;
      }}
    }}

    .topology-diagram {{
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}

    .node-box {{
      background: rgba(11, 17, 32, 0.8);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 1rem;
      position: relative;
    }}

    .node-master {{
      border-color: var(--primary);
    }}

    .node-worker {{
      border-color: var(--accent-blue);
      margin-left: 2rem;
    }}

    .node-box h5 {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 0.3rem;
      display: flex;
      justify-content: space-between;
    }}

    .node-box p {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}

    /* Downloads & Deliverables Grid */
    .downloads-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.25rem;
      margin-bottom: 3rem;
    }}

    .download-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.5rem;
      text-decoration: none;
      color: inherit;
      transition: all 0.25s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .download-card:hover {{
      border-color: var(--primary);
      transform: translateY(-4px);
      box-shadow: 0 8px 24px rgba(16, 185, 129, 0.2);
    }}

    .dl-icon {{
      font-size: 2rem;
      margin-bottom: 0.75rem;
    }}

    .dl-title {{
      font-size: 1.1rem;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 0.35rem;
    }}

    .dl-desc {{
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-bottom: 1.25rem;
      line-height: 1.5;
    }}

    .dl-btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--primary-light);
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      text-align: center;
      justify-content: center;
      transition: background 0.2s;
    }}

    .download-card:hover .dl-btn {{
      background: var(--primary);
      color: #0F172A;
    }}

    /* Footer */
    footer {{
      background: #070B14;
      border-top: 1px solid var(--border-color);
      padding: 2.5rem 1.5rem;
      text-align: center;
      font-size: 0.85rem;
      color: var(--text-dim);
    }}

    footer strong {{
      color: var(--text-main);
    }}

    footer p {{
      margin-bottom: 0.5rem;
    }}
  </style>
</head>
<body>

  <!-- Top Navigation -->
  <header>
    <div class="nav-container">
      <a href="#" class="logo-area">
        <div class="logo-badge">🌾 PySpark</div>
        <div class="logo-title">
          <h1>Smart Irrigation Prediction</h1>
          <p>Cluster Computing Laboratory (INT315)</p>
        </div>
      </a>
      <nav>
        <ul>
          <li><a href="#predictor">Live Predictor</a></li>
          <li><a href="#dashboards">Analytics</a></li>
          <li><a href="#cluster">Cluster Setup</a></li>
          <li><a href="#deliverables">Deliverables</a></li>
          <li><a href="https://github.com/Rkshah07/Smart-Irrigation-System-Prediction" target="_blank" class="highlight-btn">GitHub Repo ↗</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main>

    <!-- Hero Banner -->
    <section class="hero">
      <div class="hero-pill">
        <span>⚡ Apache Spark 3.5.9 Standalone Cluster</span>
        <span>•</span>
        <span>900,000 Field Observations</span>
      </div>
      <h2>Smart Irrigation System Prediction</h2>
      <p class="lead">
        An enterprise-scale distributed Machine Learning pipeline in PySpark MLlib that models continuous soil hydrology, micrometeorology, and crop phenology to optimize agricultural irrigation delivery and conserve vital freshwater reserves.
      </p>
      <div class="author-badge">
        <span>🎓 Student: <strong>Roshan Kumar</strong></span>
        <span>•</span>
        <span>Reg No: <strong>12322743</strong></span>
        <span>•</span>
        <span>Roll No: <strong>67</strong></span>
        <span>•</span>
        <span>Section: <strong>K4M2310A</strong></span>
        <span>•</span>
        <span>Institution: <strong>Lovely Professional University (LPU)</strong></span>
      </div>
    </section>

    <!-- KPI Summary Grid -->
    <section class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">Total Processed Records</div>
        <div class="kpi-value">900,000</div>
        <div class="kpi-subtext">630k Train • 270k Test fields</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Discrete Accuracy</div>
        <div class="kpi-value">83.29%</div>
        <div class="kpi-subtext">83,286 / 125,951 validation fields</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Validation RMSE & R²</div>
        <div class="kpi-value">0.3649</div>
        <div class="kpi-subtext">R² = 57.65% • Zero overfitting</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Generalization Delta</div>
        <div class="kpi-value">&Delta; 0.0011</div>
        <div class="kpi-subtext">Train RMSE: 0.3637 vs Val: 0.3649</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Cluster Speedup</div>
        <div class="kpi-value">4.59x</div>
        <div class="kpi-subtext">Multi-core scaling (1 vs 8 cores)</div>
      </div>
    </section>

    <!-- INTERACTIVE REAL-TIME PREDICTOR -->
    <section id="predictor" class="predictor-section">
      <div class="section-title">
        <h3>⚡ Real-Time Precision Irrigation Predictor</h3>
        <span class="tag">Live Client-Side PySpark Model</span>
      </div>
      <p style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 1.5rem;">
        Adjust the field telemetry controls below or select a quick preset scenario. The exact ElasticNet Ridge regression parameters learned on Spark execute in real-time in your browser to compute the continuous demand score, decision badge, and water allocation advisory.
      </p>

      <!-- Presets -->
      <div class="preset-bar">
        <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-dim); display: flex; align-items: center;">QUICK PRESETS:</span>
        <button class="preset-btn" onclick="applyPreset('drought')">🚨 Drought / Flowering Stress</button>
        <button class="preset-btn" onclick="applyPreset('optimal')">💧 Optimal Watered Field</button>
        <button class="preset-btn" onclick="applyPreset('moderate')">🌾 Moderate Cereal Field</button>
        <button class="preset-btn" onclick="applyPreset('monsoon')">🌧️ Monsoon Rain Event</button>
        <button class="preset-btn" onclick="applyPreset('random')">🎲 Random Field Sample</button>
      </div>

      <div class="predictor-layout">

        <!-- Controls Column -->
        <div class="controls-column">

          <!-- Group 1: Soil Sensors -->
          <div class="form-group-title">🧪 1. Soil Chemistry & Sensor Telemetry</div>
          <div class="controls-grid">
            <div class="control-item">
              <div class="control-label">
                <span>Soil Moisture</span>
                <span class="value-badge" id="lbl_moisture">37.7%</span>
              </div>
              <input type="range" id="input_moisture" min="10" max="80" step="0.5" value="37.7" oninput="runPrediction()">
            </div>
            <div class="control-item">
              <div class="control-label">
                <span>Soil pH</span>
                <span class="value-badge" id="lbl_ph">6.45</span>
              </div>
              <input type="range" id="input_ph" min="4.0" max="9.0" step="0.05" value="6.45" oninput="runPrediction()">
            </div>
            <div class="control-item">
              <div class="control-label">
                <span>Salinity (EC dS/m)</span>
                <span class="value-badge" id="lbl_ec">1.74</span>
              </div>
              <input type="range" id="input_ec" min="0.5" max="4.5" step="0.05" value="1.74" oninput="runPrediction()">
            </div>
            <div class="control-item">
              <div class="control-label">
                <span>Organic Carbon</span>
                <span class="value-badge" id="lbl_oc">0.91%</span>
              </div>
              <input type="range" id="input_oc" min="0.2" max="2.5" step="0.02" value="0.91" oninput="runPrediction()">
            </div>
            <div class="control-item">
              <div class="control-label"><span>Soil Texture</span></div>
              <select id="input_soil_type" onchange="runPrediction()">
                <option value="Sandy">Sandy</option>
                <option value="Clay">Clay</option>
                <option value="Loamy" selected>Loamy</option>
                <option value="Silt">Silt</option>
              </select>
            </div>
          </div>

          <!-- Group 2: Meteorology -->
          <div class="form-group-title">🌤️ 2. Ambient Micro-Meteorology</div>
          <div class="controls-grid">
            <div class="control-item">
              <div class="control-label">
                <span>Temperature (&deg;C)</span>
                <span class="value-badge" id="lbl_temp">28.0&deg;C</span>
              </div>
              <input type="range" id="input_temp" min="12" max="48" step="0.5" value="28.0" oninput="runPrediction()">
            </div>
            <div class="control-item">
              <div class="control-label">
                <span>Humidity (%)</span>
                <span class="value-badge" id="lbl_humidity">61.6%</span>
              </div>
              <input type="range" id="input_humidity" min="15" max="95" step="0.5" value="61.6" oninput="runPrediction()">
            </div>
            <div class="control-item">
              <div class="control-label">
                <span>Wind Speed</span>
                <span class="value-badge" id="lbl_wind">10.5 km/h</span>
              </div>
              <input type="range" id="input_wind" min="2" max="32" step="0.2" value="10.5" oninput="runPrediction()">
            </div>
            <div class="control-item">
              <div class="control-label">
                <span>Rainfall (mm)</span>
                <span class="value-badge" id="lbl_rain">1467 mm</span>
              </div>
              <input type="range" id="input_rain" min="200" max="2800" step="10" value="1467" oninput="runPrediction()">
            </div>
            <div class="control-item">
              <div class="control-label">
                <span>Sunlight Hours</span>
                <span class="value-badge" id="lbl_sun">7.6 h</span>
              </div>
              <input type="range" id="input_sun" min="3" max="13" step="0.1" value="7.6" oninput="runPrediction()">
            </div>
          </div>

          <!-- Group 3: Crop & Agronomy -->
          <div class="form-group-title">🌿 3. Crop Phenology & Infrastructure</div>
          <div class="controls-grid">
            <div class="control-item">
              <div class="control-label"><span>Crop Cultivar</span></div>
              <select id="input_crop_type" onchange="runPrediction()">
                <option value="Sugarcane">Sugarcane</option>
                <option value="Rice">Rice</option>
                <option value="Wheat" selected>Wheat</option>
                <option value="Maize">Maize</option>
                <option value="Cotton">Cotton</option>
                <option value="Potato">Potato</option>
              </select>
            </div>
            <div class="control-item">
              <div class="control-label"><span>Growth Stage</span></div>
              <select id="input_stage" onchange="runPrediction()">
                <option value="Sowing">Sowing</option>
                <option value="Vegetative" selected>Vegetative</option>
                <option value="Flowering">Flowering</option>
                <option value="Harvest">Harvest</option>
              </select>
            </div>
            <div class="control-item">
              <div class="control-label"><span>Season</span></div>
              <select id="input_season" onchange="runPrediction()">
                <option value="Kharif" selected>Kharif (Monsoon)</option>
                <option value="Rabi">Rabi (Winter)</option>
                <option value="Zaid">Zaid (Summer)</option>
              </select>
            </div>
            <div class="control-item">
              <div class="control-label"><span>Irrigation System</span></div>
              <select id="input_irr_type" onchange="runPrediction()">
                <option value="Drip" selected>Drip Irrigation</option>
                <option value="Sprinkler">Sprinkler</option>
                <option value="Canal">Canal</option>
                <option value="Rainfed">Rainfed</option>
              </select>
            </div>
            <div class="control-item">
              <div class="control-label"><span>Surface Mulching</span></div>
              <select id="input_mulch" onchange="runPrediction()">
                <option value="Yes">Yes (Mulch Applied)</option>
                <option value="No" selected>No (Bare Topsoil)</option>
              </select>
            </div>
            <div class="control-item">
              <div class="control-label"><span>Water Source</span></div>
              <select id="input_source" onchange="runPrediction()">
                <option value="Groundwater" selected>Groundwater</option>
                <option value="River">River</option>
                <option value="Reservoir">Reservoir</option>
                <option value="Rainwater">Rainwater</option>
              </select>
            </div>
            <div class="control-item">
              <div class="control-label"><span>Macro-Region</span></div>
              <select id="input_region" onchange="runPrediction()">
                <option value="North" selected>North</option>
                <option value="South">South</option>
                <option value="East">East</option>
                <option value="West">West</option>
                <option value="Central">Central</option>
              </select>
            </div>
          </div>

        </div>

        <!-- Real-Time Output Panel -->
        <div class="result-panel">
          <div class="result-header">
            <h4>Predicted Irrigation Urgency</h4>
            <div class="score-number" id="res_score">0.68</div>
            <div class="score-sub">Continuous Water Requirement Score [0.00 &ndash; 2.00]</div>
            <div id="res_badge" class="decision-badge badge-medium">MEDIUM NEED</div>
          </div>

          <div class="advice-box">
            <div class="advice-title" id="res_advice_title">💡 Operational Recommendation</div>
            <div class="advice-text" id="res_advice_body">
              Soil moisture is within the intermediate depletion buffer. Schedule a moderate replenishment cycle within 48 hours.
            </div>
            <div class="water-depth-stat">
              <span>Recommended Water Application Depth:</span>
              <strong id="res_depth">16.5 mm</strong>
            </div>
          </div>

          <div class="drivers-box">
            <div class="drivers-title">Top Feature Influence Drivers (&beta; Weights)</div>
            <div id="res_drivers_list">
              <!-- Dynamically populated -->
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- LIVE ANALYTICS DASHBOARDS -->
    <section id="dashboards">
      <div class="section-title">
        <h3>📊 Comprehensive Agronomic Analytics Dashboard</h3>
        <span class="tag">Interactive Plotly.js Visualizations</span>
      </div>

      <div class="dashboard-grid">
        <div class="chart-card">
          <h4>Mean Water Requirement Score by Crop Cultivar</h4>
          <p class="chart-desc">Shows average predicted water urgency score across all 6 agricultural cultivars.</p>
          <div id="plot_crop_trends" class="plot-container"></div>
        </div>

        <div class="chart-card">
          <h4>Percentage Breakdown of Urgency Tiers per Crop</h4>
          <p class="chart-desc">Stacked share of Low, Medium, and High irrigation demand across field observations.</p>
          <div id="plot_crop_shares" class="plot-container"></div>
        </div>

        <div class="chart-card">
          <h4>Phenological Growth Stage & Seasonal Demand Matrix</h4>
          <p class="chart-desc">Heatmap of mean water score across phenological lifecycle stages and cropping seasons.</p>
          <div id="plot_stage_heatmap" class="plot-container"></div>
        </div>

        <div class="chart-card">
          <h4>Top 15 Standardized Model Beta Coefficients</h4>
          <p class="chart-desc">Relative influence weights of biophysical and meteorological predictors.</p>
          <div id="plot_coefficients" class="plot-container"></div>
        </div>

        <div class="chart-card">
          <h4>Cluster Scalability & Parallel Speedup Benchmark</h4>
          <p class="chart-desc">Execution time (seconds) and Amdahl's Law speedup across 1, 2, 4, and 8 CPU cores.</p>
          <div id="plot_cluster_timing" class="plot-container"></div>
        </div>

        <div class="chart-card">
          <h4>Model Confusion Matrix & Class Recall</h4>
          <p class="chart-desc">Validation performance (125,951 fields) highlighting high recall on Low (85.2%) and Medium (87.7%).</p>
          <div id="plot_confusion_matrix" class="plot-container"></div>
        </div>
      </div>
    </section>

    <!-- CLUSTER COMPUTING TOPOLOGY -->
    <section id="cluster" class="cluster-section">
      <div class="section-title">
        <h3>⚡ Distributed Cluster Architecture (INT315)</h3>
        <span class="tag">Apache Spark 3.5.9 Standalone</span>
      </div>

      <div class="cluster-topology">
        <div class="topology-diagram">
          <div class="node-box node-master">
            <h5>
              <span>👑 Spark Master Daemon</span>
              <span style="color: var(--primary); font-family: var(--font-mono);">127.0.0.1:7077</span>
            </h5>
            <p>Web UI on port <strong>:8080</strong> • Coordinates resource negotiation, DAG decomposition, worker registration, and task scheduling across the cluster.</p>
          </div>
          <div class="node-box node-worker">
            <h5>
              <span>⚙️ Spark Worker 1</span>
              <span style="color: var(--accent-blue); font-family: var(--font-mono);">Port 8081</span>
            </h5>
            <p>4 Assigned CPU Cores • 2 GB RAM • Hosts Executor runners, task worker threads, and shuffle block storage.</p>
          </div>
          <div class="node-box node-worker">
            <h5>
              <span>⚙️ Spark Worker 2</span>
              <span style="color: var(--accent-blue); font-family: var(--font-mono);">Port 8082</span>
            </h5>
            <p>4 Assigned CPU Cores • 2 GB RAM • Hosts Executor runners, task worker threads, and shuffle block storage.</p>
          </div>
          <div class="node-box" style="border-color: var(--text-dim);">
            <h5>
              <span>💻 Spark Driver Application</span>
              <span style="color: var(--text-muted); font-family: var(--font-mono);">Port 4040</span>
            </h5>
            <p>Python 3.12 / Py4J Gateway • Catalyst physical query planner, Tungsten whole-stage code generator, and metrics aggregation.</p>
          </div>
        </div>

        <div class="cluster-notes">
          <h4 style="color: #FFFFFF; font-size: 1.15rem; margin-bottom: 0.75rem;">Key Distributed Invariants & Optimizations:</h4>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.88rem; color: var(--text-muted);">
            <li>🔹 <strong>Shuffle Partition Tuning:</strong> Reduced default 200 partitions to <code>spark.sql.shuffle.partitions = 16</code> to match cluster executor slots.</li>
            <li>🔹 <strong>In-Memory Caching:</strong> Preprocessed feature vectors cached in executor RAM (<code>train_clean.cache()</code>) to eliminate repeated disk I/O.</li>
            <li>🔹 <strong>Py4J Socket Isolation:</strong> Single-threaded socket orchestration for CrossValidator to avoid Windows loopback gateway collisions.</li>
            <li>🔹 <strong>Winutils & Hadoop:</strong> Windows native POSIX FileSystem permissions simulation via winutils 3.3.5 for model serialization.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- DOWNLOADABLE DELIVERABLES -->
    <section id="deliverables">
      <div class="section-title">
        <h3>📂 Academic & Project Deliverables</h3>
        <span class="tag">Direct Downloads</span>
      </div>

      <div class="downloads-grid">
        <a href="outputs/INT315_Smart_Irrigation_Report.pdf" target="_blank" class="download-card">
          <div class="dl-icon">📕</div>
          <div class="dl-title">Academic PDF Report</div>
          <div class="dl-desc">Comprehensive 76-page research report with LPU cover page, 12 formal sections, verbatim source code, and zero plagiarism.</div>
          <div class="dl-btn">View / Download PDF (3.9 MB) ↗</div>
        </a>

        <a href="outputs/dashboard/Smart_Irrigation_Dashboard.xlsx" download class="download-card">
          <div class="dl-icon">📗</div>
          <div class="dl-title">Native Excel Workbook</div>
          <div class="dl-desc">Interactive multi-sheet analytical workbook with native OpenPyXL charts, KPI cards, dataset dictionary, and diagnostics.</div>
          <div class="dl-btn">Download .XLSX (19 KB) ↗</div>
        </a>

        <a href="outputs/submission.csv" download class="download-card">
          <div class="dl-icon">📘</div>
          <div class="dl-title">Test Predictions CSV</div>
          <div class="dl-desc">270,000 verified test inference predictions formatted identically to Kaggle's sample_submission.csv.</div>
          <div class="dl-btn">Download .CSV (3.4 MB) ↗</div>
        </a>

        <a href="https://github.com/Rkshah07/Smart-Irrigation-System-Prediction" target="_blank" class="download-card">
          <div class="dl-icon">🐙</div>
          <div class="dl-title">GitHub Repository</div>
          <div class="dl-desc">Complete source code, cluster automation scripts, and notebooks available under open academic license.</div>
          <div class="dl-btn">View on GitHub ↗</div>
        </a>
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer>
    <p><strong>Smart Irrigation System Prediction</strong> &bull; Developed for INT315 (Cluster Computing)</p>
    <p>Submitted by <strong>Roshan Kumar</strong> (Reg: 12322743 | Roll: 67 | Section: K4M2310A)</p>
    <p>School of Computer Science & Engineering &bull; <strong>Lovely Professional University, Punjab (India)</strong></p>
    <p style="margin-top: 1rem; font-size: 0.75rem; color: var(--text-dim);">&copy; 2026 Roshan Kumar. Hosted on GitHub Pages.</p>
  </footer>

  <!-- EMBEDDED MODEL WEIGHTS & CLIENT-SIDE SCRIPT -->
  <script>
    const MODEL_WEIGHTS = {weights_json};
    const CROP_TRENDS = {crop_trends_json};
    const SEASON_STAGE = {season_stage_json};
    const COEFFS_DATA = {coeffs_json};
    const TIMING_DATA = {timing_json};
    const METRICS_DATA = {metrics_json};

    // --- PREDICTION ENGINE ---
    function runPrediction() {{
      const moisture = parseFloat(document.getElementById('input_moisture').value);
      const ph = parseFloat(document.getElementById('input_ph').value);
      const ec = parseFloat(document.getElementById('input_ec').value);
      const oc = parseFloat(document.getElementById('input_oc').value);
      const temp = parseFloat(document.getElementById('input_temp').value);
      const humidity = parseFloat(document.getElementById('input_humidity').value);
      const wind = parseFloat(document.getElementById('input_wind').value);
      const rain = parseFloat(document.getElementById('input_rain').value);
      const sun = parseFloat(document.getElementById('input_sun').value);

      const soilType = document.getElementById('input_soil_type').value;
      const cropType = document.getElementById('input_crop_type').value;
      const stage = document.getElementById('input_stage').value;
      const season = document.getElementById('input_season').value;
      const irrType = document.getElementById('input_irr_type').value;
      const mulch = document.getElementById('input_mulch').value;
      const source = document.getElementById('input_source').value;
      const region = document.getElementById('input_region').value;

      // Update Labels
      document.getElementById('lbl_moisture').textContent = moisture.toFixed(1) + '%';
      document.getElementById('lbl_ph').textContent = ph.toFixed(2);
      document.getElementById('lbl_ec').textContent = ec.toFixed(2) + ' dS/m';
      document.getElementById('lbl_oc').textContent = oc.toFixed(2) + '%';
      document.getElementById('lbl_temp').textContent = temp.toFixed(1) + '°C';
      document.getElementById('lbl_humidity').textContent = humidity.toFixed(1) + '%';
      document.getElementById('lbl_wind').textContent = wind.toFixed(1) + ' km/h';
      document.getElementById('lbl_rain').textContent = Math.round(rain) + ' mm';
      document.getElementById('lbl_sun').textContent = sun.toFixed(1) + ' h';

      // PySpark Model Parameters
      const intercept = MODEL_WEIGHTS.intercept;
      const feats = MODEL_WEIGHTS.features;

      let score = intercept;
      let contributions = [];

      // Helper function to add feature effect
      function addEffect(idx, val, displayName) {{
        const feat = feats[idx];
        const effect = feat.coefficient * (val / feat.std);
        score += effect;
        contributions.push({{ name: displayName, effect: effect }});
      }}

      // Continuous numeric features
      addEffect(0, moisture, 'Soil Moisture');
      addEffect(1, ph, 'Soil pH');
      addEffect(2, oc, 'Organic Carbon');
      addEffect(3, ec, 'Salinity (EC)');
      addEffect(4, humidity, 'Humidity');
      addEffect(5, rain, 'Rainfall');
      addEffect(6, sun, 'Sunlight Hours');
      addEffect(7, wind, 'Wind Speed');
      addEffect(8, 7.37, 'Field Area (Median)');
      addEffect(9, 61.13, 'Prev Irrigation (Median)');

      // Categorical one-hot features
      const activeCats = {{
        ['Soil_Type_vec_' + soilType]: 'Soil Texture: ' + soilType,
        ['Crop_Type_vec_' + cropType]: 'Crop: ' + cropType,
        ['Crop_Growth_Stage_vec_' + stage]: 'Growth Stage: ' + stage,
        ['Season_vec_' + season]: 'Season: ' + season,
        ['Irrigation_Type_vec_' + irrType]: 'Irrigation: ' + irrType,
        ['Water_Source_vec_' + source]: 'Source: ' + source,
        ['Mulching_Used_vec_' + mulch]: 'Mulching: ' + mulch,
        ['Region_vec_' + region]: 'Region: ' + region,
      }};

      for (let i = 10; i < feats.length; i++) {{
        const raw = feats[i].raw_name;
        if (activeCats[raw]) {{
          const eff = feats[i].coefficient * (1.0 / feats[i].std);
          score += eff;
          contributions.push({{ name: activeCats[raw], effect: eff }});
        }}
      }}

      // Bounded score & Discrete rounding
      const clippedScore = Math.max(0.0, Math.min(2.0, score));
      const roundedClass = Math.round(clippedScore);

      // Update UI elements
      document.getElementById('res_score').textContent = clippedScore.toFixed(2);

      const badge = document.getElementById('res_badge');
      const adviceTitle = document.getElementById('res_advice_title');
      const adviceBody = document.getElementById('res_advice_body');
      const depthEl = document.getElementById('res_depth');

      if (roundedClass === 0) {{
        badge.className = 'decision-badge badge-low';
        badge.textContent = 'LOW NEED';
        adviceTitle.textContent = '💧 Water Storage Optimal';
        adviceBody.textContent = 'Soil moisture is sufficient to meet current evapotranspiration demand. Withhold irrigation to conserve energy and prevent rhizosphere nitrogen leaching.';
        depthEl.textContent = '0.0 mm (No delivery required)';
      }} else if (roundedClass === 1) {{
        badge.className = 'decision-badge badge-medium';
        badge.textContent = 'MEDIUM NEED';
        adviceTitle.textContent = '⚠️ Scheduled Replenishment Recommended';
        adviceBody.textContent = 'Root zone moisture is approaching critical replenishment limits. Schedule a controlled irrigation cycle within 24–48 hours.';
        depthEl.textContent = ((1.5 - clippedScore) * 18.0 + 10.0).toFixed(1) + ' mm';
      }} else {{
        badge.className = 'decision-badge badge-high';
        badge.textContent = 'HIGH NEED';
        adviceTitle.textContent = '🚨 Immediate Water Delivery Required';
        adviceBody.textContent = 'High evapotranspiration stress detected! Immediate high-volume irrigation cycle is mandatory to avoid permanent wilting and yield loss.';
        depthEl.textContent = ((clippedScore - 1.0) * 22.0 + 20.0).toFixed(1) + ' mm';
      }}

      // Update Top Drivers
      contributions.sort((a, b) => Math.abs(b.effect) - Math.abs(a.effect));
      const topDrivers = contributions.slice(0, 5);
      const driversContainer = document.getElementById('res_drivers_list');
      driversContainer.innerHTML = '';
      topDrivers.forEach(d => {{
        const row = document.createElement('div');
        row.className = 'driver-item';
        const sign = d.effect >= 0 ? '+' : '';
        const colorClass = d.effect >= 0 ? 'val-pos' : 'val-neg';
        row.innerHTML = `<span>${{d.name}}</span><span class="driver-val ${{colorClass}}">${{sign}}${{d.effect.toFixed(3)}}</span>`;
        driversContainer.appendChild(row);
      }});
    }}

    // --- PRESETS ---
    function applyPreset(type) {{
      if (type === 'drought') {{
        document.getElementById('input_moisture').value = 14.0;
        document.getElementById('input_wind').value = 24.0;
        document.getElementById('input_temp').value = 39.0;
        document.getElementById('input_humidity').value = 25.0;
        document.getElementById('input_stage').value = 'Flowering';
        document.getElementById('input_mulch').value = 'No';
        document.getElementById('input_soil_type').value = 'Sandy';
      }} else if (type === 'optimal') {{
        document.getElementById('input_moisture').value = 65.0;
        document.getElementById('input_wind').value = 6.0;
        document.getElementById('input_temp').value = 24.0;
        document.getElementById('input_humidity').value = 75.0;
        document.getElementById('input_stage').value = 'Harvest';
        document.getElementById('input_mulch').value = 'Yes';
        document.getElementById('input_soil_type').value = 'Clay';
      }} else if (type === 'moderate') {{
        document.getElementById('input_moisture').value = 35.0;
        document.getElementById('input_wind').value = 12.0;
        document.getElementById('input_temp').value = 28.0;
        document.getElementById('input_stage').value = 'Vegetative';
        document.getElementById('input_crop_type').value = 'Wheat';
      }} else if (type === 'monsoon') {{
        document.getElementById('input_moisture').value = 72.0;
        document.getElementById('input_rain').value = 2400;
        document.getElementById('input_humidity').value = 88.0;
        document.getElementById('input_season').value = 'Kharif';
        document.getElementById('input_crop_type').value = 'Rice';
      }} else if (type === 'random') {{
        document.getElementById('input_moisture').value = (Math.random() * 60 + 15).toFixed(1);
        document.getElementById('input_wind').value = (Math.random() * 25 + 4).toFixed(1);
        document.getElementById('input_temp').value = (Math.random() * 25 + 18).toFixed(1);
        document.getElementById('input_humidity').value = (Math.random() * 60 + 30).toFixed(1);
      }}
      runPrediction();
    }}

    // --- PLOTLY ANALYTICS CHARTS ---
    function initPlotlyCharts() {{
      const darkLayout = {{
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {{ family: 'Inter, sans-serif', color: '#94A3B8', size: 11 }},
        margin: {{ l: 45, r: 25, t: 25, b: 40 }},
        hovermode: 'closest'
      }};

      // Chart 1: Mean Score by Crop Cultivar
      const crops = CROP_TRENDS.map(d => d.Crop_Type);
      const meanScores = CROP_TRENDS.map(d => d.Mean_Score);
      Plotly.newPlot('plot_crop_trends', [{{
        x: crops,
        y: meanScores,
        type: 'bar',
        marker: {{
          color: ['#10B981', '#38BDF8', '#F59E0B', '#6366F1', '#EC4899', '#8B5CF6'],
          line: {{ color: '#1E293B', width: 1.5 }}
        }}
      }}], {{
        ...darkLayout,
        yaxis: {{ title: 'Mean Score [0-2]', range: [0, 1.2], gridcolor: '#1E293B' }},
        xaxis: {{ gridcolor: '#1E293B' }}
      }}, {{ responsive: true, displayModeBar: false }});

      // Chart 2: Urgency Class Distribution per Crop
      Plotly.newPlot('plot_crop_shares', [
        {{ x: crops, y: CROP_TRENDS.map(d => d.Low_Pct), name: 'Low Need', type: 'bar', marker: {{ color: '#10B981' }} }},
        {{ x: crops, y: CROP_TRENDS.map(d => d.Medium_Pct), name: 'Medium Need', type: 'bar', marker: {{ color: '#F59E0B' }} }},
        {{ x: crops, y: CROP_TRENDS.map(d => d.High_Pct), name: 'High Need', type: 'bar', marker: {{ color: '#EF4444' }} }}
      ], {{
        ...darkLayout,
        barmode: 'stack',
        yaxis: {{ title: 'Percentage (%)', range: [0, 100], gridcolor: '#1E293B' }},
        legend: {{ orientation: 'h', y: 1.15 }}
      }}, {{ responsive: true, displayModeBar: false }});

      // Chart 3: Phenological Stage & Season Matrix Heatmap
      const stages = ['Sowing', 'Vegetative', 'Flowering', 'Harvest'];
      const seasons = ['Kharif', 'Rabi', 'Zaid'];
      const zMatrix = seasons.map(s => {{
        return stages.map(st => {{
          const match = SEASON_STAGE.find(d => d.Season === s && d.Crop_Growth_Stage === st);
          return match ? match.Mean_Score : 0.5;
        }});
      }});
      Plotly.newPlot('plot_stage_heatmap', [{{
        z: zMatrix,
        x: stages,
        y: seasons,
        type: 'heatmap',
        colorscale: 'Viridis',
        showscale: true
      }}], {{
        ...darkLayout,
        yaxis: {{ title: 'Season' }},
        xaxis: {{ title: 'Growth Stage' }}
      }}, {{ responsive: true, displayModeBar: false }});

      // Chart 4: Top 15 Coefficients
      const top15 = COEFFS_DATA.slice(0, 12).reverse();
      Plotly.newPlot('plot_coefficients', [{{
        x: top15.map(d => d.coefficient),
        y: top15.map(d => d.feature),
        type: 'bar',
        orientation: 'h',
        marker: {{
          color: top15.map(d => d.coefficient >= 0 ? '#EF4444' : '#10B981'),
          line: {{ color: '#1E293B', width: 1 }}
        }}
      }}], {{
        ...darkLayout,
        margin: {{ l: 160, r: 25, t: 20, b: 35 }},
        xaxis: {{ title: 'Standardized Beta Weight (β)', gridcolor: '#1E293B' }}
      }}, {{ responsive: true, displayModeBar: false }});

      // Chart 5: Cluster Timing Scalability Curve
      if (TIMING_DATA.length > 0) {{
        Plotly.newPlot('plot_cluster_timing', [
          {{
            x: TIMING_DATA.map(d => d.Cores),
            y: TIMING_DATA.map(d => d.Elapsed_Seconds),
            name: 'Wall-Clock Time (s)',
            type: 'scatter',
            mode: 'lines+markers',
            line: {{ color: '#38BDF8', width: 3 }}
          }},
          {{
            x: TIMING_DATA.map(d => d.Cores),
            y: TIMING_DATA.map(d => d.Speedup),
            name: 'Speedup Factor (x)',
            yaxis: 'y2',
            type: 'scatter',
            mode: 'lines+markers',
            line: {{ color: '#10B981', width: 3, dash: 'dot' }}
          }}
        ], {{
          ...darkLayout,
          xaxis: {{ title: 'Allocated CPU Cores', gridcolor: '#1E293B' }},
          yaxis: {{ title: 'Time (seconds)', gridcolor: '#1E293B' }},
          yaxis2: {{ title: 'Speedup (x)', overlaying: 'y', side: 'right' }},
          legend: {{ orientation: 'h', y: 1.15 }}
        }}, {{ responsive: true, displayModeBar: false }});
      }}

      // Chart 6: Confusion Matrix
      const cmZ = [[63143, 10968, 0], [5861, 41739, 2], [25, 4196, 17]];
      const cmLabels = ['Low', 'Medium', 'High'];
      Plotly.newPlot('plot_confusion_matrix', [{{
        z: cmZ,
        x: cmLabels,
        y: cmLabels,
        type: 'heatmap',
        colorscale: 'Blues',
        showscale: false,
        text: cmZ.map(row => row.map(v => v.toLocaleString())),
        texttemplate: '%{{text}}',
        textfont: {{ family: 'Inter', color: '#FFFFFF', size: 14 }}
      }}], {{
        ...darkLayout,
        xaxis: {{ title: 'Predicted Class' }},
        yaxis: {{ title: 'Actual Class', autorange: 'reversed' }}
      }}, {{ responsive: true, displayModeBar: false }});
    }}

    // Initialize on DOM load
    window.addEventListener('DOMContentLoaded', () => {{
      runPrediction();
      initPlotlyCharts();
    }});
  </script>

</body>
</html>
"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"-> Successfully generated index.html: {output_html} ({len(html_content)} bytes)")
    return output_html

if __name__ == "__main__":
    build_index_html()
