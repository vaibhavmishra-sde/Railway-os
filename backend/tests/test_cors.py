from fastapi.testclient import TestClient

from app.main import create_app


def test_frontend_origin_can_preflight_api_requests():
    response = TestClient(create_app()).options(
        "/api/v1/services",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "GET" in response.headers["access-control-allow-methods"]
