
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

if not API_KEY:
    raise ValueError("AVIATIONSTACK_API_KEY is not set")

URL = "https://api.aviationstack.com/v1/flights"

LIMIT = 100
TARGET_FLIGHTS = 1000

all_flights = []

for offset in range(0, TARGET_FLIGHTS, LIMIT):
    params = {
        "access_key": API_KEY,
        "limit": LIMIT,
        "offset": offset,
    }

    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()

    page = response.json()

    if page.get("error"):
        raise ValueError(f"Aviationstack API error: {page['error']}")

    flights = page.get("data")

    if not isinstance(flights, list):
        raise ValueError("API response does not contain a valid flights list")

    all_flights.extend(flights)

    print(
        f"Loaded page offset={offset}: {len(flights)} flights",
        flush=True
    )

    if len(flights) < LIMIT:
        break

os.makedirs("data/raw/flights", exist_ok=True)

with open(
    "data/raw/flights/flights.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        {"data": all_flights},
        file,
        ensure_ascii=False,
        indent=2
    )

print(f"Extracted {len(all_flights)} flights in total")
