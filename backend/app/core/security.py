"""Password hashing helpers used by the identity service."""

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
