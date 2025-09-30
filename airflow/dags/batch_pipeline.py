
from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.bash import BashOperator

# Schedule: run monthly; a separate quarterly aggregation step is toggled via env
default_args = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="batch_ingest_process_publish",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@monthly",
    catchup=False,
    default_args=default_args,
    tags=["batch", "phase1"],
) as dag:

    # Ingestion (container is already up; we run it once using docker compose)
    ingest = BashOperator(
        task_id="ingest_to_raw",
        bash_command="docker compose run --rm ingest python /app/app.py",
    )

    # Spark ETL
    spark_process = BashOperator(
        task_id="spark_etl_curated_agg",
        bash_command="make spark-submit",
    )

    # (Optional) Post publish notification (no-op placeholder)
    notify = BashOperator(
        task_id="notify_delivery_api",
        bash_command="echo 'Notify delivery API to refresh cache'",
    )

    ingest >> spark_process >> notify
