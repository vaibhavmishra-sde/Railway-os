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
