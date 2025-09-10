# resource_api.py
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.responses import JSONResponse
import jwt
from jwt import ExpiredSignatureError, InvalidAudienceError, InvalidTokenError

from settings import SECRET, ISSUER, AUDIENCE

app = FastAPI(title="Weather API (demo)")

def _unauthorized(desc: str):
    # RFC 6750-compliant header
    headers = {
        'WWW-Authenticate': 'Bearer realm="weather", error="invalid_token", error_description="' + desc + '"'
    }
    return JSONResponse(status_code=401, content={"error": "invalid_token", "error_description": desc}, headers=headers)

def _forbidden(required_scope: str):
    headers = {
        'WWW-Authenticate': f'Bearer error="insufficient_scope", scope="{required_scope}"'
    }
    return JSONResponse(status_code=403, content={"error": "insufficient_scope", "required_scope": required_scope}, headers=headers)

def verify_bearer(authorization: Optional[str]) -> Dict[str, Any]:
    if not authorization or not authorization.lower().startswith("bearer "):
        # Missing header or wrong scheme
        raise HTTPException(status_code=401, detail={"error":"invalid_token","error_description":"Missing access token"}, headers={
            'WWW-Authenticate': 'Bearer realm="weather", error="invalid_token", error_description="Missing access token"'
        })
    token = authorization.split(" ", 1)[1].strip()
    try:
        claims = jwt.decode(token, SECRET, algorithms=["HS256"], audience=AUDIENCE)
        if claims.get("iss") != ISSUER:
            raise InvalidTokenError("Bad issuer")
        return claims
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail={"error":"invalid_token","error_description":"Token expired"}, headers={
            'WWW-Authenticate': 'Bearer realm="weather", error="invalid_token", error_description="Token expired"'
        })
    except InvalidAudienceError:
        raise HTTPException(status_code=401, detail={"error":"invalid_token","error_description":"Invalid audience"}, headers={
            'WWW-Authenticate': 'Bearer realm="weather", error="invalid_token", error_description="Invalid audience"'
        })
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail={"error":"invalid_token","error_description":"Invalid token"}, headers={
            'WWW-Authenticate': 'Bearer realm="weather", error="invalid_token", error_description="Invalid token"'
        })

def require_scope(claims: Dict[str, Any], required: str):
    scopes = set((claims.get("scope") or "").split())
    if required not in scopes:
        # 403 insufficient_scope
        raise HTTPException(status_code=403, detail={"error":"insufficient_scope","required_scope":required}, headers={
            'WWW-Authenticate': f'Bearer error="insufficient_scope", scope="{required}"'
        })

@app.get("/status")
def status():
    return {"ok": True}

@app.get("/weather/today")
def weather_today(
    authorization: Optional[str] = Header(default=None),
    lat: float = Query(...),
    lon: float = Query(...)
):
    claims = verify_bearer(authorization)
    require_scope(claims, "forecast.read")
    # Demo payload
    return {
        "location": {"lat": lat, "lon": lon, "city": "Houston"},
        "current": {"temp_c": 31.2, "humidity": 0.56},
        "forecast": [{"ts":"2025-09-09T12:00:00Z","temp_c":33.0,"precip_prob":0.1}],
        "token_sub": claims.get("sub"),
        "scope": claims.get("scope")
    }
