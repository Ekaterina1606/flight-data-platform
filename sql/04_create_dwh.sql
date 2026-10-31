
CREATE SCHEMA IF NOT EXISTS dwh;

CREATE TABLE IF NOT EXISTS dwh.dim_airline (
    airline_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    airline_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dwh.dim_airport (
    airport_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    airport_iata TEXT NOT NULL UNIQUE,
    airport_name TEXT
);

CREATE TABLE IF NOT EXISTS dwh.dim_date (
    date_id DATE PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS dwh.fact_flights (
    source_id TEXT PRIMARY KEY,
    flight_date DATE NOT NULL,
    airline_id BIGINT REFERENCES dwh.dim_airline(airline_id),
    departure_airport_id BIGINT REFERENCES dwh.dim_airport(airport_id),
    arrival_airport_id BIGINT REFERENCES dwh.dim_airport(airport_id),
    flight_status TEXT,
    scheduled_departure TIMESTAMPTZ,
    scheduled_arrival TIMESTAMPTZ
);
