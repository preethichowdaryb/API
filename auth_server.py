import time
from typing import Optional
from fastapi import FastAPI, Form, HTTPException
import jwt

from settings import SECRET, ISSUER, AUDIENCE, CLIENT_ID, CLIENT_SECRET, ALLOWED_SCOPES

app = FastAPI(title="Auth Server (demo)")

@app.post("/oauth/token")
def token(
    grant_type: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...),
    scope: Optional[str] = Form("")
):
    if grant_type != "client_credentials":
        raise HTTPException(status_code=400, detail={"error": "unsupported_grant_type"})

    if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
        raise HTTPException(status_code=401, detail={"error": "invalid_client"})

    requested_scopes = set(scope.split()) if scope else {"forecast.read"}
    if not requested_scopes.issubset(ALLOWED_SCOPES):
        raise HTTPException(status_code=400, detail={"error": "invalid_scope"})

    now = int(time.time())
    payload = {
        "iss": ISSUER,
        "aud": AUDIENCE,
        "sub": client_id,
        "scope": " ".join(sorted(requested_scopes)),
        "iat": now,
        "exp": now + 3600
    }
    access_token = jwt.encode(payload, SECRET, algorithm="HS256")
    return {"access_token": access_token, "token_type": "Bearer", "expires_in": 3600, "scope": payload["scope"]}
