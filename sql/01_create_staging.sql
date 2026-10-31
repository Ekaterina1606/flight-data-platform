CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.flights (
    source_id TEXT PRIMARY KEY,
    flight_date DATE,
    flight_iata TEXT,
    flight_status TEXT,
    airline_name TEXT,
    departure_iata TEXT,
    departure_airport TEXT,
    arrival_iata TEXT,
    arrival_airport TEXT,
    scheduled_departure TIMESTAMPTZ,
    scheduled_arrival TIMESTAMPTZ
);