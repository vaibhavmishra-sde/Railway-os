from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_is_not_plaintext() -> None:
    password_hash = hash_password("correct horse battery staple")

    assert password_hash != "correct horse battery staple"
    assert verify_password("correct horse battery staple", password_hash)
    assert not verify_password("incorrect password", password_hash)


def test_decode_access_token_returns_subject_for_valid_token() -> None:
    token, _ = create_access_token(
        subject="user-123",
        secret_key="test-secret",
        algorithm="HS256",
        expires_minutes=5,
    )

    assert (
        decode_access_token(token=token, secret_key="test-secret", algorithm="HS256")
        == "user-123"
    )


def test_decode_access_token_rejects_expired_and_wrong_type_tokens() -> None:
    expired = jwt.encode(
        {
            "sub": "user-123",
            "type": "access",
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        },
        "test-secret",
        algorithm="HS256",
    )
    refresh = jwt.encode(
        {
            "sub": "user-123",
            "type": "refresh",
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        "test-secret",
        algorithm="HS256",
    )

    assert (
        decode_access_token(token=expired, secret_key="test-secret", algorithm="HS256")
        is None
    )
    assert (
        decode_access_token(token=refresh, secret_key="test-secret", algorithm="HS256")
        is None
    )
