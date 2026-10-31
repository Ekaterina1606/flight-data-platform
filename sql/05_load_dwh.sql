
-- 1. Load airlines
INSERT INTO dwh.dim_airline (airline_name)
SELECT DISTINCT airline_name
FROM staging.flights
WHERE airline_name IS NOT NULL
ON CONFLICT (airline_name) DO NOTHING;


-- 2. Load airports
INSERT INTO dwh.dim_airport (airport_iata, airport_name)
SELECT departure_iata, departure_airport
FROM staging.flights
WHERE departure_iata IS NOT NULL

UNION

SELECT arrival_iata, arrival_airport
FROM staging.flights
WHERE arrival_iata IS NOT NULL

ON CONFLICT (airport_iata) DO NOTHING;


-- 3. Load dates
INSERT INTO dwh.dim_date (date_id, year, month, day)
SELECT DISTINCT
    flight_date,
    EXTRACT(YEAR FROM flight_date)::INTEGER,
    EXTRACT(MONTH FROM flight_date)::INTEGER,
    EXTRACT(DAY FROM flight_date)::INTEGER
FROM staging.flights
WHERE flight_date IS NOT NULL
ON CONFLICT (date_id) DO NOTHING;


-- 4. Load flights
INSERT INTO dwh.fact_flights (
    source_id,
    flight_date,
    airline_id,
    departure_airport_id,
    arrival_airport_id,
    flight_status,
    scheduled_departure,
    scheduled_arrival
)
SELECT
    s.source_id,
    s.flight_date,
    a.airline_id,
    dep.airport_id,
    arr.airport_id,
    s.flight_status,
    s.scheduled_departure,
    s.scheduled_arrival
FROM staging.flights AS s
LEFT JOIN dwh.dim_airline AS a
    ON s.airline_name = a.airline_name
LEFT JOIN dwh.dim_airport AS dep
    ON s.departure_iata = dep.airport_iata
LEFT JOIN dwh.dim_airport AS arr
    ON s.arrival_iata = arr.airport_iata
ON CONFLICT (source_id) DO NOTHING;
