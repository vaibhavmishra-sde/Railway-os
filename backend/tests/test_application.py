"""Tests for application-level API configuration."""

from app.core.metadata import APP_NAME, APP_VERSION
from app.main import create_app


def test_application_exposes_project_metadata() -> None:
    application = create_app()

    assert application.title == APP_NAME
    assert application.version == APP_VERSION


def test_openapi_includes_health_response_contract() -> None:
    schema = create_app().openapi()

    response_schema = schema["paths"]["/health"]["get"]["responses"]["200"]
    assert response_schema["content"]["application/json"]["schema"]["$ref"] == (
        "#/components/schemas/HealthResponse"
    )
