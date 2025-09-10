# settings.py
SECRET = "super-secret-signing-key"        # HS256 signing key (demo only)
ISSUER = "auth.example"
AUDIENCE = "weather-api"

CLIENT_ID = "acme-app"
CLIENT_SECRET = "acme-secret"

# Which scopes this client is allowed to request
ALLOWED_SCOPES = {"forecast.read", "history.read"}
