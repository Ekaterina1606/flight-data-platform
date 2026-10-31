import os
import json

import psycopg
from dotenv import load_dotenv


INPUT_PATH = "data/raw/flights/flights.json"


def build_source_id(flight):
    """Build a unique source ID for a flight record."""

    try:
        return (
            f"{flight['flight_date']}_"
            f"{flight['flight']['iata']}_"
            f"{flight['departure']['iata']}_"
            f"{flight['departure']['scheduled']}"
        )
    except (KeyError, TypeError):
        raise ValueError(
            "Flight record is missing required fields for source_id"
        )


def load_flights_to_db(flights, connection):
    """Insert flight records into the raw schema."""

    with connection.cursor() as cursor:
        for flight in flights:
            source_id = build_source_id(flight)

            cursor.execute(
                """
                INSERT INTO raw.flights (source_id, raw_data)
                VALUES (%s, %s)
                ON CONFLICT (source_id) DO NOTHING
                """,
                (source_id, json.dumps(flight))
            )

    connection.commit()


def main():
    load_dotenv()

    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    flights = data["data"]

    print("Flights loaded from JSON:", len(flights))

    connection = psycopg.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

    try:
        print("Connected to PostgreSQL")

        load_flights_to_db(flights, connection)

        print(f"Processed {len(flights)} flights")
    finally:
        connection.close()


if __name__ == "__main__":
    main()