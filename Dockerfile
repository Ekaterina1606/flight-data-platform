FROM apache/airflow:2.10.5

USER airflow

RUN pip install --no-cache-dir \
    psycopg2-binary \
    psycopg[binary] \
    requests \
    python-dotenv