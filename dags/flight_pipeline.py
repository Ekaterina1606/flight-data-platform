
import os
from datetime import datetime
from pathlib import Path

import psycopg2

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


PROJECT_DIR = Path("/opt/airflow")


def execute_sql_file(filename):
    """Execute an SQL file against the flight database."""
    sql_path = PROJECT_DIR / "sql" / filename
    sql = sql_path.read_text(encoding="utf-8")

    connection = psycopg2.connect(
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
    )

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
    finally:
        connection.close()


with DAG(
    dag_id="flight_data_pipeline",
    description="ETL pipeline for flight data",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["flights", "etl", "postgres"],
) as dag:

    extract_flights = BashOperator(
        task_id="extract_flights",
        bash_command="cd /opt/airflow && python ingestion/extract_flights.py",
    )

    load_raw = BashOperator(
        task_id="load_raw",
        bash_command="cd /opt/airflow && python ingestion/load_flights.py",
    )

    load_staging = PythonOperator(
        task_id="load_staging",
        python_callable=execute_sql_file,
        op_kwargs={"filename": "02_load_staging.sql"},
    )

    staging_quality = PythonOperator(
        task_id="staging_quality",
        python_callable=execute_sql_file,
        op_kwargs={"filename": "03_data_quality.sql"},
    )

    load_dwh = PythonOperator(
        task_id="load_dwh",
        python_callable=execute_sql_file,
        op_kwargs={"filename": "05_load_dwh.sql"},
    )

    dwh_quality = PythonOperator(
        task_id="dwh_quality",
        python_callable=execute_sql_file,
        op_kwargs={"filename": "06_dwh_quality.sql"},
    )

    (
        extract_flights
        >> load_raw
        >> load_staging
        >> staging_quality
        >> load_dwh
        >> dwh_quality
    )
