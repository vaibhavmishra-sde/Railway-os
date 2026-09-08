"""Tests for the public liveness endpoint."""

from fastapi.testclient import TestClient


def test_health_endpoint_returns_service_metadata(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "RailwayOS API",
        "version": "0.1.0",
    }
