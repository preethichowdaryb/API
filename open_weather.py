#  - Loads API key from .env (secure)
#  - Fetches CURRENT weather for 3 cities
#  - Gets both metric (°C) and imperial (°F) temps
#  - Saves all results to JSON (deliverable)
#  - Tries an INVALID key and prints status + message
#  - Prints a simple metric vs imperial comparison

import os, json, requests
from datetime import datetime, timezone
from dotenv import load_dotenv

# 1) Load your key from .env 
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "OPENWEATHER_API_KEY not found. Create a .env file with "
        "OPENWEATHER_API_KEY=YOUR_REAL_KEY_HERE"
    )

# 2) Pick at least 3 cities (lat/lon avoids name ambiguity)
CITIES = [
    {"name": "Chicago,US", "lat": 41.8781, "lon": -87.6298},
    {"name": "London,GB",  "lat": 51.5074, "lon": -0.1278},
    {"name": "Sydney,AU",  "lat": -33.8688, "lon": 151.2093},
]

BASE = "https://api.openweathermap.org/data/2.5/weather"

def fetch_current(lat, lon, units, api_key):
    """
    Call the Current Weather API for (lat, lon) in chosen units.
    Returns a small dict with status, temp, and any message.
    """
    params = {"lat": lat, "lon": lon, "units": units, "appid": api_key}
    r = requests.get(BASE, params=params, timeout=30)
    out = {"status": r.status_code, "units": units}
    try:
        j = r.json()
        out["json"] = j
        out["temp"] = (j.get("main") or {}).get("temp")
        out["message"] = j.get("message")
    except ValueError:
        out["text"] = r.text  # non-JSON response
    return out

# 3) Fetch metric + imperial for each city
results = {"retrieved_at_utc": datetime.now(timezone.utc).isoformat(), "cities": []}
for c in CITIES:
    m = fetch_current(c["lat"], c["lon"], "metric",   API_KEY)  # °C
    i = fetch_current(c["lat"], c["lon"], "imperial", API_KEY)  # °F
    results["cities"].append({
        "city": c["name"], "lat": c["lat"], "lon": c["lon"],
        "metric":   {"status": m["status"], "temp_C": m.get("temp"), "message": m.get("message")},
        "imperial": {"status": i["status"], "temp_F": i.get("temp"), "message": i.get("message")},
    })

# 4) Save all results to JSON (deliverable)
OUT = "openweathermap_current_weather.json"
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("Saved JSON →", OUT)

# 5) Invalid API key test (expect 401 + message)
bad = fetch_current(CITIES[0]["lat"], CITIES[0]["lon"], "metric", "INVALID_KEY")
print("\nInvalid key test:")
print("  Status:", bad["status"])
print("  Message/Text:", bad.get("message") or bad.get("text"))

# 6) Compare metric vs imperial
print("\nMetric vs Imperial (per city):")
for entry in results["cities"]:
    print(f"  {entry['city']}: {entry['metric']['temp_C']} °C  |  {entry['imperial']['temp_F']} °F")