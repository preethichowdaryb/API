# Part A: Open-Meteo (No-Auth)
# City used: Chicago, USA (lat/lon below)
import requests
import pandas as pd
LAT, LON = 41.8781, -87.6298           # Chicago, USA
TZ = "America/Chicago"                  # local timezone for readable timestamps
CSV_PATH = "open_meteo_hourly.csv"      # output CSV file
def build_url(hourly_vars: str) -> str:
    """Build the Open-Meteo forecast URL for the next 3 days (72 hours)."""
    return (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        f"&hourly={hourly_vars}"
        "&forecast_days=3"
        f"&timezone={TZ}"
    )
# Q1) Connect to the Open-Meteo API using latitude/longitude
print("\nQ1) Connect to Open-Meteo with lat/lon")
url = build_url("temperature_2m,relative_humidity_2m")
print("Request URL:", url)
resp = requests.get(url, timeout=30)  # timeout avoids hanging forever
print("HTTP status:", resp.status_code)
resp.raise_for_status()               # stop here if not 2xx (OK)
# Q2) Retrieve hourly weather: temperature + humidity
print("\nQ2) Retrieve hourly temperature & humidity")
data = resp.json()            # parse JSON into Python dict
hourly = data["hourly"]       # hourly arrays (parallel lists)
print("Hourly keys:", list(hourly.keys()))
print("First 3 times:", hourly["time"][:3])
print("First 3 temps (°C):", hourly["temperature_2m"][:3])
print("First 3 RH (%):", hourly["relative_humidity_2m"][:3])
# Q3) Save the response data into a CSV file
print("\nQ3) Save to CSV:", CSV_PATH)
df = pd.DataFrame({
    "time": hourly["time"],
    "temperature_2m": hourly["temperature_2m"],               # °C
    "relative_humidity_2m": hourly["relative_humidity_2m"],   # %
})
df.to_csv(CSV_PATH, index=False)
print("Saved:", CSV_PATH)
# Q4) Find max & min temperature for the next 3 days + times
print("\nQ4) Min/Max temperature + times")
min_idx = df["temperature_2m"].idxmin()
max_idx = df["temperature_2m"].idxmax()
min_temp = df.loc[min_idx, "temperature_2m"]
min_time = df.loc[min_idx, "time"]
max_temp = df.loc[max_idx, "temperature_2m"]
max_time = df.loc[max_idx, "time"]
print(f"Min temperature: {min_temp} °C at {min_time}")
print(f"Max temperature: {max_temp} °C at {max_time}")
# Q5) Error case: misspell a parameter → show code + message
print("\nQ5) Error case: misspelled parameter (expect HTTP 400)")
bad_url = build_url("tempeture_2m,relative_humidity_2m")  # <-- typo on purpose
bad_resp = requests.get(bad_url, timeout=30)
print("HTTP status:", bad_resp.status_code)
# Try to print JSON error if available; otherwise print text
try:
    print("Error JSON:", bad_resp.json())
except ValueError:
    print("Error text:", bad_resp.text[:400], "...")



