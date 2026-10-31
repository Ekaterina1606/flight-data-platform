
import subprocess
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_CONTAINER = os.getenv("POSTGRES_CONTAINER")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")

required_settings = {
    "POSTGRES_CONTAINER": POSTGRES_CONTAINER,
    "POSTGRES_USER": POSTGRES_USER,
    "POSTGRES_DB": POSTGRES_DB,
}

missing_settings = [
    name
    for name, value in required_settings.items()
    if not value
]

if missing_settings:
    raise ValueError(
        f"Missing environment settings: {', '.join(missing_settings)}"
    )

PROJECT_DIR = Path(__file__).resolve().parent


def run_python(script_name):
    script_path = PROJECT_DIR / "ingestion" / script_name

    print(f"\n[START] Running {script_name}", flush=True)

    subprocess.run(

        [sys.executable, str(script_path)],
        cwd=PROJECT_DIR,
        check=True
    )

    print(f"[SUCCESS] {script_name} completed", flush=True)


def run_sql(sql_name):
    sql_path = PROJECT_DIR / "sql" / sql_name

    print(f"\n[START] Running {sql_name}", flush=True)

    with open(sql_path, "r", encoding="utf-8") as sql_file:
        subprocess.run(
            [
                "docker", "exec", "-i",
                POSTGRES_CONTAINER,
                "psql",
                "-v", "ON_ERROR_STOP=1",
                "-U", POSTGRES_USER,
                "-d", POSTGRES_DB
            ],
            stdin=sql_file,
            cwd=PROJECT_DIR,
            check=True
        )
    print(f"[SUCCESS] {sql_name} completed", flush=True)


def main():
    # 1. Extract data from API
    run_python("extract_flights.py")

    # 2. Load data into Raw layer
    run_python("load_flights.py")

    # 3. Load data into Staging
    run_sql("02_load_staging.sql")

    # 4. Run Staging data quality checks
    run_sql("03_data_quality.sql")

    # 5. Load data into DWH
    run_sql("05_load_dwh.sql")

    # 6. Run DWH data quality checks
    run_sql("06_dwh_quality.sql")

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()
