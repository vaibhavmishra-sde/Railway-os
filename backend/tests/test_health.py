"""Tests for the public liveness endpoint."""

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_returns_service_metadata() -> None:
    response = TestClient(create_app()).get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "RailwayOS API",
        "version": "0.1.0",
    }
