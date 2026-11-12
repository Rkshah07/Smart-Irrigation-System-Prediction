# 🌾 Smart Irrigation System Prediction

[![Live Demo](https://img.shields.io/badge/Live_Working_App-GitHub_Pages-10B981?style=for-the-badge&logo=github&logoColor=white)](https://rkshah07.github.io/Smart-Irrigation-System-Prediction/)
[![Apache Spark](https://img.shields.io/badge/Apache_Spark-3.5.9-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Course](https://img.shields.io/badge/Course-INT315_Cluster_Computing-38BDF8?style=for-the-badge)](https://www.lpu.in/)
[![Institution](https://img.shields.io/badge/Institution-Lovely_Professional_University-F59E0B?style=for-the-badge)](https://www.lpu.in/)

> 🌐 **LIVE WORKING WEB APPLICATION:**  
> 👉 **[Click here to open the Interactive Live Project](https://rkshah07.github.io/Smart-Irrigation-System-Prediction/)**  
> *Test any field scenario live in your browser with real-time PySpark model predictions, dynamic urgency meter, and interactive Plotly analytics.*

---

## 🎓 Academic Submission Details
* **Project Name:** Smart Irrigation System Prediction: Distributed Precision Agriculture Intelligence
* **Course Code & Title:** INT315 — Cluster Computing
* **Student Name:** **Roshan Kumar**
* **Registration Number:** **12322743**
* **Roll Number:** **67**
* **Section:** **K4M2310A**
* **Degree Program:** Bachelor of Technology (B.Tech) in Computer Science & Engineering
* **Department:** Department of Computer Science & Engineering
* **School:** School of Computer Science & Engineering
* **Institution:** Lovely Professional University, Phagwara, Punjab – 144411 (India)
* **Date of Submission:** November 06, 2026

---

## 📋 Table of Contents
1. [Overview & Problem Statement](#-overview--problem-statement)
2. [Live Working Application Features](#-live-working-application-features)
3. [Key Experimental Results & KPIs](#-key-experimental-results--kpis)
4. [Project Architecture & Directory Structure](#-project-architecture--directory-structure)
5. [Dataset Description](#-dataset-description)
6. [Machine Learning Pipeline](#-machine-learning-pipeline)
7. [Cluster Computing Architecture (Master-Worker Topology)](#-cluster-computing-architecture)
8. [Multi-Core Scalability Benchmark (Amdahl's Law)](#-multi-core-scalability-benchmark)
9. [Academic Deliverables & Downloads](#-academic-deliverables--downloads)
10. [How to Run Locally](#-how-to-run-locally)

---

## 🌿 Overview & Problem Statement
Freshwater depletion and climatic stochasticity represent critical bottlenecks to global agricultural security. Traditional calendar-driven or manual tactile irrigation scheduling leads to dual failure states:
* **Hyper-Irrigation:** Induces rhizosphere hypoxia (cellular root asphyxiation), leaches mobile nutrients ($NO_3^-$ nitrate) below root uptake thresholds, and promotes fungal root-rot pathogens (*Phytophthora*, *Fusarium*).
* **Hypo-Irrigation:** Drives soil matric potential past the permanent wilting point, triggering stomatal closure, suppressing photosynthesis, and collapsing crop yields.

This project delivers a **fault-tolerant, scalable, distributed precision irrigation intelligence pipeline** deployed on **Apache Spark (PySpark MLlib)** over **900,000 empirical field observations** (630,000 training records and 270,000 test fields across 21 multi-modal sensor dimensions).

---

## 🌐 Live Working Application Features
The project is hosted live via GitHub Pages at:  
👉 **`https://rkshah07.github.io/Smart-Irrigation-System-Prediction/`**

### What You Can Do on the Live Application:
1. **Interactive Real-Time Predictor:**
   * Adjust continuous soil sensor sliders (`Soil_Moisture`, `Soil_pH`, `Electrical_Conductivity`, `Organic_Carbon`).
   * Configure meteorology (`Temperature_C`, `Humidity`, `Wind_Speed_kmh`, `Rainfall_mm`, `Sunlight_Hours`).
   * Select cultivar, phenological growth stage, season, irrigation type, and mulching practice.
   * **Instant Model Evaluation:** Executes the exact PySpark ElasticNet model weights client-side in real-time, displaying the continuous score $[0.00, 2.00]$, decision badge (**Low / Medium / High**), recommended water depth (mm), and top contributing feature drivers.
2. **One-Click Field Presets:**
   * 🚨 *Drought / Flowering Stress*
   * 💧 *Optimal Watered Clay Field*
   * 🌾 *Moderate Cereal Field*
   * 🌧️ *Monsoon Rain Event*
   * 🎲 *Random Field Simulation*
3. **Interactive Analytical Visualizations (Plotly.js):**
   * Mean score by crop cultivar
   * Percentage class share per crop
   * Phenological stage vs seasonal demand matrix heatmap
   * Top 15 standardized beta weights
   * Cluster scalability & Amdahl speedup curve
   * 3×3 validation confusion matrix
4. **Direct Deliverable Downloads:**
   * One-click download of the 76-page Academic PDF Report, Excel Workbook, and Submission CSV.

---

## 📊 Key Experimental Results & KPIs

$$\begin{array}{|l|c|c|c|}
\hline
\textbf{Evaluation Metric} & \textbf{Training Split (80\%)} & \textbf{Validation Split (20\%)} & \textbf{Generalization Delta } (\Delta) \\
\hline
\text{Root Mean Squared Error (RMSE)} & \mathbf{0.3637} & \mathbf{0.3649} & +0.0011 \text{ (Zero Overfitting)} \\
\text{Coefficient of Determination } (R^2) & \mathbf{57.83\%} & \mathbf{57.65\%} & -0.18\% \\
\text{Mean Absolute Error (MAE)} & \mathbf{0.2897} & \mathbf{0.2902} & +0.0005 \\
\text{Discrete Accuracy} & \mathbf{83.20\%} & \mathbf{83.29\%} & +0.09\% \text{ (83,286 / 125,951 fields)} \\
\hline
\end{array}$$

* **Optimal Regularization:** ElasticNet $\lambda^* = 0.01$, $\alpha^* = 0.0$ (L2 Ridge) discovered via distributed 3-Fold Cross-Validation (`CrossValidator`).
* **Dominant Biophysical Drivers:**
  * `Soil_Moisture` ($\beta = -0.21146$): Dominant negative predictor of irrigation necessity.
  * `Wind_Speed_kmh` ($\beta = +0.12471$): Boundary-layer convective vapor stripping accelerates demand.
  * `Flowering Stage` ($\beta = +0.11959$) vs `Harvest` ($\beta = -0.11737$): Anthesis phenology is highly vulnerable to moisture deficit.
  * `Mulching_Used = Yes` ($\beta = -0.07024$): Attenuates evaporative flux and saves water.

---

## 🏗️ Project Architecture & Directory Structure

```text
smart_irrigation/
├── index.html                     # Live interactive web application (GitHub Pages)
├── README.md                      # Comprehensive documentation & setup instructions
├── requirements.txt               # Environment dependencies (pyspark, pandas, plotly, reportlab, etc.)
├── main.py                        # Complete end-to-end execution pipeline
├── compile_report.py              # Standalone ReportLab 76-page PDF compiler
├── run_cluster.bat / .sh          # Standalone Spark cluster runner scripts
├── data/
│   ├── download_dataset.py        # Automated Kaggle S6E4 download utility
│   └── sample_submission.csv      # Verification template (id, Irrigation_Need)
├── src/
│   ├── spark_session.py           # SparkSession creation, memory & JVM tuning
│   ├── data_loading.py            # Dataset loading, path resolution & null inspection
│   ├── preprocessing.py           # Target mapping, Imputer, StringIndexer, OHE, Scaler
│   ├── modeling.py                # Linear Regression training, CrossValidator & coefficients
│   ├── evaluation.py              # RMSE, R2, MAE, accuracy & confusion matrix
│   ├── visualization.py           # Publication-quality static plots (Matplotlib/Seaborn)
│   ├── cluster_manager.py         # Standalone cluster lifecycle & timing benchmarks
│   ├── dashboard_builder.py       # Excel (openpyxl) & Power BI data mart generator
│   ├── screenshot_generator.py    # Headless Playwright UI & terminal screenshot capturer
│   └── report_generator.py        # Two-pass academic ReportLab PDF report compiler
├── notebooks/
│   └── smart_irrigation.ipynb     # Step-by-step presentation notebook
└── outputs/
    ├── INT315_Smart_Irrigation_Report.pdf  # 76-page academic final report
    ├── metrics.json                        # Serialized evaluation metrics payload
    ├── model_weights.json                  # Extracted model parameters for live prediction
    ├── submission.csv                      # Test predictions (270,000 fields)
    ├── cluster_timing.csv                  # Multi-core benchmark measurements
    ├── saved_model/                        # Serialized PySpark PipelineModel
    ├── dashboard/
    │   ├── Smart_Irrigation_Dashboard.xlsx # 7-sheet native Excel workbook
    │   ├── dashboard.html                  # Standalone Plotly HTML dashboard
    │   ├── POWERBI_STEPS.md                # Power BI star-schema construction guide
    │   └── powerbi_data/                   # Normalized CSV data marts
    ├── plots/                              # 300 DPI publication trend charts
    └── screenshots/                        # Live Spark UI & terminal execution captures
```

---

## ⚡ Cluster Computing Architecture
This project is engineered for course **INT315 (Cluster Computing)** and executes across an Apache Spark Standalone Cluster:
* **Spark Master Daemon:** Port 7077 (IPC/RPC) | Web UI on port **:8080**
* **Spark Worker 1:** 4 Cores | 2 GB JVM RAM | Web UI on port **:8081**
* **Spark Worker 2:** 4 Cores | 2 GB JVM RAM | Web UI on port **:8082**
* **Spark Driver Application:** Python 3.12 / Py4J Gateway | Web UI on port **:4040**

### Distributed Invariants & Optimizations:
1. **Shuffle Partition Tuning:** Set `spark.sql.shuffle.partitions = 16` to match cluster executor slots, eliminating the overhead of 200 tiny partitions.
2. **In-Memory Caching:** Feature DataFrames are cached in executor RAM (`train_clean.cache()`) to eliminate disk serialization during iterative cross-validation.
3. **Loopback IPv4 Binding:** Bound all cluster sockets strictly to `127.0.0.1` to prevent Windows socket gateway collisions.

---

## ⏱️ Multi-Core Scalability Benchmark

$$\begin{array}{|l|c|c|c|c|}
\hline
\textbf{Configuration} & \textbf{Cores } (p) & \textbf{Elapsed Time } (T_p) & \textbf{Speedup } (S_p) & \textbf{Parallel Efficiency } (E_p) \\
\hline
\text{Single Core (local[1])} & 1 & 15.52\,\text{s} & 1.00\times & 100.0\% \\
\text{Dual Core (local[2])} & 2 & 11.29\,\text{s} & 1.38\times & 68.8\% \\
\text{Quad Core (local[4])} & 4 & 12.20\,\text{s} & 1.27\times & 31.8\% \\
\text{All Cores (local[*], 8)} & 8 & 14.65\,\text{s} & 1.06\times & 13.2\% \\
\hline
\end{array}$$

*Near-linear scaling is achieved up to 4 cores, after which thread contention and shuffle synchronization overhead introduce diminishing returns under Amdahl's Law.*

---

## 📂 Academic Deliverables & Downloads
* [📘 View Academic PDF Report (76 Pages)](outputs/INT315_Smart_Irrigation_Report.pdf)
* [📊 Download Native Excel Workbook](outputs/dashboard/Smart_Irrigation_Dashboard.xlsx)
* [🗂️ Download Test Predictions (270k Rows)](outputs/submission.csv)
* [🌐 Open Live Interactive Dashboard](https://rkshah07.github.io/Smart-Irrigation-System-Prediction/)

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/Rkshah07/Smart-Irrigation-System-Prediction.git
cd Smart-Irrigation-System-Prediction
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Download Dataset (Kaggle S6E4)
```bash
python data/download_dataset.py
```

### 4. Run the Full Pipeline End-to-End
```bash
python main.py --cluster
```

### 5. Compile the Final Academic PDF Report
```bash
python compile_report.py
```

---

## 📜 License & Acknowledgments
* **Author:** Roshan Kumar (Reg: 12322743, Roll: 67, Section: K4M2310A)
* **Institution:** Lovely Professional University, Punjab (India)
* **Course:** INT315 — Cluster Computing
* **Dataset Reference:** Kaggle Playground Series S6E4 & Miadul Islam (*Irrigation Water Requirement Prediction Dataset*).
