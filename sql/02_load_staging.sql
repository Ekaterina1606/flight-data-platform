INSERT INTO staging.flights (
    source_id,
    flight_date,
    flight_iata,
    flight_status,
    airline_name,
    departure_iata,
    departure_airport,
    arrival_iata,
    arrival_airport,
    scheduled_departure,
    scheduled_arrival
)
SELECT
    source_id,
    (raw_data->>'flight_date')::DATE,
    raw_data->'flight'->>'iata',
    raw_data->>'flight_status',
    raw_data->'airline'->>'name',
    raw_data->'departure'->>'iata',
    raw_data->'departure'->>'airport',
    raw_data->'arrival'->>'iata',
    raw_data->'arrival'->>'airport',
    (raw_data->'departure'->>'scheduled')::TIMESTAMPTZ,
    (raw_data->'arrival'->>'scheduled')::TIMESTAMPTZ
FROM raw.flights
ON CONFLICT (source_id) DO NOTHING;