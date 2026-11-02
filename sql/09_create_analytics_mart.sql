
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE OR REPLACE VIEW analytics.mart_flight_operations AS
SELECT
    f.source_id,
    f.flight_date,

    d.year AS flight_year,
    d.month AS flight_month,
    d.day AS flight_day,

    a.airline_name,

    dep.airport_iata AS departure_airport_iata,
    dep.airport_name AS departure_airport_name,

    arr.airport_iata AS arrival_airport_iata,
    arr.airport_name AS arrival_airport_name,

    f.flight_status,
    f.scheduled_departure,
    f.scheduled_arrival

FROM dwh.fact_flights AS f

LEFT JOIN dwh.dim_date AS d
    ON f.flight_date = d.date_id

LEFT JOIN dwh.dim_airline AS a
    ON f.airline_id = a.airline_id

LEFT JOIN dwh.dim_airport AS dep
    ON f.departure_airport_id = dep.airport_id

LEFT JOIN dwh.dim_airport AS arr
    ON f.arrival_airport_id = arr.airport_id;
