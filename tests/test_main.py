"""Unit tests for the FastAPI app.

These run in GitHub Actions on every push and pull request. Failing any
of these tests blocks the deployment pipeline (the CI quality gate).
"""

from fastapi.testclient import TestClient

from app.main import APP_NAME, app

client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_payload_shape() -> None:
    response = client.get("/version")
    assert response.status_code == 200

    body = response.json()
    assert set(body.keys()) == {"name", "version", "color"}
    assert body["name"] == APP_NAME
    # color must be one of the two values used by the blue/green setup
    assert body["color"] in {"blue", "green"}
    # version is either "dev" locally or the 7-char short SHA on Render
    assert 1 <= len(body["version"]) <= 7


def test_index_renders_html_with_version_banner() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")

    html = response.text
    assert APP_NAME in html
    assert "version:" in html
    assert "environment:" in html


def test_docs_endpoint_available() -> None:
    """FastAPI's auto-generated OpenAPI UI must be reachable."""
    response = client.get("/docs")
    assert response.status_code == 200
