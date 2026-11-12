"""
spark_session.py
----------------
Manages SparkSession creation and environment configuration for the
Smart Irrigation System Prediction project.
"""

import os
import sys
from pyspark.sql import SparkSession


def get_spark_session(app_name: str = "SmartIrrigationPrediction", memory: str = "3g", master: str = "local[*]") -> SparkSession:
    """
    Initializes and returns a configured SparkSession.

    Configures local Hadoop binaries (winutils) if available, ensures
    sufficient driver memory, and applies recommended JVM options.
    """
    # Configure HADOOP_HOME for Windows compatibility if present
    possible_hadoop_dirs = [
        r"D:\hadoop",
        r"C:\hadoop",
        os.path.join(os.path.dirname(__file__), "..", "hadoop"),
    ]
    for hadoop_dir in possible_hadoop_dirs:
        if os.path.exists(os.path.join(hadoop_dir, "bin", "winutils.exe")):
            os.environ["HADOOP_HOME"] = os.path.abspath(hadoop_dir)
            hadoop_bin = os.path.join(os.environ["HADOOP_HOME"], "bin")
            if hadoop_bin not in os.environ.get("PATH", ""):
                os.environ["PATH"] = hadoop_bin + os.pathsep + os.environ.get("PATH", "")
            break

    # Java 21 & Memory JVM options
    java_options = (
        "--add-opens=java.base/java.lang=ALL-UNNAMED "
        "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED "
        "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED "
        "--add-opens=java.base/java.io=ALL-UNNAMED "
        "--add-opens=java.base/java.net=ALL-UNNAMED "
        "--add-opens=java.base/java.nio=ALL-UNNAMED "
        "--add-opens=java.base/java.util=ALL-UNNAMED "
        "--add-opens=java.base/java.util.concurrent=ALL-UNNAMED "
        "--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED "
        "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED "
        "-Djava.net.preferIPv4Stack=true"
    )

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.memory", memory)
        .config("spark.executor.memory", memory)
        .config("spark.driver.extraJavaOptions", java_options)
        .config("spark.executor.extraJavaOptions", java_options)
        .config("spark.sql.shuffle.partitions", "16")
        .config("spark.default.parallelism", "8")
        .config("spark.sql.execution.arrow.pyspark.enabled", "false")
        .config("spark.ui.enabled", "true")
        .config("spark.ui.port", "4040")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")
    return spark
