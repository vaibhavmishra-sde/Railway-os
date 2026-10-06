"""Identity operations for registration and password verification."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.identity import User


class EmailAlreadyRegisteredError(ValueError):
    """Raised when registration uses an existing email address."""


def create_user(session: Session, *, email: str, password: str) -> User:
    """Create a user with a normalized email and one-way password hash."""
    user = User(email=email.strip().lower(), password_hash=hash_password(password))
    session.add(user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise EmailAlreadyRegisteredError from exc
    session.refresh(user)
    return user


def authenticate_user(session: Session, *, email: str, password: str) -> User | None:
    """Return an active user for valid credentials, otherwise ``None``."""
    user = session.scalar(select(User).where(User.email == email.strip().lower()))
    if (
        user is None
        or not user.is_active
        or not verify_password(password, user.password_hash)
    ):
        return None
    return user
