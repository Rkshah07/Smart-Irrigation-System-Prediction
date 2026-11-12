@echo off
REM run_cluster.bat
REM ---------------
REM Launches the Spark Standalone Cluster and runs main.py

echo ======================================================================
echo Starting Apache Spark Standalone Cluster (1 Master + 2 Workers)
echo ======================================================================

python main.py --cluster --memory 6g --seed 42

echo Pipeline execution finished successfully on Spark cluster.
pause
