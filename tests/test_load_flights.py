import pytest

from ingestion.load_flights import build_source_id


def test_build_source_id():
    """Check that a source ID is built correctly."""

    flight = {
        "flight_date": "2026-09-20",
        "flight": {
            "iata": "LH400"
        },
        "departure": {
            "iata": "FRA",
            "scheduled": "2026-09-20T10:30:00+00:00"
        }
    }

    result = build_source_id(flight)

    assert result == (
        "2026-09-20_LH400_FRA_2026-09-20T10:30:00+00:00"
    )


def test_build_source_id_missing_flight_number():
    """Check that missing flight data raises a ValueError."""

    flight = {
        "flight_date": "2026-09-20",
        "flight": {},
        "departure": {
            "iata": "FRA",
            "scheduled": "2026-09-20T10:30:00+00:00"
        }
    }

    with pytest.raises(ValueError, match="missing required fields"):
        build_source_id(flight)


def test_build_source_id_missing_departure():
    """Check that missing departure data raises a ValueError."""

    flight = {
        "flight_date": "2026-09-20",
        "flight": {
            "iata": "LH400"
        }
    }

    with pytest.raises(ValueError, match="missing required fields"):
        build_source_id(flight)

from unittest.mock import MagicMock

from ingestion.load_flights import load_flights_to_db


def test_load_flights_to_db():
    """Check that flight records are inserted and the transaction is committed."""

    flights = [
        {
            "flight_date": "2026-09-20",
            "flight": {"iata": "LH400"},
            "departure": {
                "iata": "FRA",
                "scheduled": "2026-09-20T10:30:00+00:00"
            }
        },
        {
            "flight_date": "2026-09-21",
            "flight": {"iata": "AF123"},
            "departure": {
                "iata": "CDG",
                "scheduled": "2026-09-21T12:00:00+00:00"
            }
        }
    ]

    connection = MagicMock()
    cursor = MagicMock()

    connection.cursor.return_value.__enter__.return_value = cursor

    load_flights_to_db(flights, connection)

    assert cursor.execute.call_count == 2
    assert connection.commit.call_count == 1

    first_call = cursor.execute.call_args_list[0]

    assert first_call.args[1][0] == (
        "2026-09-20_LH400_FRA_2026-09-20T10:30:00+00:00"
    )