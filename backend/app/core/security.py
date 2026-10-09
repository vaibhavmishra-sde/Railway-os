"""Password hashing and access-token helpers."""

from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

# PBKDF2-SHA256 is provided by Passlib itself and avoids backend-specific
# bcrypt incompatibilities across developer machines and CI environments.
password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return a one-way bcrypt hash for a plaintext password."""
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Check a plaintext password against a stored hash."""
    return password_context.verify(password, password_hash)


def create_access_token(*, subject: str, secret_key: str, algorithm: str,
                        expires_minutes: int) -> tuple[str, datetime]:
    """Create a short-lived JWT and return it with its UTC expiry."""
    expires_at = datetime.now(UTC) + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "exp": expires_at, "type": "access"}
    return jwt.encode(payload, secret_key, algorithm=algorithm), expires_at


def decode_access_token(*, token: str, secret_key: str, algorithm: str) -> str | None:
    """Return the user id from a valid access token, otherwise ``None``."""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    except JWTError:
        return None

    if payload.get("type") != "access" or not isinstance(payload.get("sub"), str):
        return None
    return payload["sub"]
