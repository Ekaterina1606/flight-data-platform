import os

import json

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

if not API_KEY:
    raise ValueError("AVIATIONSTACK_API_KEY is not set")

print("API key loaded:", bool(API_KEY))


URL = "https://api.aviationstack.com/v1/flights"

params = {
    "access_key": API_KEY,
    "limit": 5
}

response = requests.get(URL, params=params, timeout=30)

print("Status code:", response.status_code)

data = response.json()

os.makedirs("data/raw/flights", exist_ok=True)

with open("data/raw/flights/flights.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(data)