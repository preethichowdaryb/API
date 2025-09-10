Part A – Using a No-Auth Weather API (Open-Meteo)
Connect to the Open-Meteo API using a city of your choice (use latitude and longitude).
Retrieve hourly weather data including temperature and humidity.
Save the response data into a CSV file.
Find the maximum and minimum temperature for the next 3 days and record the time they occur.
Handle an error case: What happens if you misspell a parameter? Write down the response code and message.

Part B – Using an API Key (OpenWeatherMap)
Sign up for OpenWeatherMap and obtain a free API key.
Store the API key in a secure way (e.g., environment variable or .env file).
Fetch the current weather for at least 3 different cities and compare their temperatures.
Save the data in JSON format.
Try making a request with an invalid API key and note the response (status code + error message).
Compare the results of metric vs. imperial units and write the differences in your notes.
Document what rate limits are applied (how many calls per minute/hour).

Part C – Understanding OAuth (Conceptual + Simulation)
Explain in your own words the difference between No-Auth, API Key, and OAuth 2.0.
Create a flow diagram of how OAuth works (User → App → Authorization Server → Resource API).
Simulate an OAuth-protected API:
Try making a request without a token and describe the error you receive.
Add a valid token and describe how the response changes.
Extend the simulation: Imagine you are designing a weather API that requires OAuth. Write down what data you would protect and why.

Part D -  US National Weather Service (NWS)
Connect to the NWS API using your location’s grid point.
Add a custom User-Agent header to your request (as required by NWS).
Try making a request without the User-Agent and note what happens.
Compare the forecast data with Open-Meteo or OpenWeatherMap results.
