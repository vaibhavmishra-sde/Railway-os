def test_unauthenticated_network_mutation_is_rejected(client) -> None:
    response = client.post(
        "/api/v1/trains",
        json={"train_number": "70001", "name": "Demo Express"},
    )

    assert response.status_code == 401


def test_passenger_cannot_create_a_route(client, db_session) -> None:
    from app.services.identity import create_user

    user = create_user(db_session, email="passenger2@example.com", password="secret")
    token_response = client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "secret"},
    )

    response = client.post(
        "/api/v1/routes",
        headers={"Authorization": f"Bearer {token_response.json()['access_token']}"},
        json={"code": "DEMO", "name": "Demo Route"},
    )

    assert response.status_code == 403
