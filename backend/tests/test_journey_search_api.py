"""Contract tests for direct dated journey search."""

from datetime import time

from app.api.v1.search import _duration_minutes


def test_duration_calculation_crosses_midnight():
    assert _duration_minutes(time(23, 45), time(1, 15)) == 90
    assert _duration_minutes(time(8, 0), time(8, 0)) == 0
    assert _duration_minutes(None, time(1, 15)) is None
    assert _duration_minutes(time(8, 0), None) is None


def _create_network(client):
    stations = {}
    for code, name in (
        ("NDLS", "New Delhi"),
        ("BCT", "Mumbai Central"),
        ("JP", "Jaipur"),
    ):
        stations[code] = client.post(
            "/api/v1/stations",
            json={"code": code, "name": name, "city": name, "state": "Test"},
        ).json()
    train = client.post(
        "/api/v1/trains", json={"number": "12301", "name": "Capital Express"}
    ).json()
    route = client.post(
        "/api/v1/routes",
        json={"code": "NDLS-BCT", "name": "Test Route", "total_distance_km": 100},
    ).json()
    service = client.post(
        "/api/v1/services",
        json={
            "train_id": train["id"],
            "route_id": route["id"],
            "service_date": "2026-10-19",
        },
    ).json()
    for sequence, code, departure, arrival in (
        (1, "NDLS", "06:00:00", None),
        (2, "JP", "09:00:00", "08:55:00"),
        (3, "BCT", None, "14:00:00"),
    ):
        client.post(
            f"/api/v1/services/{service['id']}/stops",
            json={
                "station_id": stations[code]["id"],
                "stop_sequence": sequence,
                "scheduled_departure": departure,
                "scheduled_arrival": arrival,
            },
        )
    return stations


def test_search_returns_ordered_direct_match(authenticated_client):
    _create_network(authenticated_client)
    trains = authenticated_client.get("/api/v1/trains?search=12301").json()
    train_id = trains[0]["id"]
    for coach_number, seat_class in (("A1", "FIRST_AC"), ("S1", "SLEEPER")):
        assert (
            authenticated_client.post(
                f"/api/v1/trains/{train_id}/coaches",
                json={
                    "coach_number": coach_number,
                    "seat_class": seat_class,
                    "total_seats": 20,
                },
            ).status_code
            == 201
        )
    response = authenticated_client.get(
        "/api/v1/search/journeys?origin=ndls&destination=bct&service_date=2026-10-19"
    )
    assert response.status_code == 200
    body = response.json()
    assert body["origin"] == "NDLS"
    assert body["items"][0]["origin"]["stop_sequence"] == 1
    assert body["items"][0]["destination"]["station_name"] == "Mumbai Central"
    assert body["items"][0]["departure_time"] == "06:00:00"
    assert body["items"][0]["arrival_time"] == "14:00:00"
    assert body["items"][0]["duration_minutes"] == 480
    assert body["items"][0]["available_classes"] == ["FIRST_AC", "SLEEPER"]
    assert body["items"][0]["fares"] == {"FIRST_AC": 378, "SLEEPER": 122}


def test_search_rejects_same_and_unknown_stations(client):
    assert (
        client.get(
            "/api/v1/search/journeys?origin=NDLS&destination=ndls&service_date=2026-10-19"
        ).status_code
        == 422
    )
    assert (
        client.get(
            "/api/v1/search/journeys?origin=NOPE&destination=BCT&service_date=2026-10-19"
        ).status_code
        == 404
    )


def test_search_supports_pagination_and_empty_result(authenticated_client):
    _create_network(authenticated_client)
    response = authenticated_client.get(
        "/api/v1/search/journeys?origin=BCT&destination=NDLS&service_date=2026-10-19&offset=1&limit=1"
    )
    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["items"] == []


def test_search_rejects_invalid_pagination_and_missing_query(client):
    assert (
        client.get(
            "/api/v1/search/journeys?origin=NDLS&destination=BCT&service_date=2026-10-19&limit=101"
        ).status_code
        == 422
    )
    assert (
        client.get(
            "/api/v1/search/journeys?origin=NDLS&destination=BCT&service_date=2026-10-19&offset=-1"
        ).status_code
        == 422
    )
    assert client.get("/api/v1/search/journeys").status_code == 422


def test_search_seat_class_filter_uses_available_coaches(authenticated_client):
    _create_network(authenticated_client)
    train_id = authenticated_client.get("/api/v1/trains?search=12301").json()[0]["id"]
    authenticated_client.post(
        f"/api/v1/trains/{train_id}/coaches",
        json={"coach_number": "S1", "seat_class": "SLEEPER", "total_seats": 20},
    )

    sleeper = authenticated_client.get(
        "/api/v1/search/journeys?origin=NDLS&destination=BCT&service_date=2026-10-19&seat_class=SLEEPER"
    )
    first_ac = authenticated_client.get(
        "/api/v1/search/journeys?origin=NDLS&destination=BCT&service_date=2026-10-19&seat_class=FIRST_AC"
    )
    assert len(sleeper.json()["items"]) == 1
    assert first_ac.json()["items"] == []
