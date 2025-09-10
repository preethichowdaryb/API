# 1) Find your grid point from lat/lon (api.weather.gov/points)
# 2) Add a required custom User-Agent header and get the forecast
# 3) Try the same request WITHOUT User-Agent and show what happens
# 4) Compare NWS hourly forecast with Open-Meteo for the same location

import requests
from pprint import pprint

# ---- Choose a location (Chicago, USA example) ----
LAT, LON = 41.8781, -87.6298

# ---- REQUIRED by NWS: a custom User-Agent with contact info ----
#    Replace with YOUR app + email or website
UA = "(beginner-weather-lab, you@example.com)"
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/geo+json",  # NWS returns GeoJSON/JSON-LD; this is fine
}

# ----------------------------
# 1) Get your grid + forecast URLs
# ----------------------------
points_url = f"https://api.weather.gov/points/{LAT},{LON}"
print("Points URL:", points_url)

resp_points = requests.get(points_url, headers=HEADERS, timeout=30)
print("Points status:", resp_points.status_code)
resp_points.raise_for_status()
points = resp_points.json()

# Extract useful bits
props = points["properties"]
grid_id = props["gridId"]
grid_x  = props["gridX"]
grid_y  = props["gridY"]
forecast_url        = props["forecast"]         # 12-hr periods
forecast_hourly_url = props["forecastHourly"]   # hourly periods

print(f"Grid: {grid_id} {grid_x},{grid_y}")
print("Forecast URL:", forecast_url)
print("Hourly URL:  ", forecast_hourly_url)

# ----------------------------
# 2) Call hourly forecast (with required User-Agent)
# ----------------------------
r_ok = requests.get(forecast_hourly_url, headers=HEADERS, timeout=30)
print("\nHourly forecast WITH User-Agent:", r_ok.status_code)
r_ok.raise_for_status()
hourly = r_ok.json()["properties"]["periods"]

print("First 3 NWS hourly periods (time, temp, unit, shortForecast):")
for p in hourly[:3]:
    print(p["startTime"], p["temperature"], p["temperatureUnit"], "-", p["shortForecast"])

# ----------------------------
# 3) Try the same request WITHOUT User-Agent
# ----------------------------
# NOTE: NWS requires a User-Agent. Without it, you may get blocked/denied.
r_bad = requests.get(forecast_hourly_url, timeout=30)  # no headers
print("\nHourly forecast WITHOUT User-Agent:", r_bad.status_code)
print("Response snippet:", r_bad.text[:300], "...")

# ----------------------------
# 4) Compare with Open-Meteo (no auth)
#    - Open-Meteo gives temperature in °C by default
#    - NWS hourly periods usually show temperature in F (temperatureUnit='F')
# ----------------------------
om_url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&hourly=temperature_2m"
    "&forecast_days=1"
    "&timezone=America/Chicago"
)
om = requests.get(om_url, timeout=30)
print("\nOpen-Meteo status:", om.status_code)
om.raise_for_status()
omj = om.json()

print("First 3 Open-Meteo hours (time, temp_C):")
for t, temp_c in list(zip(omj["hourly"]["time"], omj["hourly"]["temperature_2m"]))[:3]:
    print(t, temp_c)

# (Optional) quick, rough comparison of first hour from each:
def f_to_c(f): return (f - 32) * 5/9

if hourly and omj["hourly"]["temperature_2m"]:
    nws_temp_f = hourly[0]["temperature"]
    nws_temp_c_est = round(f_to_c(nws_temp_f), 1)
    om_temp_c = omj["hourly"]["temperature_2m"][0]
    print("\nQuick compare (first available hour):")
    print(f"NWS: ~{nws_temp_f} °F (~{nws_temp_c_est} °C)   vs   Open-Meteo: {om_temp_c} °C")