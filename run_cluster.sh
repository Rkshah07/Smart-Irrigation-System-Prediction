#!/usr/bin/env bash
# run_cluster.sh
# --------------
# Launches the Spark Standalone Cluster (1 Master + 2 Workers)
# and executes the Smart Irrigation System prediction pipeline.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================================"
echo "Starting Apache Spark Standalone Cluster (1 Master + 2 Workers)"
echo "======================================================================"

# Run main pipeline with standalone cluster mode enabled
python main.py --cluster --memory 6g --seed 42

echo "Pipeline execution finished successfully on Spark cluster."
