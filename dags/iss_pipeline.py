from __future__ import annotations

import logging
from datetime import datetime, timedelta

import requests
from airflow.decorators import task
from airflow.models.dag import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook

ISS_URL = "http://api.open-notify.org/iss-now.json"
POSTGRES_CONN_ID = "iss_postgres"

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="iss_position_pipeline",
    default_args=default_args,
    description="HW: fetch ISS position every 30 min -> parse -> insert into analytics.iss_location",
    schedule="*/30 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["homework", "api", "postgres"],
) as dag:

    @task
    def fetch_iss() -> dict:
        response = requests.get(ISS_URL, timeout=30)
        response.raise_for_status()
        raw = response.json()
        logging.info("Raw API response: %s", raw)
        return raw

    @task
    def parse_iss(raw: dict) -> dict:
        parsed = {
            "timestamp": int(raw["timestamp"]),
            "latitude": float(raw["iss_position"]["latitude"]),
            "longitude": float(raw["iss_position"]["longitude"]),
        }
        logging.info("Parsed row: %s", parsed)
        return parsed

    @task
    def load_iss(row: dict) -> str:
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        sql = """
            INSERT INTO iss_location (event_timestamp, latitude, longitude)
            VALUES (to_timestamp(%s), %s, %s)
            ON CONFLICT (event_timestamp) DO NOTHING
        """
        hook.run(sql, parameters=(row["timestamp"], row["latitude"], row["longitude"]))
        logging.info("Inserted: %s", row)
        return f"loaded {row}"

    @task
    def verify_rows() -> int:
        hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        count = hook.get_first("SELECT COUNT(*) FROM iss_location")[0]
        logging.info("Total rows in iss_location: %s", count)
        return count

    loaded = load_iss(parse_iss(fetch_iss()))
    loaded >> verify_rows()
