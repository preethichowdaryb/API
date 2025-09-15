Problem Statement: A real-time pipeline that collects external weather data from public APIs, processes and filters it, and stores the refined data for analytics and alerting. I designed and implemented this to demonstrate proper error handling, secure API key usage, and standardized data storage for multiple weather sources.

Target State: The goal is to design and implement a fully automated data pipeline that ingests weather data from Open-Meteo, OpenWeatherMap, and the National Weather Service, transforms it, and stores it in a structured format for analysis, testing both normal and erroneous scenarios.

Project overview : This project builds a real-time weather data pipeline that integrates data from Open-Meteo, OpenWeatherMap, and the U.S. National Weather Service (NWS), then standardizes and stores the results for analytics and reporting. From Open-Meteo, it retrieves hourly temperature and humidity readings and computes 3-day max/min summaries. From OpenWeatherMap, it captures current weather snapshots for multiple cities, with secure API key handling via .env and negative test cases for invalid keys and unit conversions. From the NWS, it pulls forecast data using a required custom User-Agent, also demonstrating expected failures when headers are missing.
The pipeline outputs data in structured formats—CSV for Open-Meteo and JSON for OpenWeatherMap and NWS—while logging validations, error handling, and data quality checks directly in the terminal. Overall, this repository highlights best practices in API integration, secure secret management, and resilient ETL design, producing clear, reproducible artifacts ready for downstream analysis or alerting.

Files in the repo : 
.env – stores API keys securely
README.md – project documentation
app.py – main application script
auth_server.py – authentication server code
nws.py – National Weather Service integration
open_meteo.py – Open-Meteo API integration
open_meteo_hourly.csv – sample CSV output
open_weather.py – OpenWeatherMap API integration
openweathermap_current_weather.json – sample JSON output
part c test run.txt – test run logs
resource_api.py – shared API resource utilities
settings.py – configuration settings
pycache/ – Python cache folder
