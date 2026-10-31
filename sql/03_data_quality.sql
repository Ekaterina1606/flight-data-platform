
-- 1. Check missing required values

DO $$
DECLARE
    missing_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO missing_count
    FROM staging.flights
    WHERE flight_date IS NULL
       OR departure_iata IS NULL
       OR arrival_iata IS NULL;

    IF missing_count > 0 THEN
        RAISE EXCEPTION
            'ERROR: % flights have missing required values',
            missing_count;
    END IF;

    RAISE NOTICE 'PASS: No missing required values';
END $$;


-- 2. Check duplicate source IDs

DO $$
DECLARE
    duplicate_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO duplicate_count
    FROM (
        SELECT source_id
        FROM staging.flights
        GROUP BY source_id
        HAVING COUNT(*) > 1
    ) duplicates;

    IF duplicate_count > 0 THEN
        RAISE EXCEPTION
            'ERROR: % duplicate source IDs found',
            duplicate_count;
    END IF;

    RAISE NOTICE 'PASS: No duplicate source IDs';
END $$;


-- 3. Check missing flight numbers (WARNING)

DO $$
DECLARE
    missing_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO missing_count
    FROM staging.flights
    WHERE flight_iata IS NULL;

    IF missing_count > 0 THEN
        RAISE WARNING
            'WARNING: % flights have missing flight numbers',
            missing_count;
    ELSE
        RAISE NOTICE 'PASS: All flight numbers are available';
    END IF;
END $$;


-- 4. Check negative flight duration (WARNING)

DO $$
DECLARE
    invalid_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO invalid_count
    FROM staging.flights
    WHERE scheduled_departure IS NOT NULL
      AND scheduled_arrival IS NOT NULL
      AND scheduled_arrival < scheduled_departure;

    IF invalid_count > 0 THEN
        RAISE WARNING
            'WARNING: % flights have arrival before departure',
            invalid_count;
    ELSE
        RAISE NOTICE 'PASS: No negative flight durations';
    END IF;
END $$;
