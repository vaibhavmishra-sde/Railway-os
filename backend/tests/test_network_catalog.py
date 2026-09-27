from app.data.network import ROUTES, SERVICES, STATIONS, validate_catalog


def test_synthetic_catalog_is_valid():
    validate_catalog()


def test_catalog_has_expected_demo_scale():
    assert 10 <= len(STATIONS) <= 20
    assert 3 <= len(ROUTES)
    assert 5 <= len(SERVICES) <= 10


def test_routes_are_ordered_and_connected():
    station_codes = {station.code for station in STATIONS}
    for route in ROUTES:
        assert route.station_codes[0] in station_codes
        assert len(route.station_codes) == len(set(route.station_codes))
        assert route.distance_km > 0


def test_service_numbers_and_dates_are_unique_pairs():
    pairs = {(service.train_number, service.service_date) for service in SERVICES}
    assert len(pairs) == len(SERVICES)
    assert all(len(service.train_number) == 5 for service in SERVICES)
