import os
import json

import psycopg
from dotenv import load_dotenv


load_dotenv()

with open("data/raw/flights/flights.json", "r", encoding="utf-8") as file:
    data = json.load(file)

flights = data["data"]

print("Flights loaded from JSON:", len(flights))

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")


connection = psycopg.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

print("Connected to PostgreSQL")

with connection.cursor() as cursor:
    for flight in flights:
        source_id = (
            f"{flight['flight_date']}_"
            f"{flight['flight']['iata']}_"
            f"{flight['departure']['iata']}_"
            f"{flight['departure']['scheduled']}"
            )
        cursor.execute(
            """
            INSERT INTO raw.flights (source_id, raw_data)
            VALUES (%s, %s)
            ON CONFLICT (source_id) DO NOTHING
            """,
            (source_id, json.dumps(flight))
        )

connection.commit()

print(f"Processed {len(flights)} flights")

connection.close()