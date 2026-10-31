

-- 1. Check missing dimension references

DO $$
DECLARE
    invalid_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO invalid_count
    FROM dwh.fact_flights f
    LEFT JOIN dwh.dim_airline a
        ON f.airline_id = a.airline_id
    LEFT JOIN dwh.dim_airport da
        ON f.departure_airport_id = da.airport_id
    LEFT JOIN dwh.dim_airport aa
        ON f.arrival_airport_id = aa.airport_id
    LEFT JOIN dwh.dim_date d
        ON f.flight_date = d.date_id
    WHERE a.airline_id IS NULL
       OR da.airport_id IS NULL
       OR aa.airport_id IS NULL
       OR d.date_id IS NULL;

    IF invalid_count > 0 THEN
        RAISE EXCEPTION
            'ERROR: % flights have missing DWH references',
            invalid_count;
    END IF;

    RAISE NOTICE 'PASS: All DWH references are valid';
END $$;


-- 2. Check duplicate flight records

DO $$
DECLARE
    duplicate_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO duplicate_count
    FROM (
        SELECT source_id
        FROM dwh.fact_flights
        GROUP BY source_id
        HAVING COUNT(*) > 1
    ) duplicates;

    IF duplicate_count > 0 THEN
        RAISE EXCEPTION
            'ERROR: % duplicate flights found in DWH',
            duplicate_count;
    END IF;

    RAISE NOTICE 'PASS: No duplicate flights in DWH';
END $$;


-- 3. Check empty fact table

DO $$
DECLARE
    total_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO total_count
    FROM dwh.fact_flights;

    IF total_count = 0 THEN
        RAISE EXCEPTION
            'ERROR: DWH fact table is empty';
    END IF;

    RAISE NOTICE 'PASS: DWH fact table contains % flights',
        total_count;
END $$;
