
import os
import json
import requests
from dotenv import load_dotenv


URL = "https://api.aviationstack.com/v1/flights"

LIMIT = 100
TARGET_FLIGHTS = 1000
OUTPUT_PATH = "data/raw/flights/flights.json"


def fetch_flights(api_key, limit=LIMIT, target_flights=TARGET_FLIGHTS):
    """Fetch flight records from Aviationstack API using pagination."""
    all_flights = []

    for offset in range(0, target_flights, limit):
        params = {
            "access_key": api_key,
            "limit": limit,
            "offset": offset,
        }

        response = requests.get(URL, params=params, timeout=30)
        response.raise_for_status()

        page = response.json()

        if not isinstance(page, dict):
            raise ValueError("Invalid API response format")

        if page.get("error"):
            raise ValueError(f"Aviationstack API error: {page['error']}")

        flights = page.get("data")

        if not isinstance(flights, list):
            raise ValueError(
                "API response does not contain a valid flights list"
            )

        all_flights.extend(flights)

        print(
            f"Loaded page offset={offset}: {len(flights)} flights",
            flush=True
        )

        if len(flights) < limit:
            break

    return all_flights


def save_flights(flights, output_path=OUTPUT_PATH):
    """Save flight records to a JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            {"data": flights},
            file,
            ensure_ascii=False,
            indent=2
        )


def main():
    load_dotenv()

    api_key = os.getenv("AVIATIONSTACK_API_KEY")

    if not api_key:
        raise ValueError("AVIATIONSTACK_API_KEY is not set")

    flights = fetch_flights(api_key)
    save_flights(flights)

    print(f"Extracted {len(flights)} flights in total")


if __name__ == "__main__":
    main()
