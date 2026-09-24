"""HTTP tests for route endpoints."""


def test_create_route_add_stop_and_list_stops(client) -> None:
    station = client.post(
        "/api/v1/stations",
        json={"code": "NDLS", "name": "New Delhi", "city": "Delhi", "state": "Delhi"},
    ).json()
    route_response = client.post(
        "/api/v1/routes",
        json={"code": "ndls-bct", "name": "Capital Express", "total_distance_km": 1384},
    )
    assert route_response.status_code == 201
    route_id = route_response.json()["id"]

    stop_response = client.post(
        f"/api/v1/routes/{route_id}/stops",
        json={
            "station_id": station["id"],
            "stop_sequence": 1,
            "distance_from_origin_km": 0,
        },
    )
    assert stop_response.status_code == 201

    list_response = client.get(f"/api/v1/routes/{route_id}/stops")
    assert list_response.status_code == 200
    assert [stop["station_id"] for stop in list_response.json()] == [station["id"]]


def test_route_code_is_unique(client) -> None:
    payload = {"code": "NDLS-BCT", "name": "Capital Express", "total_distance_km": 1384}
    assert client.post("/api/v1/routes", json=payload).status_code == 201
    assert client.post("/api/v1/routes", json=payload).status_code == 409
