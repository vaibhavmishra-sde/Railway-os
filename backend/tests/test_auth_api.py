from app.core.security import hash_password
from app.models.identity import User
from app.services.identity import create_user


def test_login_returns_bearer_token(client, db_session) -> None:
    create_user(db_session, email="admin@example.com", password="secret")

    response = client.post(
        "/api/v1/auth/login",
        json={"email": " ADMIN@example.com ", "password": "secret"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["expires_at"]


def test_login_hides_invalid_and_inactive_credentials(client, db_session) -> None:
    user = User(
        email="inactive@example.com",
        password_hash=hash_password("secret"),
        is_active=False,
    )
    db_session.add(user)
    db_session.commit()

    for email in ("inactive@example.com", "missing@example.com"):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": "secret"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"


def test_me_returns_authenticated_user_without_sensitive_fields(client, db_session) -> None:
    create_user(db_session, email="admin@example.com", password="secret")
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "secret"},
    )

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "admin@example.com"
    assert "password_hash" not in response.json()


def test_me_rejects_missing_and_malformed_tokens(client) -> None:
    assert client.get("/api/v1/auth/me").status_code == 401
    assert client.get(
        "/api/v1/auth/me", headers={"Authorization": "Bearer not-a-jwt"}
    ).status_code == 401
