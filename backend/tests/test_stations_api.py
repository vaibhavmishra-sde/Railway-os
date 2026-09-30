"""HTTP tests for station endpoints."""


def test_create_then_list_stations(client) -> None:
    response = client.post(
        "/api/v1/stations",
        json={"code": "ndls", "name": "New Delhi", "city": "Delhi", "state": "Delhi"},
    )

    assert response.status_code == 201
    assert response.json()["code"] == "NDLS"

    list_response = client.get("/api/v1/stations")
    assert list_response.status_code == 200
    assert [station["code"] for station in list_response.json()] == ["NDLS"]


def test_duplicate_station_code_returns_conflict(client) -> None:
    station = {"code": "NDLS", "name": "New Delhi", "city": "Delhi", "state": "Delhi"}
    client.post("/api/v1/stations", json=station)

    response = client.post("/api/v1/stations", json=station)
    assert response.status_code == 409


def test_station_search_and_pagination(client) -> None:
    for code, city in (("NDLS", "Delhi"), ("BCT", "Mumbai"), ("JP", "Jaipur")):
        client.post(
            "/api/v1/stations",
            json={"code": code, "name": f"{city} Central", "city": city, "state": city},
        )

    response = client.get("/api/v1/stations", params={"search": "mumbai", "limit": 1})
    assert response.status_code == 200
    assert [station["code"] for station in response.json()] == ["BCT"]


def test_station_detail_and_missing_station(client) -> None:
    created = client.post(
        "/api/v1/stations",
        json={"code": "NDLS", "name": "New Delhi", "city": "Delhi", "state": "Delhi"},
    ).json()

    assert client.get(f"/api/v1/stations/{created['id']}").json()["code"] == "NDLS"
    assert client.get("/api/v1/stations/missing").status_code == 404
