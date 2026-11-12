"""
download_dataset.py
-------------------
Utility script to download the Kaggle Playground Series S6E4 dataset
(train.csv and test.csv) for local execution of the PySpark pipeline.

Usage:
  python download_dataset.py

Prerequisites:
  kaggle API credentials in ~/.kaggle/kaggle.json
  or manual download from:
  https://www.kaggle.com/competitions/playground-series-s6e4/data
"""

import os
import subprocess

def download_data():
    data_dir = os.path.dirname(os.path.abspath(__file__))
    train_path = os.path.join(data_dir, "train.csv")
    test_path = os.path.join(data_dir, "test.csv")

    if os.path.exists(train_path) and os.path.exists(test_path):
        print(f"-> Datasets already present in: {data_dir}")
        print(f"   train.csv: {os.path.getsize(train_path) / (1024*1024):.2f} MB")
        print(f"   test.csv:  {os.path.getsize(test_path) / (1024*1024):.2f} MB")
        return

    print("-> Downloading Kaggle Playground Series S6E4 dataset...")
    try:
        subprocess.run([
            "kaggle", "competitions", "download",
            "-c", "playground-series-s6e4",
            "-p", data_dir
        ], check=True)
        print("-> Unzipping playground-series-s6e4.zip...")
        import zipfile
        zip_path = os.path.join(data_dir, "playground-series-s6e4.zip")
        if os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(data_dir)
            os.remove(zip_path)
            print("-> Successfully extracted train.csv and test.csv!")
    except Exception as e:
        print(f"-> Automatic Kaggle download failed: {e}")
        print("   Please download manually from:")
        print("   https://www.kaggle.com/competitions/playground-series-s6e4/data")
        print(f"   and place train.csv & test.csv in: {data_dir}")

if __name__ == "__main__":
    download_data()
