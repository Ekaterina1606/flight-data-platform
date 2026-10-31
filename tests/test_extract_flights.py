import json

from ingestion.extract_flights import fetch_flights, save_flights


def test_fetch_flights_pagination(monkeypatch):
    """Check that fetch_flights collects records from multiple pages."""

    responses = [
        {"data": [{"id": 1}, {"id": 2}]},
        {"data": [{"id": 3}]},
    ]

    requested_offsets = []

    class FakeResponse:
        def __init__(self, data):
            self.data = data

        def raise_for_status(self):
            pass

        def json(self):
            return self.data

    def fake_get(url, params, timeout):
        requested_offsets.append(params["offset"])
        return FakeResponse(responses[len(requested_offsets) - 1])

    monkeypatch.setattr(
        "ingestion.extract_flights.requests.get",
        fake_get
    )

    flights = fetch_flights(
        api_key="test-key",
        limit=2,
        target_flights=4
    )

    assert len(flights) == 3
    assert requested_offsets == [0, 2]


def test_fetch_flights_api_error(monkeypatch):
    """Check that API errors are handled."""

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"error": {"message": "Invalid API key"}}

    def fake_get(url, params, timeout):
        return FakeResponse()

    monkeypatch.setattr(
        "ingestion.extract_flights.requests.get",
        fake_get
    )

    try:
        fetch_flights(api_key="test-key", limit=2, target_flights=2)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert "Aviationstack API error" in str(error)


def test_save_flights(tmp_path):
    """Check that flight records are saved as JSON."""

    flights = [{"id": 1}, {"id": 2}]
    output_path = tmp_path / "flights.json"

    save_flights(flights, str(output_path))

    with open(output_path, encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == {"data": flights}