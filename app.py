from flask import Flask, request, jsonify, make_response
from functools import wraps

app = Flask(__name__)

# --- Fake token store (simulating an OAuth AS/IdP) ---
TOKENS = {
    # read-only user
    "secret-token-123": {
        "sub": "user_123",
        "scopes": {"weather.read"}
    },
    # admin user with write privileges
    "admin-token-456": {
        "sub": "admin_001",
        "scopes": {"weather.read", "weather.write"}
    }
}


def error_response(status, err, desc, scope=None):
    """RFC 6750-style error payload + WWW-Authenticate header."""
    payload = {"error": err, "error_description": desc}
    resp = make_response(jsonify(payload), status)
    www = f'Bearer realm="api", error="{err}", error_description="{desc}"'
    if scope:
        www += f', scope="{scope}"'
    resp.headers["WWW-Authenticate"] = www
    return resp


def require_oauth(required_scopes=None):
    required_scopes = set(required_scopes or [])

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return error_response(
                    401, "invalid_request", "Missing or malformed Authorization header"
                )
            token = auth.removeprefix("Bearer ").strip()
            meta = TOKENS.get(token)
            if not meta:
                return error_response(
                    401, "invalid_token", "Access token is invalid"
                )
            token_scopes = meta.get("scopes", set())
            if not required_scopes.issubset(token_scopes):
                # 403 with insufficient_scope is allowed by RFC 6750
                missing = " ".join(sorted(required_scopes - token_scopes)) or None
                return error_response(
                    403, "insufficient_scope", "Token lacks required scope(s)", scope=missing
                )
            # Attach identity to request context (simple simulation)
            request.user = {"sub": meta["sub"], "scopes": list(token_scopes)}
            return fn(*args, **kwargs)

        return wrapper

    return decorator


# --- Public ping endpoint (no auth) ---
@app.get("/api/ping")
def ping():
    return {"ok": True, "message": "pong"}


# --- Protected demo endpoint (auth required, no specific scopes) ---
@app.get("/api/secret")
@require_oauth()
def secret():
    return {"message": f"Hello, {request.user['sub']}!"}


# ===== Weather API (with scopes) =====

# GET current weather requires weather.read
@app.get("/v1/weather/current")
@require_oauth({"weather.read"})
def current_weather():
    city = request.args.get("city", "Chicago")
    # Fake data for demonstration
    return {
        "city": city,
        "temp_c": 23.4,
        "condition": "Partly Cloudy",
        "retrieved_by": request.user["sub"]
    }


# POST observation requires weather.write
@app.post("/v1/weather/observations")
@require_oauth({"weather.write"})
def submit_observation():
    body = request.get_json(force=True, silent=True) or {}
    # pretend we validate + persist
    return {
        "status": "created",
        "by": request.user["sub"],
        "observation": body
    }, 201


# Who am I?
@app.get("/v1/me")
@require_oauth()
def me():
    return {"sub": request.user["sub"], "scopes": request.user["scopes"]}


if __name__ == "__main__":
    app.run(debug=True)
