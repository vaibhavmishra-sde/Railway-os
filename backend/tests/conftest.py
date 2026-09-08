"""Shared fixtures for the backend test suite."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    """Return an isolated client for the RailwayOS application."""
    with TestClient(create_app()) as test_client:
        yield test_client
