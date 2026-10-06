from app.services.identity import authenticate_user, create_user


def test_identity_service_normalizes_email_and_authenticates(client, db_session) -> None:
    user = create_user(db_session, email="  Admin@Example.com ", password="secret")

    assert user.email == "admin@example.com"
    assert authenticate_user(db_session, email="ADMIN@example.com", password="secret")
    assert authenticate_user(db_session, email="admin@example.com", password="wrong") is None
