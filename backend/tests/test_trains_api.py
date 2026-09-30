"""HTTP tests for train and coach endpoints."""


def test_create_train_add_coach_and_list_coaches(client) -> None:
    train_response = client.post(
        "/api/v1/trains", json={"number": "12301", "name": "Rajdhani"}
    )
    assert train_response.status_code == 201
    train_id = train_response.json()["id"]

    coach_response = client.post(
        f"/api/v1/trains/{train_id}/coaches",
        json={"coach_number": "a1", "seat_class": "SECOND_AC", "total_seats": 48},
    )
    assert coach_response.status_code == 201
    assert coach_response.json()["coach_number"] == "A1"

    list_response = client.get(f"/api/v1/trains/{train_id}/coaches")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_train_number_is_unique(client) -> None:
    payload = {"number": "12301", "name": "Rajdhani"}
    client.post("/api/v1/trains", json=payload)
    assert client.post("/api/v1/trains", json=payload).status_code == 409


def test_list_and_get_train(client) -> None:
    created = client.post(
        "/api/v1/trains", json={"number": "12301", "name": "Rajdhani"}
    ).json()

    assert client.get("/api/v1/trains").json()[0]["number"] == "12301"
    assert client.get(f"/api/v1/trains/{created['id']}").json()["name"] == "Rajdhani"
    assert client.get("/api/v1/trains/missing").status_code == 404


def test_train_list_supports_search_and_pagination(client) -> None:
    for number, name in (("12301", "Rajdhani"), ("12951", "Mumbai Express")):
        client.post("/api/v1/trains", json={"number": number, "name": name})

    response = client.get("/api/v1/trains", params={"search": "mumbai", "limit": 1})
    assert response.status_code == 200
    assert [train["number"] for train in response.json()] == ["12951"]


def test_train_list_rejects_invalid_pagination(client) -> None:
    assert client.get("/api/v1/trains", params={"limit": 0}).status_code == 422
    assert client.get("/api/v1/trains", params={"limit": 101}).status_code == 422
