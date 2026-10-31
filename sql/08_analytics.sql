
-- Count flights by airline
SELECT
    a.airline_name,
    COUNT(*) AS flights_count
FROM dwh.dim_airline AS a
JOIN dwh.fact_flights AS f
    ON f.airline_id = a.airline_id
GROUP BY a.airline_id, a.airline_name
ORDER BY flights_count DESC;


-- Count departures by airport
SELECT
    a.airport_name,
    a.airport_iata,
    COUNT(*) AS flights_count
FROM dwh.dim_airport AS a
JOIN dwh.fact_flights AS f
    ON a.airport_id = f.departure_airport_id
GROUP BY a.airport_id, a.airport_name, a.airport_iata
ORDER BY flights_count DESC;


-- Count flights by date
SELECT
    d.date_id,
    d.year,
    d.month,
    d.day,
    COUNT(*) AS flights_count
FROM dwh.fact_flights AS f
JOIN dwh.dim_date AS d
    ON f.flight_date = d.date_id
GROUP BY d.date_id, d.year, d.month, d.day
ORDER BY d.date_id;


-- Count arrivals by airport
SELECT
    a.airport_name,
    a.airport_iata,
    COUNT(*) AS arrivals_count
FROM dwh.dim_airport AS a
JOIN dwh.fact_flights AS f
    ON a.airport_id = f.arrival_airport_id
GROUP BY a.airport_id, a.airport_name, a.airport_iata
ORDER BY arrivals_count DESC;


-- Count flights by route
SELECT
    dep.airport_name AS departure_airport,
    arr.airport_name AS arrival_airport,
    COUNT(*) AS flights_count
FROM dwh.fact_flights AS f
JOIN dwh.dim_airport AS dep
    ON f.departure_airport_id = dep.airport_id
JOIN dwh.dim_airport AS arr
    ON f.arrival_airport_id = arr.airport_id
GROUP BY
    dep.airport_id,
    dep.airport_name,
    arr.airport_id,
    arr.airport_name
ORDER BY flights_count DESC;


-- Count flights by status
SELECT
    flight_status,
    COUNT(*) AS flights_count
FROM dwh.fact_flights
GROUP BY flight_status
ORDER BY flights_count DESC;


-- Earliest and latest scheduled departure
SELECT
    MIN(scheduled_departure) AS earliest_departure,
    MAX(scheduled_departure) AS latest_departure
FROM dwh.fact_flights;


-- Average flight duration in minutes
SELECT
    ROUND(
        AVG(EXTRACT(EPOCH FROM (scheduled_arrival - scheduled_departure)) / 60),
        2
    ) AS avg_duration_minutes
FROM dwh.fact_flights
WHERE scheduled_departure IS NOT NULL
  AND scheduled_arrival IS NOT NULL;



  -- Flights scheduled for more than 2 hours
SELECT
    source_id,
    scheduled_departure,
    scheduled_arrival,
    ROUND(
        EXTRACT(EPOCH FROM (scheduled_arrival - scheduled_departure)) / 60,
        2
    ) AS duration_minutes
FROM dwh.fact_flights
WHERE scheduled_departure IS NOT NULL
  AND scheduled_arrival IS NOT NULL
  AND scheduled_arrival - scheduled_departure > INTERVAL '2 hours'
ORDER BY duration_minutes DESC;


