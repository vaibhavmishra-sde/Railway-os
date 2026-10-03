"""HTTP tests for dated train-service endpoints."""


def test_create_service_add_stop_and_filter_by_date(client) -> None:
    train = client.post(
        "/api/v1/trains", json={"number": "12301", "name": "Rajdhani"}
    ).json()
    route = client.post(
        "/api/v1/routes",
        json={"code": "NDLS-BCT", "name": "Capital Express", "total_distance_km": 1384},
    ).json()
    station = client.post(
        "/api/v1/stations",
        json={"code": "NDLS", "name": "New Delhi", "city": "Delhi", "state": "Delhi"},
    ).json()

    service_response = client.post(
        "/api/v1/services",
        json={
            "train_id": train["id"],
            "route_id": route["id"],
            "service_date": "2026-10-01",
        },
    )
    assert service_response.status_code == 201
    service_id = service_response.json()["id"]

    stop_response = client.post(
        f"/api/v1/services/{service_id}/stops",
        json={
            "station_id": station["id"],
            "stop_sequence": 1,
            "scheduled_departure": "16:55:00",
            "platform_number": "1",
        },
    )
    assert stop_response.status_code == 201

    list_response = client.get("/api/v1/services?service_date=2026-10-01")
    assert list_response.status_code == 200
    assert [service["id"] for service in list_response.json()] == [service_id]

    stops_response = client.get(f"/api/v1/services/{service_id}/stops")
    assert stops_response.status_code == 200
    assert stops_response.json()[0]["platform_number"] == "1"

    detail_response = client.get(f"/api/v1/services/{service_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["stops"][0]["station_id"] == station["id"]


def test_service_detail_returns_404_for_unknown_service(client) -> None:
    response = client.get("/api/v1/services/not-a-service")

    assert response.status_code == 404


def test_services_list_supports_bounded_pagination(client) -> None:
    train = client.post(
        "/api/v1/trains", json={"number": "12301", "name": "Rajdhani"}
    ).json()
    route = client.post(
        "/api/v1/routes",
        json={"code": "NDLS-BCT", "name": "Capital Express", "total_distance_km": 1384},
    ).json()
    for service_date in ("2026-10-01", "2026-10-02"):
        assert client.post(
            "/api/v1/services",
            json={"train_id": train["id"], "route_id": route["id"], "service_date": service_date},
        ).status_code == 201

    response = client.get("/api/v1/services?service_date=2026-10-01&offset=1&limit=1")

    assert response.status_code == 200
    assert response.json() == []


def test_service_rejects_duplicate_train_date(client) -> None:
    train = client.post(
        "/api/v1/trains", json={"number": "12301", "name": "Rajdhani"}
    ).json()
    route = client.post(
        "/api/v1/routes",
        json={"code": "NDLS-BCT", "name": "Capital Express", "total_distance_km": 1384},
    ).json()
    payload = {
        "train_id": train["id"],
        "route_id": route["id"],
        "service_date": "2026-10-01",
    }

    assert client.post("/api/v1/services", json=payload).status_code == 201
    assert client.post("/api/v1/services", json=payload).status_code == 409
