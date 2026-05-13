"""
JWT and password helpers for LuntiAI account auth.
"""

import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import HTTPException, Request, status

try:
    from jose import JWTError, jwt
except ImportError:  # pragma: no cover - exercised only without optional dependency
    JWTError = Exception
    jwt = None

try:
    from passlib.context import CryptContext
except ImportError:  # pragma: no cover - exercised only without optional dependency
    CryptContext = None

try:
    import bcrypt
except ImportError:  # pragma: no cover - exercised only without optional dependency
    bcrypt = None


ALGORITHM = "HS256"
DEFAULT_TOKEN_HOURS = 24
_pwd_context = (
    CryptContext(schemes=["bcrypt"], deprecated="auto") if CryptContext is not None else None
)


def _secret_key() -> str:
    return os.environ.get("JWT_SECRET_KEY", "luntiai-dev-secret-change-me")


def hash_password(plain: str) -> str:
    if _pwd_context is not None:
        return _pwd_context.hash(plain)
    if bcrypt is not None:
        return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt.encode("utf-8"), 260000)
    return f"pbkdf2_sha256$260000${salt}${digest.hex()}"


def verify_password(plain: str, hashed: str) -> bool:
    if _pwd_context is not None:
        return _pwd_context.verify(plain, hashed)
    if bcrypt is not None and hashed.startswith(("$2a$", "$2b$", "$2y$")):
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

    try:
        scheme, iterations, salt, expected = hashed.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            plain.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations),
        )
        return hmac.compare_digest(digest.hex(), expected)
    except ValueError:
        return False


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(raw: str) -> bytes:
    padding = "=" * (-len(raw) % 4)
    return base64.urlsafe_b64decode(raw + padding)


def _fallback_jwt_encode(payload: dict[str, Any]) -> str:
    header = {"alg": ALGORITHM, "typ": "JWT"}
    header_part = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_part = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_part}.{payload_part}".encode("ascii")
    signature = hmac.new(_secret_key().encode("utf-8"), signing_input, hashlib.sha256).digest()
    return f"{header_part}.{payload_part}.{_b64url_encode(signature)}"


def _fallback_jwt_decode(token: str) -> dict[str, Any]:
    try:
        header_part, payload_part, signature_part = token.split(".")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    signing_input = f"{header_part}.{payload_part}".encode("ascii")
    expected_signature = hmac.new(
        _secret_key().encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    actual_signature = _b64url_decode(signature_part)
    if not hmac.compare_digest(actual_signature, expected_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    payload = json.loads(_b64url_decode(payload_part))
    if int(payload.get("exp", 0)) < int(datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    return payload


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=DEFAULT_TOKEN_HOURS))
    payload: dict[str, Any] = {"sub": str(user_id), "exp": expire}
    if jwt is not None:
        return jwt.encode(payload, _secret_key(), algorithm=ALGORITHM)

    payload["exp"] = int(expire.timestamp())
    return _fallback_jwt_encode(payload)


def verify_token(token: str) -> int:
    try:
        if jwt is not None:
            payload = jwt.decode(token, _secret_key(), algorithms=[ALGORITHM])
        else:
            payload = _fallback_jwt_decode(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return int(user_id)
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_current_user(request: Request) -> dict[str, Any]:
    from database import get_user

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = auth_header.removeprefix("Bearer ").strip()
    user_id = verify_token(token)
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
